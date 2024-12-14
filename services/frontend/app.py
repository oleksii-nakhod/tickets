from flask import Flask, render_template, request, redirect, make_response, url_for, jsonify
from waitress import serve
import requests
import logging
import os
import time
import redis
from queue import Queue
import threading
from functools import wraps

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

search_service_host = os.getenv('SEARCH_SERVICE_HOST')
search_service_port = os.getenv('SEARCH_SERVICE_PORT')
search_service_base_url = f"http://{search_service_host}:{search_service_port}"

auth_service_host = os.getenv('AUTH_SERVICE_HOST')
auth_service_port = os.getenv('AUTH_SERVICE_PORT')
auth_service_base_url = f"http://{auth_service_host}:{auth_service_port}"

order_service_host = os.getenv('ORDER_SERVICE_HOST')
order_service_port = os.getenv('ORDER_SERVICE_PORT')
order_service_base_url = "http://kong-kong-proxy"

logger.info(f"Search service: {search_service_base_url}")
logger.info(f"Auth service: {auth_service_base_url}")
logger.info(f"Order service: {order_service_base_url}")


app = Flask(__name__, template_folder='templates', static_folder='static')
redis_client = redis.Redis(host='redis', port=6379)

RATE_LIMIT = 4
WINDOW_SIZE = 60
request_queue = Queue()

app.secret_key = b'yb4No3!w2NX528'

def process_queue():
    while True:
        if not request_queue.empty():
            pod_id = get_pod_id()
            current_time = int(time.time())
            key = f"requests:{pod_id}:{current_time // WINDOW_SIZE}"
            count = redis_client.get(key)
            count = int(count) if count else 0
            
            if count < RATE_LIMIT:
                callback = request_queue.get()
                callback()
                
                pipe = redis_client.pipeline()
                pipe.incr(key)
                pipe.expire(key, WINDOW_SIZE)
                pipe.execute()
        
        time.sleep(1)

queue_thread = threading.Thread(target=process_queue, daemon=True)
queue_thread.start()

def get_pod_id():
    return os.environ.get('POD_NAME', 'unknown')

def rate_limit_with_queue(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        pod_id = get_pod_id()
        current_time = int(time.time())
        key = f"requests:{pod_id}:{current_time // WINDOW_SIZE}"
        count = redis_client.get(key)
        count = int(count) if count else 0
        
        if count >= RATE_LIMIT:
            future_response = {}
            def callback():
                try:
                    result = f(*args, **kwargs)
                    future_response['result'] = result
                except Exception as e:
                    future_response['error'] = str(e)
            
            request_queue.put(callback)
            return jsonify({
                "status": "queued",
                "message": "Request has been queued due to rate limit",
                "retry_after": WINDOW_SIZE - (current_time % WINDOW_SIZE)
            }), 429
        
        pipe = redis_client.pipeline()
        pipe.incr(key)
        pipe.expire(key, WINDOW_SIZE)
        pipe.execute()
        
        try:
            return f(*args, **kwargs)
        except Exception as e:
            logger.error(f"Error in rate-limited function: {str(e)}")
            return jsonify({"error": str(e)}), 500
            
    return decorated_function

@app.route("/")
def index():
    query = request.args.get('q')
    if query:
        stations = requests.get(
            f"{search_service_base_url}/stations",
            params={'q': query}
        ).json()
        return stations
    else:
        return render_template("index.html")

@app.route("/search", methods=['GET'])
def search():
    from_station = request.args.get('from')
    to_station = request.args.get('to')
    depart_date = request.args.get('depart')
    logger.info(f"Search parameters: {from_station}, {to_station}, {depart_date}")
    trips = requests.get(
        f"{search_service_base_url}/trips",
        params={
            'from_station': from_station,
            'to_station': to_station,
            'depart_date': depart_date
        }
    ).json()
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

@app.route("/login", methods=['POST'])
def login():
    logger.info(f"Login request: {request.json}")
    response = requests.post(
        f"{auth_service_base_url}/login",
        json={
            'email': request.json['email'],
            'password': request.json['password']
        }
    )
    auth_data = response.json()
    resp = make_response(auth_data, response.status_code)
    
    if response.ok:
        resp.set_cookie(
            'token',
            auth_data.get('access_token'),
            max_age=86400
        )
        resp.set_cookie(
            'user_name',
            auth_data.get('user_name'),
            max_age=86400
        )
    
    return resp
    
@app.route("/signup", methods=['POST'])
def signup():
    response = requests.post(
        f"{auth_service_base_url}/signup",
        json={
            'name': request.json['name'],
            'email': request.json['email'],
            'password': request.json['password']
        }
    )
    return response.json(), response.status_code

@app.route("/logout", methods=['POST'])
def logout():
    resp = make_response()
    resp.delete_cookie('token', path='/')
    resp.delete_cookie('user_name', path='/')
    return resp

@app.route("/orders", methods=['GET', 'POST'])
@rate_limit_with_queue
def orders():
    access_token = request.cookies.get('token')
    user = None
    if access_token:
        user = requests.get(
            f"{auth_service_base_url}/verify",
            headers={
                'Authorization': f"Bearer {access_token}"
            }
        ).json()
    else:
        return redirect(url_for('index'), 401)
    logger.info(f"User: {user}")
    
    if request.method == 'GET':
        tickets = requests.get(
            f"{order_service_base_url}/orders",
            headers={
                'apikey': "test-key"
            },
            params={'user_id': user['id']},
        )
        tickets_data = tickets.json()
        logger.info(tickets.headers)
        logger.info(tickets_data)
        return render_template("orders.html", data=tickets_data)
    elif request.method == 'POST':
        response = requests.post(
            f"{order_service_base_url}/orders",
            headers={
                'apikey': "test-key"
            },
            json={
                'user_id': user['id'],
                'station_start_id': request.json['station_start_id'],
                'station_end_id': request.json['station_end_id'],
                'trip_id': request.json['trip_id'],
                'seats': request.json['seats']
            }
        )
        return response.json(), response.status_code


@app.errorhandler(404)
def handle_404(e):
    return redirect(url_for('index'))


@app.errorhandler(500)
def handle_500(e):
    return redirect(url_for('index'))

if __name__ == '__main__':
    serve(app, host='0.0.0.0', port=5000)