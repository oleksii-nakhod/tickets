from flask import current_app, session, redirect, url_for, render_template, send_file, after_this_request
from database.entity.ticket import *
from database.entity.trip_station import *
from database.entity.station import *
from database.mysql_implementation.station import *
from database.mysql_implementation.trip import *
from database.mysql_implementation.train import *
from database.mysql_implementation.trip_station import *
from database.mysql_implementation.seat import *
from database.mysql_implementation.carriage import *
from database.mysql_implementation.carriage_type import *
from database.mysql_implementation.ticket import *
import stripe
import random
import string
import os
import qrcode
from dotenv import load_dotenv

class OrderService:
    def read(self):
        if not 'logged_in' in session or not session['logged_in']:
            return redirect(url_for('index'))
        engine = current_app.config['engine']
        ticket_table = current_app.config['tables']['ticket']
        trip_station_table = current_app.config['tables']['trip_station']
        station_table = current_app.config['tables']['station']
        with Session(engine) as s:
            tickets = ticket_table.find(s, session['id'])
            data = {'tickets': []}
            for ticket in tickets:
                ticket_info = ticket_table.info(s, ticket.id)
                trip_station_start = trip_station_table.read(s, ticket_info[4])
                trip_station_end = trip_station_table.read(s, ticket_info[5])
                station_start = station_table.read(s, trip_station_start.id)
                station_end = station_table.read(s, trip_station_end.id)
                data['tickets'].append({
                    'id': ticket_info[0],
                    'station_start_name': station_start.name,
                    'station_end_name': station_end.name,
                    'time_dep': trip_station_start.time_dep
                })
        return render_template('orders.html', data=data)
    
    def create(self, station_start_id, station_end_id, trip_id, seats):
        if not 'logged_in' in session or not session['logged_in']:
            return {'msg': 'Please login to create an order'}, 401
        load_dotenv()
        stripe.api_key = os.getenv('STRIPE_API_KEY')
        user_id = session['id']
        public_url = current_app.config['public_url']
        engine = current_app.config['engine']
        station_table = current_app.config['tables']['station']
        trip_table = current_app.config['tables']['trip']
        user_id = session['id']
        train_table = current_app.config['tables']['train']
        trip_station_table = current_app.config['tables']['trip_station']
        carriage_table = current_app.config['tables']['carriage']
        carriage_type_table = current_app.config['tables']['carriage_type']
        seat_table = current_app.config['tables']['seat']
        with Session(engine) as s:
            station_start = station_table.read(s, station_start_id)
            station_end = station_table.read(s, station_end_id)
            trip = trip_table.read(s, trip_id)
            train = train_table.read(s, trip.train_id)
            trip_extra_info = trip_station_table.find(s, 
                trip.id, station_start_id, station_end_id)
            line_items = []
            for seat_id in seats:
                seat = seat_table.read(s, seat_id)
                carriage = carriage_table.read(s, seat.carriage_id)
                carriage_type = carriage_type_table.read(s, carriage.carriage_type_id)
                train = train_table.read(s, carriage.train_id)
                name = f"{station_start.name} - {station_end.name}, Train {train.name}, Carriage {carriage.num}, Seat: {seat.num}"
                line_items.append({
                    'price_data': {
                        'currency': 'uah',
                        'unit_amount': trip_extra_info[2]*carriage_type.price_mod,
                        'product_data': {
                            'name': name,
                            'metadata': {
                                'user_id': user_id,
                                'seat_id': seat.id,
                                'station_start_id': station_start.id,
                                'station_end_id': station_end.id
                            }
                        },
                    },
                    'quantity': 1
                })
            checkout_session = stripe.checkout.Session.create(
                success_url=f"{public_url}{url_for('orders')}",
                cancel_url=f"{public_url}{url_for('seats')}?trip={trip.id}&ctype={carriage_type.id}&from={station_start.id}&to={station_end.id}",
                line_items=line_items,
                mode='payment'
            )
        return {'url': checkout_session.url}, 200
    
    def complete(self, payload, sig_header, checkout_session_id):
        stripe.api_key = os.getenv('STRIPE_API_KEY')
        endpoint_secret = os.getenv('STRIPE_ENDPOINT_KEY')
        event = None
        try:
            event = stripe.Webhook.construct_event(payload, sig_header, endpoint_secret)
        except ValueError as e:
            return {'msg': 'Invalid payload'}, 400
        except stripe.error.SignatureVerificationError as e:
            return {'msg': 'This request didn\'t come from Stripe'}, 400

        checkout_session = stripe.checkout.Session.retrieve(
            checkout_session_id,
            expand=['line_items']
        )
        for item in checkout_session['line_items']['data']:
            product = stripe.Product.retrieve(
                item['price']['product']
            )
            metadata = product['metadata']
            engine = current_app.config['engine']
            ticket_table = current_app.config['tables']['ticket']
            with Session(engine) as s:
                ticket_table.create(s, Ticket(
                    user_id=metadata['user_id'],
                    seat_id=metadata['seat_id'],
                    trip_station_start_id=metadata['station_start_id'],
                    trip_station_end_id=metadata['station_end_id'],
                    token=''.join(random.choices(string.ascii_uppercase + string.digits, k=10))
                ))
        return {'msg': 'success'}, 200
    
    def verify(self, id, token):
        engine = current_app.config['engine']
        ticket_table = current_app.config['tables']['ticket']
        trip_station_table = current_app.config['tables']['trip_station']
        station_table = current_app.config['tables']['station']
        with Session(engine) as s:
            ticket = ticket_table.verify(s, id, token)
            if not ticket:
                data = {'status': 'invalid'}
            else:
                ticket_info = ticket_table.info(s, id)
                trip_station_start = trip_station_table.read(s, ticket_info[4])
                trip_station_end = trip_station_table.read(s, ticket_info[5])
                station_start = station_table.read(s, trip_station_start.id)
                station_end = station_table.read(s, trip_station_end.id)
                data = {'status': 'valid',
                    'ticket': {
                        'id': ticket_info[0],
                        'train_name': ticket_info[1],
                        'carriage_num': ticket_info[2],
                        'seat_num': ticket_info[3],
                        'station_start_name': station_start.name,
                        'station_end_name': station_end.name,
                        'time_dep': trip_station_start.time_dep,
                        'time_arr': trip_station_end.time_arr,
                        'user_email': ticket_info[6]
                    }}
        return render_template('verify.html', data=data)
    
    def create_qrcode(self, ticket_id):
        if not 'logged_in' in session or not session['logged_in']:
            return redirect(url_for('index'))
        engine = current_app.config['engine']
        ticket_table = current_app.config['tables']['ticket']
        with Session(engine) as s:
            ticket = ticket_table.read(s, ticket_id)
            public_url = current_app.config['public_url']
            if ticket.user_id != session['id']:
                return redirect(url_for('index'))
            img = qrcode.make(f"{public_url}{url_for('verify')}?id={ticket_id}&token={ticket.token}")
            img_path = f'qrcode-{ticket_id}.png'
            img.save(img_path)
            response = send_file(img_path, mimetype='image/png')
            @after_this_request
            def remove_file(response):
                try:
                    os.remove(img_path)
                except Exception as e:
                    print(e)
                return response
        return response