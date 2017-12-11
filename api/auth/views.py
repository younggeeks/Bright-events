import uuid

import os
from flask import Blueprint, request, jsonify
from flask_restplus import Api, Resource
from werkzeug.security import generate_password_hash
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
