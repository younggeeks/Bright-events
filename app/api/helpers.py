
from flask import jsonify


def event_parser(event):
    new_event = {
        "id": event.id,
        "name": event.name,
        "address": event.address,
        "start_date": event.start_date,
        "end_date": event.end_date,
        "user": event.user,
        "description": event.description,
        "category": event.category
    }
    return new_event


def user_parser(user):
    new_user = {
        "id": user.id,
        "full_name": user.full_name,
        "email": user.email,
        "password": user.password
    }
    return new_user


# helper function used to return the message when login fails
def failed_login():
    response = jsonify({"message": "Wrong Combination of Username and Password"})
    response.status_code = 401
    return response
