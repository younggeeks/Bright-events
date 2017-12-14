import uuid

import os

from flask import Blueprint, request, jsonify, url_for
from flask_restplus import Api, Resource
from itsdangerous import URLSafeTimedSerializer
from werkzeug.security import generate_password_hash, check_password_hash
from api.models import User, BlacklistToken

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


@api.route("/logout")
class Logout(Resource):
    def post(self):
        bearer_token = request.headers.get("Authorization")
        if not bearer_token:
            response = jsonify({
                "message": "Token is missing from your header"
            })
            response.status_code = 401
            return response

        token = bearer_token.replace("Bearer ", "")
        decoded_token = User.decode_token(token)

        if isinstance(decoded_token, int):
            already_blacklisted = BlacklistToken.query.filter_by(token=token).first()

            if already_blacklisted:
                response = jsonify({
                    "message": "User is already signed out"
                })
                response.status_code = 401
                return response

            blacklist = BlacklistToken(token=token)
            blacklist.save()

            response = jsonify({
                "message": "Logout Successfully"
            })
            response.status_code = 200
            return response
        response = jsonify({
            "message": decoded_token
        })
        response.status_code = 200
        return response


@api.route("/reset")
class PasswordReset(Resource):
    def post(self):
        data = request.get_json()
        if "email" in data and data["email"] != "":
            user = User.query.filter_by(email=data["email"]).first()
            if not user:
                response = jsonify({
                    "message": "Email not found , Password reset Failed"
                })
                response.status_code = 404
                return response

            password_reset_serializer = URLSafeTimedSerializer(os.getenv("SECRET"))
            reset_url = url_for("auth.password_reset_token",
                                token=password_reset_serializer.dumps(data["email"],
                                                                      salt=os.getenv("RESET_SALT")),
                                _external=True)

            response = jsonify({
                "message": "Password Reset Link Successfully Generated",
                "link": reset_url
            })
            response.status_code = 400
            return response
        else:
            response = jsonify({
                "message": "Password Reset failed, Please check your input"
            })
            response.status_code = 400
            return response


@api.route("/reset-password/<token>")
class PasswordResetToken(Resource):
    def get(self, token):
        if token:
            try:
                password_reset_serializer = URLSafeTimedSerializer(os.getenv("SECRET"))
                password_reset_serializer.loads(token, salt=os.getenv("RESET_SALT"), max_age=3600)

                response = jsonify({
                    "message": "Password Reset Link Verified Successfully",
                    "verified": True,
                    "token": token
                })
                response.status_code = 400
                return response
            except Exception as e:
                response = jsonify({
                    "message": "Password Reset Link is invalid, or Expired"
                })
                response.status_code = 400
                return response

        else:
            response = jsonify({
                "message": "Password Reset failed, Please check your input"
            })
            response.status_code = 400
            return response


@api.route("/reset-password/<token>")
class PasswordResetToken(Resource):
    def get(self, token):
        if token:
            try:
                password_reset_serializer = URLSafeTimedSerializer(os.getenv("SECRET"))
                password_reset_serializer.loads(token, salt=os.getenv("RESET_SALT"), max_age=3600)

                response = jsonify({
                    "message": "Password Reset Link Verified Successfully",
                    "verified": True,
                    "token": token
                })
                response.status_code = 200
                return response
            except Exception as e:
                response = jsonify({
                    "message": "Password Reset Link is invalid, or Expired"
                })
                response.status_code = 400
                return response

        else:
            response = jsonify({
                "message": "Password Reset failed, Please check your input"
            })
            response.status_code = 400
            return response

    def post(self, token):
        data = request.get_json()
        if token:
            try:
                password_reset_serializer = URLSafeTimedSerializer(os.getenv("SECRET"))
                email = password_reset_serializer.loads(token, salt=os.getenv("RESET_SALT"), max_age=3600)

                if "password" in data and "password_confirmation" in data:
                    if data["password"] != "" and data["password_confirmation"] != "":
                        if data["password"] == data["password_confirmation"]:
                            hashed_password = generate_password_hash(data["password"])
                            user = User.query.filter_by(email=email).first()
                            user.password = hashed_password
                            user.save()
                            response = jsonify({
                                "message": "Password Reset Successfully"
                            })
                            response.status_code = 200
                            return response

                        else:
                            response = jsonify({
                                "message": "Password and Password confirmation do not match"
                            })
                            response.status_code = 400
                            return response
                    else:
                        response = jsonify({
                            "message": "Password Reset Failed, All fields are required"
                        })
                        response.status_code = 400
                        return response
                else:
                    response = jsonify({
                        "message": "Password Reset Failed, Please check your input"
                    })
                    response.status_code = 400
                    return response
            except Exception as e:
                response = jsonify({
                    "message": "Password Reset Link is invalid, or Expired"
                })
                response.status_code = 400
                return response

        else:
            response = jsonify({
                "message": "Password Reset failed, Please check your input"
            })
            response.status_code = 400
            return response
