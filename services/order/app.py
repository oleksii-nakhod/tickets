from flask import Flask, render_template, request, redirect
from waitress import serve
import requests
import logging
import os
import stripe

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

database_service_host = os.getenv('DATABASE_SERVICE_HOST')
database_service_port = os.getenv('DATABASE_SERVICE_PORT')
database_service_base_url = f"http://{database_service_host}:{database_service_port}"

frontend_service_host = os.getenv('FRONTEND_SERVICE_HOST')
frontend_service_port = os.getenv('FRONTEND_SERVICE_PORT')
frontend_service_base_url = f"http://{frontend_service_host}:{frontend_service_port}"

stripe.api_key = os.getenv('STRIPE_API_KEY')

app = Flask(__name__)

@app.route("/orders", methods=["GET"])
def orders():
    user = request.args.get('user')
    tickets = requests.get(
        f"{database_service_base_url}/tickets",
        params={"user": user}
    ).json()
    data = {'tickets': []}
    for ticket in tickets:
        ticket_info = requests.get(
            f"{database_service_base_url}/tickets/{ticket['id']}/info",
            params={"user": user}
        ).json()
        trip_station_start = requests.get(
            f"{database_service_base_url}/trip-stations/{ticket_info['trip_station_start']}"
        ).json()
        trip_station_end = requests.get(
            f"{database_service_base_url}/trip-stations/{ticket_info['trip_station_end']}"
        ).json()
        station_start = requests.get(
            f"{database_service_base_url}/stations/{trip_station_start['station_id']}"
        ).json()
        station_end = requests.get(
            f"{database_service_base_url}/stations/{trip_station_end['station_id']}"
        ).json()
        data['tickets'].append({
            'id': ticket['id'],
            'station_start_name': station_start['name'],
            'station_end_name': station_end['name'],
            'time_dep': trip_station_start['time_dep']
        })
    return data

@app.route("/orders", methods=["POST"])
def create_order():
    station_start_id = request.json['station_start_id']
    station_end_id = request.json['station_end_id']
    trip_id = request.json['trip_id']
    seats = request.json['seats']
    user_id = request.json['user_id']
    
    station_start = requests.get(
        f"{database_service_base_url}/stations/{station_start_id}"
    ).json()
    station_end = requests.get(
        f"{database_service_base_url}/stations/{station_end_id}"
    ).json()
    trip_station_start = requests.get(
        f"{database_service_base_url}/trip-stations",
        params={"trip_id": trip_id, "station_id": station_start_id}
    ).json()[0]
    trip_station_end = requests.get(
        f"{database_service_base_url}/trip-stations",
        params={"trip_id": trip_id, "station_id": station_end_id}
    ).json()[0]
    trip = requests.get(
        f"{database_service_base_url}/trips/{trip_id}"
    ).json()
    train = requests.get(
        f"{database_service_base_url}/trains/{trip['train_id']}"
    ).json()
    line_items = []
    
    for seat_id in seats:
        seat = requests.get(
            f"{database_service_base_url}/seats/{seat_id}"
        ).json()
        carriage = requests.get(
            f"{database_service_base_url}/carriages/{seat['carriage_id']}"
        ).json()
        carriage_type = requests.get(
            f"{database_service_base_url}/carriage-types/{carriage['carriage_type_id']}"
        ).json()
        train = requests.get(
            f"{database_service_base_url}/trains/{carriage['train_id']}"
        ).json()
        name = f"{station_start['name']} - {station_end['name']}, Train {train['name']}, Carriage {carriage['num']}, Seat: {seat['num']}"
        line_items.append({
            'price_data': {
                'currency': 'uah',
                'unit_amount': (trip_station_end['price'] - trip_station_start['price']) * carriage_type['price_mod'],
                'product_data': {
                    'name': name,
                    'metadata': {
                        'user_id': user_id,
                        'seat_id': seat['id'],
                        'trip_station_start_id': trip_station_start['id'],
                        'trip_station_end_id': trip_station_end['id']
                    }
                },
            },
            'quantity': 1
        })
    checkout_session = stripe.checkout.Session.create(
        success_url=f"{frontend_service_base_url}/orders",
        cancel_url=f"{frontend_service_base_url}/seats?trip={trip['id']}&ctype={carriage_type['id']}&from={station_start['id']}&to={station_end['id']}",
        line_items=line_items,
        mode='payment'
    )
    return {'url': checkout_session.url}, 200

if __name__ == '__main__':
    serve(app, host='0.0.0.0', port=5004)