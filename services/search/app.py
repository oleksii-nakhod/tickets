from flask import Flask, request
from waitress import serve
import requests
import datetime
import logging
import os

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

database_service_host = os.getenv('DATABASE_SERVICE_HOST')
database_service_port = os.getenv('DATABASE_SERVICE_PORT')
database_service_base_url = f'http://{database_service_host}:{database_service_port}'

app = Flask(__name__)

@app.route("/stations")
def stations():
    query = request.args.get('q')
    stations = requests.get(
        f"{database_service_base_url}/stations",
        params={'q': query}
    ).json()
    return stations

@app.route("/trips")
def trips():
    from_station = request.args.get('from_station')
    to_station = request.args.get('to_station')
    depart_date = request.args.get('depart_date')
    logger.info(f"Search parameters: {from_station}, {to_station}, {depart_date}")
    response = requests.get(
        f"{database_service_base_url}/trips",
        params={
            'station_start': from_station,
            'station_end': to_station,
            'depart_date': depart_date
        }
    )
    trips = response.json()
    logger.info(f"Trips: {trips}")
    data = {'trips': []}
    for trip in trips:
        response = requests.get(
            f'{database_service_base_url}/carriages',
            params={'trip': trip['id']}
        )
        carriage_seats = response.json()
        carriage_seats_formatted = []
        for carriage_seat in carriage_seats:
            carriage_seats_formatted.append(
                {
                    'carriage_id': carriage_seat['carriage_type_id'],
                    'carriage_type': carriage_seat['carriage_type_name'],
                    'seat_price': int(trip['price'] * carriage_seat['price_mod']),
                    'seat_quantity': carriage_seat['count']
                }
            )
        if not carriage_seats_formatted:
            continue
        response = requests.get(
            f"{database_service_base_url}/trains/{trip['id']}"
        )
        train = response.json()
        time_dep = datetime.datetime.strptime(trip['time_dep'], '%Y-%m-%dT%H:%M:%SZ')
        time_arr = datetime.datetime.strptime(trip['time_arr'], '%Y-%m-%dT%H:%M:%SZ')
        duration_seconds = (time_arr - time_dep).total_seconds()
        hours = int(duration_seconds//3600)
        minutes = int((duration_seconds - hours * 3600)//60)
        duration = f'{hours} h {minutes} min'
        data['trips'].append({
            'id': trip['id'],
            'train_id': train['id'],
            'train_name': train['name'],
            'time_dep': trip['time_dep'],
            'time_arr': trip['time_arr'],
            'time_dep_pretty': time_dep.strftime('%H:%M'),
            'time_arr_pretty': time_arr.strftime('%H:%M'),
            'duration_pretty': duration,
            'base_price': trip['price'],
            'carriage_seats': carriage_seats_formatted
        })
    response = requests.get(
        f'{database_service_base_url}/stations/{from_station}'
    )
    station_start = response.json()
    response = requests.get(
        f'{database_service_base_url}/stations/{to_station}'
    )
    station_end = response.json()
    data['station_start_name'] = station_start['name']
    data['station_start_id'] = station_start['id']
    data['station_end_name'] = station_end['name']
    data['station_end_id'] = station_end['id']
    data['depart_date'] = datetime.datetime.strptime(depart_date, '%Y-%m-%d').strftime('%a, %b %d %Y')
    return data

@app.route("/seats")
def seats():
    trip_id = request.args.get('trip_id')
    ctype = request.args.get('ctype')
    from_station = request.args.get('from_station')
    to_station = request.args.get('to_station')
    train = requests.get(
        f"{database_service_base_url}/trains",
        params={
            'trip': trip_id
        }
    ).json()
    carriages = requests.get(
        f"{database_service_base_url}/seats",
        params={
            'trip': trip_id,
            'train': train['id'],
            'ctype': ctype,
            'from_station': from_station,
            'to_station': to_station
        }
    ).json()
    station_start = requests.get(
        f"{database_service_base_url}/stations/{from_station}"
    ).json()
    station_end = requests.get(
        f"{database_service_base_url}/stations/{to_station}"
    ).json()
    trip_extra_info = requests.get(
        f"{database_service_base_url}/trip-stations/info",
        params={
            'trip': trip_id,
            'station_start': from_station,
            'station_end': to_station
        }
    ).json()
    carriage_type = requests.get(
        f"{database_service_base_url}/carriage-types/{ctype}"
    ).json()
    time_dep = datetime.datetime.strptime(trip_extra_info['time_dep'], '%Y-%m-%dT%H:%M:%SZ')
    time_arr = datetime.datetime.strptime(trip_extra_info['time_arr'], '%Y-%m-%dT%H:%M:%SZ')
    data = {
        'carriages': carriages,
        'trip_id': trip_id,
        'train_id': train['id'],
        'train_name': train['name'],
        'station_start_name': station_start['name'],
        'station_start_id': station_start['id'],
        'station_end_name': station_end['name'],
        'station_end_id': station_end['id'],
        'carriage_type_id': ctype,
        'carriage_type_name': carriage_type['name'],
        'price': int(trip_extra_info['price'] * carriage_type['price_mod']),
        'depart_date': time_dep.strftime('%Y-%m-%d'),
        'depart_date_pretty': time_dep.strftime('%a, %b %d %Y'),
        'time_dep_pretty': time_dep.strftime('%H:%M'),
        'time_arr_pretty': time_arr.strftime('%H:%M')
    }
    return data

if __name__ == '__main__':
    serve(app, host='0.0.0.0', port=5002)