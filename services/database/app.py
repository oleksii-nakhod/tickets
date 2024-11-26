from flask import Flask, request, redirect, current_app
from waitress import serve
from dotenv import load_dotenv
from urllib.parse import quote_plus
import os
from database import *
import logging
import random
import string

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

load_dotenv()

engine = create_engine(
    f"{os.getenv('DATABASE_TYPE')}+{os.getenv('DATABASE_API')}://{os.getenv('USER')}:{quote_plus(os.getenv('PASSWORD'))}@{os.getenv('HOST')}/{os.getenv('DATABASE')}",
    pool_size=5
)

database_type = os.getenv('DATABASE_TYPE')

database = DatabaseList().get_database(database_type)

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

tables = {
    'carriage': carriage_table,
    'carriage_type': carriage_type_table,
    'seat': seat_table,
    'station': station_table,
    'ticket': ticket_table,
    'train': train_table,
    'trip': trip_table,
    'trip_station': trip_station_table,
    'user': user_table,
    'user_role': user_role_table
}

app = Flask(__name__, template_folder='templates', static_folder='static')

app.secret_key = b'yb4No3!w2NX528'

with app.app_context():
    app.config['engine'] = engine
    app.config['tables'] = tables

@app.route("/carriage-types", methods=['GET'])
def carriage_types():
    engine = current_app.config['engine']
    with Session(engine) as s:
        carriage_types = carriage_type_table.read_all(s)
        return carriage_types

@app.route("/carriage-types/<id>", methods=['GET'])
def carriage_type(id):
    engine = current_app.config['engine']
    with Session(engine) as s:
        carriage_type = carriage_type_table.read(s, id)
        return carriage_type
    
@app.route("/carriages", methods=['GET'])
def carriages():
    engine = current_app.config['engine']
    with Session(engine) as s:
        trip = request.args.get('trip')
        if trip:
            carriages = carriage_table.find(s, trip)
        else:
            carriages = carriage_table.read_all(s)
        return carriages

@app.route("/carriages/<id>", methods=['GET'])
def carriage(id):
    engine = current_app.config['engine']
    with Session(engine) as s:
        carriage = carriage_table.read(s, id)
        return carriage

@app.route("/seats", methods=['GET'])
def seats():
    engine = current_app.config['engine']
    with Session(engine) as s:
        trip = request.args.get('trip')
        train = request.args.get('train')
        ctype = request.args.get('ctype')
        from_station = request.args.get('from_station')
        to_station = request.args.get('to_station')
        if trip:
            seats = seat_table.find(s, trip, train, ctype, from_station, to_station)
        else:
            seats = seat_table.read_all(s)
        return seats
    
@app.route("/seats/<id>", methods=['GET'])
def seat(id):
    engine = current_app.config['engine']
    with Session(engine) as s:
        seat = seat_table.read(s, id)
        return seat
    
@app.route("/stations", methods=['GET'])
def stations():
    engine = current_app.config['engine']
    with Session(engine) as s:
        query = request.args.get('q')
        if query:
            stations = station_table.find(s, query)
        else:
            stations = station_table.read_all(s)
        return stations

@app.route("/stations/<id>", methods=['GET'])
def station(id):
    engine = current_app.config['engine']
    with Session(engine) as s:
        station = station_table.read(s, id)
        return station

@app.route("/tickets", methods=['GET'])
def tickets():
    engine = current_app.config['engine']
    with Session(engine) as s:
        user = request.args.get('user')
        if user:
            tickets = ticket_table.find(s, user)
        else:
            tickets = ticket_table.read_all(s)
        return tickets
    
@app.route("/tickets/<id>", methods=['GET'])
def ticket(id):
    engine = current_app.config['engine']
    with Session(engine) as s:
        ticket = ticket_table.read(s, id)
        return ticket

@app.route("/tickets/<id>/info", methods=['GET'])
def ticket_info(id):
    engine = current_app.config['engine']
    with Session(engine) as s:
        ticket = ticket_table.info(s, id)
        return ticket

