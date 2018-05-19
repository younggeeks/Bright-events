import uuid

import os

from flask import Blueprint, request, jsonify, url_for, current_app, render_template
from flask_cors import CORS
from flask_mail import Message, Mail
from flask_restful import Api, Resource
from flask_restful.utils import cors

from itsdangerous import URLSafeTimedSerializer, BadSignature
from werkzeug.security import generate_password_hash, check_password_hash

from api.helpers.response_helpers import make_response, validate_inputs
from api.helpers.tests_dummy_data import required_user_fields, required_credentials_fields, required_new_password_fields
from api.models import User, BlacklistToken

auth = Blueprint("auth", __name__, url_prefix="/api/v1/auth")
CORS(auth)
api = Api(auth, catch_all_404s=True)


class Register(Resource):
    """
    New User Registration
    """

    @validate_inputs(required_user_fields)
    def post(self):
        data = request.get_json()
        new_user = User.query.filter_by(email=data["email"]).first()
        if not new_user:
            hashed_password = generate_password_hash(data["password"])
            user = User(public_id=uuid.uuid4(), name=data["name"], email=data["email"], password=hashed_password)
            user.save()
            response = jsonify({
                "message": "Successfully Registered"
            })
            response.status_code = 201
            return response
        else:
            return make_response(401, "User Already Exists, Please Login")


class Login(Resource):
    """User Authentication using Email and password"""

    @validate_inputs(required_credentials_fields)
    def post(self):
        credentials = request.get_json()
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


class Logout(Resource):
    """Authenticated Users can Destroy their token to indicate logging  out"""

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
    """User enters their email and resent link is returned as a feedback for them to reset"""

    def post(self):
        mail = Mail(current_app)
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

            # new_url = url_for("http://localhost:3000/change-password",  token=password_reset_serializer.dumps(data["email"],
            #                                                           salt=os.getenv("RESET_SALT")),
            #                     _external=True)
            salt = os.getenv("RESET_SALT")
            app_url = os.getenv("FRONTEND_URL")
            token = password_reset_serializer.dumps(data["email"], salt)
            url = "{}/change-password/{}".format(app_url, token)
            msg = Message('Hello ', sender="Bright Events", recipients=[data["email"]])
            msg.body = "Please click {} To reset your password".format(url)
            msg.html = render_template('reset.html', username=user.name, url=url)
            mail.send(msg)
            response = jsonify({"success": True})
            response.status_code = 200
            return response
        else:
            return make_response(400, "Email field is required, Password Reset failed")


class PasswordResetToken(Resource):
    """Once User clicks on the link that was sent to them  we verify to see the validity of the link"""

    def get(self, token):
        try:
            password_reset_serializer = URLSafeTimedSerializer(os.getenv("SECRET"))
            email = password_reset_serializer.loads(token, salt=os.getenv("RESET_SALT"), max_age=14400)
            token = password_reset_serializer.dumps(email, salt=os.getenv("RESET_SALT_VERIFY"))
            response = jsonify({
                "message": "Password Reset Link Verified Successfully",
                "verified": True,
                "token": token
            })
            response.status_code = 200
            return response
        except BadSignature as e:
            print(e.message)
            return make_response(400, "Password Reset Link is invalid")


class PasswordResetChangePassword(Resource):
    """User can now enter their new password and change their password"""

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

    @validate_inputs(required_new_password_fields)
    def post(self, token):
        data = request.get_json()
        password_reset_serializer = URLSafeTimedSerializer(os.getenv("SECRET"))
        email = password_reset_serializer.loads(token, salt=os.getenv("RESET_SALT_VERIFY"), max_age=3600)
        hashed_password = generate_password_hash(data["password"])
        user = User.query.filter_by(email=email).first()
        user.password = hashed_password
        user.save()
        response = jsonify({
            "message": "Password Reset Successfully"
        })
        response.status_code = 200
        return response


api.add_resource(Register, "/register")
api.add_resource(Login, "/login")
api.add_resource(Logout, "/logout")
api.add_resource(PasswordResetLink, "/reset")
api.add_resource(PasswordResetToken, "/reset-password/verify/<token>")
api.add_resource(PasswordResetChangePassword, "/reset-password/<token>")
