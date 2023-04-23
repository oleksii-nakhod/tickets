from flask import Flask, render_template, request, redirect, url_for, jsonify, session
import os
import datetime
from dotenv import load_dotenv
from connection import *
from database import *
import stripe
stripe.api_key = os.getenv('STRIPE_API_KEY')
endpoint_secret = os.getenv('STRIPE_ENDPOINT_KEY')
load_dotenv()

public_url = f"{os.getenv('DOMAIN')}"

cnxpool_config = {
    "host": f"{os.getenv('HOST')}",
    "database": os.getenv('DATABASE'),
    "user": os.getenv('USER'),
    "password": os.getenv('PASSWORD')
}

database_type = os.getenv('DATABASE_TYPE')

cnxpool = ConnectionPoolList().get_cnxpool(database_type, cnxpool_config)

database = DatabaseList().get_database(database_type, cnxpool)

carriage_table = database.get_table('carriage')
carriage_type_table = database.get_table('carriage_type')
seat_table = database.get_table('seat')
station_table = database.get_table('station')
ticket_table = database.get_table('ticket')
train_table = database.get_table('train')
trip_table = database.get_table('trip')
trip_station_table = database.get_table('trip_station')
user_table = database.get_table('user')
user_role_table = database.get_table('user_role')


template_dir = os.path.abspath('frontend')

app = Flask(__name__, template_folder='templates', static_folder='static')

app.secret_key = b'yb4No3!w2NX528'

@app.route("/")
def index():
    return render_template("index.html")


@app.route("/tickets")
def tickets():
    return None

@app.route("/stations")
def stations():
    stations = []
    args = request.args
    try:
        query = args.get("q")
        stations = station_table.find(query)
    except Exception as e:
        print(e)
    return jsonify([station.__dict__ for station in stations])


@app.route("/signup", methods=['POST'])
def signup():
    try:
        user = user_table.find(request.json['email'])
        if user:
            return {'msg': 'This email address is already registered. If that\'s you, please log in instead.'}, 409
        else:
            user_id = user_table.create(User(
                name=request.json['name'],
                email=request.json['email'],
                user_role_id=2
            ), request.json['password'])
            session['logged_in'] = True
            session['id'] = user_id
            session['email'] = request.json['email']
            session['name'] = request.json['name']
            return {'msg': 'success'}, 200
    except Exception as e:
        print(e)
    return {'msg': 'server error'}, 500


@app.route("/login", methods=['POST'])
def login():
    try:
        user = user_table.find(request.json['email'], request.json['password'])
        if user:
            session['logged_in'] = True
            session['id'] = user.id
            session['email'] = user.email
            session['name'] = user.name
            return {'msg': 'Success'}, 200
        else:
            return {'msg': 'Incorrect email/password'}, 401
    except Exception as e:
        print(e)
    return {'msg': 'Server Error'}, 500


@app.route("/logout", methods=['GET'])
def logout():
    session.clear()
    return redirect(url_for('index'))


@app.route("/orders", methods=['GET'])
def orders():
    return redirect(url_for('index'))


@app.route("/profile", methods=['GET', 'PATCH'])
def profile():
    if request.method == 'GET':
        if 'logged_in' in session and session['logged_in']:
            return render_template("profile.html")
        return redirect(url_for('index'))
        
    if request.method == 'PATCH':
        if not 'logged_in' in session or not session['logged_in']:
            return {'msg': 'Please log in to change your information'}, 401
        try:
            print(request.json)
            if 'password' in request.json['fields']:
                user = user_table.find(session['email'], request.json['password'])
                if not user:
                    return {'msg': 'Incorrect password'}, 401
                    
            user_table.update(session['id'], request.json['fields'])
            user = user_table.read(session['id'])
            session['name'] = user.name
            session['email'] = user.email
            return {'msg': 'Success'}, 200
        except Exception as e:
            print(e)
        return {'msg': 'Server Error'}, 500

