import uuid

import os

from flask import Blueprint, request, jsonify, url_for
from flask_restful import Api, Resource

from itsdangerous import URLSafeTimedSerializer
from werkzeug.security import generate_password_hash, check_password_hash

from api.helpers.response_helpers import make_response
from api.models import User, BlacklistToken

auth = Blueprint("auth", __name__, url_prefix="/api/v1/auth")

api = Api(auth, catch_all_404s=True)


class Register(Resource):
    """
    New User Registration
    """

    def post(self):
        data = request.get_json()
        if "email" not in data or "name" not in data or "password" not in data:
            return make_response(400, "Registration Failed, Please check your input")

        new_user = User.query.filter_by(email=data["email"]).first()
        if not new_user:
            hashed_password = generate_password_hash(data["password"])
            user = User(public_id=uuid.uuid4(), name=data["name"], email=data["email"], password=hashed_password)
            token = user.encode_token()
            user.save()
            response = jsonify({
                "message": "Successfully Registered",
                "token": token.decode('UTF-8')
            })
            response.status_code = 201
            return response
        else:
            return make_response(401, "User Already Exists, Please Login")


class Login(Resource):
    """User Authentication using Email and password"""

    def post(self):
        credentials = request.get_json()
        if "email" in credentials and "password" in credentials:
            if credentials["email"] == "" or credentials["password"] == "":
                return make_response(400, "Email and password fields are required to login")

            user = User.query.filter_by(email=credentials["email"]).first()
            if not user:
                return make_response(401, "No Account is associated with Email {}, Login Failed".format(
                    credentials["email"]))

            if check_password_hash(user.password, credentials["password"]):
                token = user.encode_token()
                response = jsonify({
                    "message": "Login successful",
                    "token": token.decode("UTF-8")
                })
                response.status_code = 200
                return response
            else:
                return make_response(401, "Wrong Combination of Email and password, Login Failed")

        else:
            return make_response(400, "Login Failed, Please check your input")


class Logout(Resource):
    def post(self):
        bearer_token = request.headers.get("Authorization")
        if not bearer_token:
            return make_response(401, "Token is missing from your header")

        token = bearer_token.replace("Bearer ", "")
        decode_response = User.decode_token(token)

        if isinstance(decode_response, int):
            already_blacklisted = BlacklistToken.query.filter_by(token=token).first()
            if already_blacklisted:
                return make_response(401, "User is already signed out")

            blacklist = BlacklistToken(token=token)
            blacklist.save()

            response = jsonify({
                "message": "Logout Successful"
            })
            response.status_code = 200
            return response
        return make_response(400, decode_response)


class PasswordResetLink(Resource):
    def post(self):
        data = request.get_json()
        if "email" in data and data["email"] != "":
            user = User.query.filter_by(email=data["email"]).first()
            if not user:
                return make_response(404, "Email not found , Password reset Failed")

            password_reset_serializer = URLSafeTimedSerializer(os.getenv("SECRET"))
            reset_url = url_for("auth.passwordresettoken",
                                token=password_reset_serializer.dumps(data["email"],
                                                                      salt=os.getenv("RESET_SALT")),
                                _external=True)

            response = jsonify({
                "message": "Password Reset Link Successfully Generated",
                "link": reset_url
            })
            response.status_code = 200
            return response
        else:
            return make_response(400, "Password Reset failed, Please check your input")


class PasswordResetToken(Resource):
    def get(self, token):
        try:
            password_reset_serializer = URLSafeTimedSerializer(os.getenv("SECRET"))
            email = password_reset_serializer.loads(token, salt=os.getenv("RESET_SALT"), max_age=3600)
            token = password_reset_serializer.dumps(email, salt=os.getenv("RESET_SALT_VERIFY"))
            response = jsonify({
                "message": "Password Reset Link Verified Successfully",
                "verified": True,
                "token": token
            })
            response.status_code = 200
            return response
        except Exception as e:
            return make_response(400, "Password Reset Link is invalid, or Expired")


class PasswordResetChangePassword(Resource):
    def get(self, token):
        password_reset_serializer = URLSafeTimedSerializer(os.getenv("SECRET"))
        password_reset_serializer.loads(token, salt=os.getenv("RESET_SALT_VERIFY"), max_age=3600)

        response = jsonify({
            "message": "Password Reset Link Verified Successfully",
            "verified": True,
            "token": token
        })
        response.status_code = 200
        return response

    def post(self, token):
        data = request.get_json()

        password_reset_serializer = URLSafeTimedSerializer(os.getenv("SECRET"))
        email = password_reset_serializer.loads(token, salt=os.getenv("RESET_SALT_VERIFY"), max_age=3600)
        if data:
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
                        return make_response(401, "Password and Password confirmation do not match")

                else:
                    return make_response(400, "Password Reset Failed, All fields are required")

            else:
                return make_response(400, "Password Reset Failed, Please check your input")

        else:
            return make_response(400, "Password Reset Failed, Please check your input")


api.add_resource(Register, "/register")
api.add_resource(Login, "/login")
api.add_resource(Logout, "/logout")
api.add_resource(PasswordResetLink, "/reset")
api.add_resource(PasswordResetToken, "/reset-password/verify/<token>")
api.add_resource(PasswordResetChangePassword, "/reset-password/<token>")
