from flask import Flask, render_template, request, redirect
from waitress import serve
from dotenv import load_dotenv
from connection import *
from database import *
from command import *

load_dotenv()

public_url = f"{os.getenv('DOMAIN')}"

engine = create_engine(
    f"{os.getenv('DATABASE_TYPE')}+{os.getenv('DATABASE_API')}://{os.getenv('USER')}:{os.getenv('PASSWORD')}@{os.getenv('HOST')}/{os.getenv('DATABASE')}",
    pool_size=5,
    echo=True
)

app = Flask(__name__, template_folder='templates', static_folder='static')

app.secret_key = b'yb4No3!w2NX528'

with app.app_context():
    app.config['engine'] = engine
    app.config['public_url'] = public_url


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/stations")
def stations():
    result = SearchStationsCommand(request).execute()
    return result


@app.route("/signup", methods=['POST'])
def signup():
    result = SignupCommand(request).execute()
    return result


@app.route("/login", methods=['POST'])
def login():
    result = LoginCommand(request).execute()
    return result


@app.route("/logout", methods=['GET'])
def logout():
    result = LogoutCommand().execute()
    return result


@app.route("/profile", methods=['GET', 'PATCH'])
def profile():
    if request.method == 'GET':
        result = ReadProfileCommand().execute()
        
    if request.method == 'PATCH':
        result = UpdateProfileCommand(request).execute()
    
    return result


@app.route("/admin", methods=['GET'])
def admin():
    result = ReadUsersCommand().execute()
    return result


@app.route("/search", methods=['GET'])
def search():
    result = SearchTicketsCommand(request).execute()
    return result


@app.route("/seats", methods=['GET'])
def seats():
    result = SearchSeatsCommand(request).execute()
    return result


@app.route("/orders", methods=['GET', 'POST'])
def orders():
    if request.method == 'GET':
        result = ReadOrdersCommand().execute()

    if request.method == 'POST':
        result = CreateOrderCommand(request).execute()
    
    return result


@app.route("/payment-completed", methods=['POST'])
def payment_completed():
    result = CompleteOrderCommand(request).execute()
    return result


@app.route("/verify", methods=['GET'])
def verify():
    result = VerifyOrderCommand(request).execute()
    return result


@app.route("/qrcode", methods=['GET'])
def generate_qrcode():
    result = GenerateQrcodeCommand(request).execute()
    return result
    

@app.errorhandler(404)
def handle_404(e):
    return redirect(url_for('index'))


@app.errorhandler(500)
def handle_500(e):
    return redirect(url_for('index'))


if __name__ == '__main__':
    serve(app, host='0.0.0.0', port=5000)