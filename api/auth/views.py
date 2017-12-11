import uuid

import os

import jwt
from flask import Blueprint, request, jsonify
from flask_restplus import Api, Resource
from werkzeug.security import generate_password_hash, check_password_hash
from api.models import User

auth = Blueprint("auth", __name__, url_prefix="/api/v1/auth")

api = Api(auth, catch_all_404s=True)


@api.route("/register")
class Register(Resource):
    """
    New User Registration
    """

    def post(self):
        data = request.get_json()
        new_user = User.query.filter_by(email=data["email"]).first()
        if not new_user:
            try:
                hashed_password = generate_password_hash(data["password"])
                user = User(public_id=uuid.uuid4(), name=data["name"], email=data["email"], password=hashed_password)
                token = user.encode_token()
                user.save()
                response = jsonify({
                    "message": "Successfully Registered",
                    "token": token.decode('UTF-8')
                })
                return response
            except Exception as e:
                response = jsonify({
                    "message": "User Registration Failed"
                })
                response.status_code = 401
                return response
        else:
            response = jsonify({
                "message": "User Already Exists, Please Login"
            })
            response.status_code = 401
            return response


@api.route("/login")
class Login(Resource):
    """User Authentication using Email and password"""

    def post(self):
        credentials = request.get_json()
        if "email" in credentials and "password" in credentials:
            if credentials["email"] == "" or credentials["password"] == "":
                response = jsonify({
                    "message": "Email and password fields are required to login"
                })
                response.status_code = 422
                return response
            user = User.query.filter_by(email=credentials["email"]).first()

            if not user:
                response = jsonify({
                    "message": "Wrong Combination of Email and password, Login Failed"
                })
                response.status_code = 422
                return response
            if check_password_hash(user.password, credentials["password"]):
                token = user.encode_token()
                response = jsonify({
                    "message": "Login successfully",
                    "token": token.decode("UTF-8")
                })
                response.status_code = 200
                return response

            response = jsonify({
                "message": "Login Failed, Please check your input"
            })
            response.status_code = 422  
            return response

        else:
            response = jsonify({
                "message": "Login Failed, Please check your input"
            })
            response.status_code = 400
            return response
