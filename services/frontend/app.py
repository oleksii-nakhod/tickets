from flask import Flask, render_template, request, redirect
from waitress import serve
import requests
import logging
import os

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

search_service_host = os.getenv('SEARCH_SERVICE_HOST')
search_service_port = os.getenv('SEARCH_SERVICE_PORT')
search_service_base_url = f"http://{search_service_host}:{search_service_port}"

app = Flask(__name__, template_folder='templates', static_folder='static')

app.secret_key = b'yb4No3!w2NX528'

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/search", methods=['GET'])
def search():
    from_station = request.args.get('from')
    to_station = request.args.get('to')
    depart_date = request.args.get('depart')
    logger.info(f"Search parameters: {from_station}, {to_station}, {depart_date}")
    response = requests.get(
        f"{search_service_base_url}/trips",
        params={
            'from_station': from_station,
            'to_station': to_station,
            'depart_date': depart_date
        }
    )
    trips = response.json()
    return render_template("search.html", data=trips)

@app.route("/seats", methods=['GET'])
def seats():
    trip_id = request.args.get('trip')
    ctype = request.args.get('ctype')
    from_station = request.args.get('from')
    to_station = request.args.get('to')
    response = requests.get(
        f"{search_service_base_url}/seats",
        params={
            'trip_id': trip_id,
            'ctype': ctype,
            'from_station': from_station,
            'to_station': to_station
        }
    )
    seats = response.json()
    return render_template("seats.html", data=seats)

if __name__ == '__main__':
    serve(app, host='0.0.0.0', port=5000)