@app.route("/search", methods=['GET'])
def search():
    from_station = request.args.get('from')
    to_station = request.args.get('to')
    depart_date = request.args.get('depart')
    trips = trip_table.find(from_station, to_station, depart_date)
    data = {'trips': []}
    for trip in trips:
        train = train_table.read(trip[0])
        carriage_seats = carriage_table.find(trip[0])
        duration_seconds = (trip[2] - trip[1]).total_seconds()
        hours = int(duration_seconds//3600)
        minutes = int((duration_seconds - hours * 3600)//60)
        duration = f'{hours} h {minutes} min'
        data['trips'].append({
            'id': trip[0],
            'train_id': train.id,
            'train_name': train.name,
            'time_dep': trip[1],
            'time_arr': trip[2],
            'time_dep_pretty': trip[1].strftime('%H:%M'),
            'time_arr_pretty': trip[2].strftime('%H:%M'),
            'duration_pretty': duration,
            'base_price': trip[3],
            'carriage_seats': [
                {
                    'carriage_id': carriage_seat[0],
                    'carriage_type': carriage_seat[1],
                    'seat_price': int(trip[3] * carriage_seat[2]),
                    'seat_quantity': carriage_seat[3]
                }
                for carriage_seat in carriage_seats
            ]
        })
    station_start = station_table.read(from_station)
    station_end = station_table.read(to_station)
    data['station_start_name'] = station_start.name
    data['station_start_id'] = station_start.id
    data['station_end_name'] = station_end.name
    data['station_end_id'] = station_end.id
    data['depart_date'] = datetime.datetime.strptime(depart_date, '%Y-%m-%d').strftime('%a, %b %d %Y')
    print(data)
    return render_template('search.html', data=data)


@app.route("/seats", methods=['GET'])
def seats():
    trip = request.args.get('trip')
    train = request.args.get('train')
    ctype = request.args.get('ctype')
    from_station = request.args.get('from')
    to_station = request.args.get('to')
    carriages = seat_table.find(trip, train, ctype, from_station, to_station)
    station_start = station_table.read(from_station)
    station_end = station_table.read(to_station)
    trip_extra_info = trip_station_table.find(trip, from_station, to_station)
    carriage_type = carriage_type_table.read(ctype)
    data = {
        'carriages': carriages,
        'trip_id': trip,
        'train_id': train,
        'train_name': train_table.read
        (train).name,
        'station_start_name': station_start.name,
        'station_start_id': station_start.id,
        'station_end_name': station_end.name,
        'station_end_id': station_end.id,
        'carriage_type_id': ctype,
        'carriage_type_name': carriage_type.name,
        'price': int(trip_extra_info[2] * carriage_type.price_mod),
        'depart_date': trip_extra_info[0].strftime('%Y-%m-%d'),
        'depart_date_pretty': trip_extra_info[0].strftime('%a, %b %d %Y'),
        'time_dep_pretty': trip_extra_info[0].strftime('%H:%M'),
        'time_arr_pretty': trip_extra_info[1].strftime('%H:%M')
    }

    print(data)
    return render_template('seats.html', data=data)


@app.route("/order", methods=['POST'])
def order():
    station_start = station_table.read(request.json['station_start_id'])
    station_end = station_table.read(request.json['station_end_id'])
    trip = trip_table.read(request.json['trip_id'])
    train = train_table.read(trip.train_id)
    trip_extra_info = trip_station_table.find(
        trip.id, request.json['station_start_id'], request.json['station_end_id'])
    prices = []
    for seat_id in request.json['seats']:
        seat = seat_table.read(seat_id)
        carriage = carriage_table.read(seat.carriage_id)
        carriage_type = carriage_type_table.read(carriage.carriage_type_id)
        train = train_table.read(carriage.train_id)
        name = f"{station_start.name} - {station_end.name}, Train {train.name}, Carriage {carriage.num}, Seat: {seat.num}"
        product = stripe.Product.create(
        name=name)
        
        prices.append(stripe.Price.create(
        unit_amount=trip_extra_info[2]*carriage_type.price_mod,
        currency="uah",
        product=product.id,
        ))
    checkout_session = stripe.checkout.Session.create(
        success_url=f"{public_url}/",
        cancel_url=f"{public_url}/seats?trip={trip.id}&train={train.id}&ctype={carriage_type.id}&from={station_start.id}&to={station_end.id}",
        line_items=[
            {
                "price": price.id,
                "quantity": 1,
            } for price in prices
        ],
        mode="payment"
    )
    print(checkout_session)
    return {'url': checkout_session.url}

@app.route("/payment-completed", methods=['POST'])
def payment_completed():
    payload = request.get_data(as_text=True)
    sig_header = request.headers.get('Stripe-Signature')
    print(payload)
    print(sig_header)
    event = None
    try:
        event = stripe.Webhook.construct_event(payload, sig_header, endpoint_secret)
    except ValueError as e:
        # Invalid payload
        return {'msg': 'Invalid payload'}, 400
    except stripe.error.SignatureVerificationError as e:
        # Invalid signature
        return {'msg': 'This request didn\'t come from Stripe'}, 400

    # Passed signature verification
    return {'msg': 'success'}, 200
    
@app.errorhandler(404)
def handle_404(e):
    return redirect(url_for('index'))

@app.errorhandler(500)
def handle_500(e):
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(host="localhost", port=5000, threaded=True, debug=True)