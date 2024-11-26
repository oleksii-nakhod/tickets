from flask import Flask, render_template, request, redirect
from flask_jwt_extended import create_access_token
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required
from flask_jwt_extended import JWTManager
from waitress import serve
import requests
import logging
import os

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

database_service_host = os.getenv('DATABASE_SERVICE_HOST')
database_service_port = os.getenv('DATABASE_SERVICE_PORT')
database_service_base_url = f"http://{database_service_host}:{database_service_port}"

app = Flask(__name__)

app.config["JWT_SECRET_KEY"] = "super-secret"
jwt = JWTManager(app)

@app.route("/login", methods=["POST"])
def login():
    email = request.json.get("email", None)
    password = request.json.get("password", None)

    users = requests.get(
        f"{database_service_base_url}/users",
        params={"email": email, "password": password}
    ).json()
    if not users:
        return {"msg": "Bad username or password"}, 401

    access_token = create_access_token(identity=email)
    return {"access_token": access_token, "user_name": users[0]['name']}, 200

@app.route("/signup", methods=["POST"])
def signup():
    name = request.json.get("name", None)
    email = request.json.get("email", None)
    password = request.json.get("password", None)

    users = requests.get(
        f"{database_service_base_url}/users",
        params={"email": email}
    ).json()
    if users:
        return {'msg': 'This email address is already registered. If that\'s you, please log in instead.'}, 409

    response = requests.post(
        f"{database_service_base_url}/users",
        json={"name": name, "email": email, "password": password}
    )
    return response.json(), response.status_code

@app.route("/verify", methods=["GET"])
@jwt_required()
def verify():
    email = get_jwt_identity()
    users = requests.get(
        f"{database_service_base_url}/users",
        params={"email": email}
    ).json()
    return users[0], 200

if __name__ == '__main__':
    serve(app, host='0.0.0.0', port=5003)