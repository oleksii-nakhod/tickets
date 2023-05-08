from flask import current_app, session, jsonify, render_template, url_for
from database.entity.user import *
import datetime

class SearchService:
    def search_tickets(self, from_station, to_station, depart_date):
        trip_table = current_app.config['tables']['trip']
        carriage_table = current_app.config['tables']['carriage']
        train_table = current_app.config['tables']['train']
        station_table = current_app.config['tables']['station']
        trips = trip_table.find(from_station, to_station, depart_date)
        data = {'trips': []}
        for trip in trips:
            carriage_seats = carriage_table.find(trip[0])
            if not carriage_seats:
                continue
            train = train_table.read(trip[0])
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
        return render_template('search.html', data=data)
    
    def search_seats(self, trip, ctype, from_station, to_station):
        train_table = current_app.config['tables']['train']
        seat_table = current_app.config['tables']['seat']
        trip_station_table = current_app.config['tables']['trip_station']
        station_table = current_app.config['tables']['station']
        carriage_table = current_app.config['tables']['carriage']
        carriage_type_table = current_app.config['tables']['carriage_type']
        train = train_table.find(trip)
        carriages = seat_table.find(trip, train.id, ctype, from_station, to_station)
        station_start = station_table.read(from_station)
        station_end = station_table.read(to_station)
        trip_extra_info = trip_station_table.find(trip, from_station, to_station)
        carriage_type = carriage_type_table.read(ctype)
        data = {
            'carriages': carriages,
            'trip_id': trip,
            'train_id': train.id,
            'train_name': train.name,
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
        return render_template('seats.html', data=data)
    
    def search_stations(self, query):
        station_table = current_app.config['tables']['station']
        stations = station_table.find(query)
        return jsonify([station.__dict__ for station in stations])