@app.route("/tickets/<id>/verify", methods=['GET'])
def ticket_verify(id):
    engine = current_app.config['engine']
    with Session(engine) as s:
        token = request.args.get('token')
        ticket = ticket_table.verify(s, id, token)
        return ticket
    
@app.route("/tickets", methods=['POST'])
def create_ticket():
    engine = current_app.config['engine']
    with Session(engine) as s:
        data = request.json
        ticket = ticket_table.create(s, data)
        return ticket
    
@app.route("/trains", methods=['GET'])
def trains():
    engine = current_app.config['engine']
    with Session(engine) as s:
        trip = request.args.get('trip')
        if trip:
            trains = train_table.find(s, trip)
        else:
            trains = train_table.read_all(s)
        return trains
    
@app.route("/trains/<id>", methods=['GET'])
def train(id):
    engine = current_app.config['engine']
    with Session(engine) as s:
        train = train_table.read(s, id)
        return train

@app.route("/trip-stations", methods=['GET'])
def trip_stations():
    engine = current_app.config['engine']
    with Session(engine) as s:
        trip_id = request.args.get('trip_id')
        station_id = request.args.get('station_id')
        if trip_id:
            trip_stations = trip_station_table.find(s, trip_id, station_id)
        else:
            trip_stations = trip_station_table.read_all(s)
        return trip_stations

@app.route("/trip-stations/<id>", methods=['GET'])
def trip_station(id):
    engine = current_app.config['engine']
    with Session(engine) as s:
        trip_station = trip_station_table.read(s, id)
        return trip_station

@app.route("/trip-stations/info", methods=['GET'])
def trip_station_info():
    engine = current_app.config['engine']
    with Session(engine) as s:
        trip = request.args.get('trip')
        station_start = request.args.get('station_start')
        station_end = request.args.get('station_end')
        trip_station = trip_station_table.info(s, trip, station_start, station_end)
        return trip_station

@app.route("/trips", methods=['GET'])
def trips():
    engine = current_app.config['engine']
    with Session(engine) as s:
        station_start = request.args.get('station_start')
        station_end = request.args.get('station_end')
        depart_date = request.args.get('depart_date')
        if station_start:
            trips = trip_table.find(s, station_start, station_end, depart_date)
        else:
            trips = trip_table.read_all(s)
        return trips

@app.route("/trips/<id>", methods=['GET'])
def trip(id):
    engine = current_app.config['engine']
    with Session(engine) as s:
        trip = trip_table.read(s, id)
        return trip

@app.route("/user-roles", methods=['GET'])
def user_roles():
    engine = current_app.config['engine']
    with Session(engine) as s:
        user_roles = user_role_table.read_all(s)
        return user_roles

@app.route("/user-roles/<id>", methods=['GET'])
def user_role(id):
    engine = current_app.config['engine']
    with Session(engine) as s:
        user_role = user_role_table.read(s, id)
        return user_role
    
@app.route("/users", methods=['GET'])
def users():
    engine = current_app.config['engine']
    with Session(engine) as s:
        email = request.args.get('email')
        password = request.args.get('password')
        if email:
            users = user_table.find(s, email, password)
        else:
            users = user_table.read_all(s)
        return users

@app.route("/users/<id>", methods=['GET'])
def user(id):
    engine = current_app.config['engine']
    with Session(engine) as s:
        user = user_table.read(s, id)
        return user

@app.route("/users", methods=['POST'])
def create_user():
    engine = current_app.config['engine']
    with Session(engine) as s:
        data = request.json
        confirm_email_token = ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))
        user = user_table.create(s, User(
            name=data['name'],
            email=data['email'],
            user_role_id=2,
            confirm_email_token=confirm_email_token
        ), data['password'])
        return user

@app.route("/users/<id>", methods=['PUT'])
def update_user(id):
    engine = current_app.config['engine']
    with Session(engine) as s:
        data = request.json
        user = user_table.update(s, id, data)
        return user

if __name__ == '__main__':
    serve(app, host='0.0.0.0', port=5001)