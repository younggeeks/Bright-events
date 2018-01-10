from flask import jsonify


def event_parser(event):
    new_event = {
        "id": event.id,
        "name": event.name,
        "address": event.address,
        "start_date": event.start_date,
        "end_date": event.end_date,
        "user": event.user,
        "price": event.price,
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


def failed_login():
    """
    helper function used to return the message when login fails
    :return:
    """
    response = jsonify({"message": "Wrong Combination of Username and Password"})
    response.status_code = 401
    return response


def make_response(status, message):
    """
    helper function used to return the message when request fails fails
    :param status:
    :param message:
    :return:
    """
    response = jsonify({"message": "{}".format(message)})
    response.status_code = status
    return response
