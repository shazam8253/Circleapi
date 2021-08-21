from utils import db_write, generate_hash, generate_salt, validate_user, validate_user_input
from flask import Blueprint, request, Response, jsonify

authentication = Blueprint("authentication", __name__)

@authentication.route("/register", methods=["POST"])
def register_user():
    user_email = request.json["email"]
    user_password = request.json["password"]
    user_confirm_password = request.json["confirm_password"]
    user_username = request.json["username"]
    user_firstname = request.json["firstname"]
    user_lastname = request.json["lastname"]

    if user_password == user_confirm_password and validate_user_input(
        "authentication", email=user_email, password=user_password
    ):
        password_salt = generate_salt()
        password_hash = generate_hash(user_password, password_salt)
        if db_write(
            """INSERT INTO circle.Users (username, password_hash, password_salt, email, firstname, lastname) VALUES (%s, %s, %s, %s, %s, %s)""",
            (user_username, password_hash , password_salt, user_email, user_firstname, user_lastname),
        ):
            # Registration Successful
            return Response(status=201)
        else:
            # Registration Failed
            return Response(status=409)
    else:
        # Registration Failed
        return Response(status=400)

@authentication.route("/login", methods=["POST"])
def login_user():
    user_email = request.json["email"]
    user_password = request.json["password"]

    user_token = validate_user(user_email, user_password)

    if user_token:
        return jsonify({"jwt_token": user_token})
    else:
        return Response(status=250)