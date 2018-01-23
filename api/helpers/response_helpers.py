from flask import jsonify, request, g
from six import wraps

from api.models import User


def protected_route(f):
    @wraps(f)
    def func_wrapper(*args, **kwargs):
        bearer_token = request.headers.get("Authorization")
        if not bearer_token:
            response = jsonify({
                "message": "Token is missing"
            })
            response.status_code = 401
            return response

        token = bearer_token.replace("Bearer ", "")

        resp = User.decode_token(token)

        if isinstance(resp, int):
            user = User.query.filter_by(id=resp).first()
            if not user:
                response = jsonify({
                    "message": "User not found "
                })
                response.status_code = 404
                return response
            g.user = user
            return f(*args, **kwargs)
        else:
            response = jsonify({
                "message": resp
            })
            response.status_code = 401
            return response

    return func_wrapper


def validate_event(f):
    @wraps(f)
    def func_wrapper(*args, **kwargs):
        if not request.is_json and not request.get_json():
            return make_response(400, "You have not provided Valid Json Input")
        required_fields = ["name", "address", "start_date", "end_date", "description", "price", "category_id"]
        data = request.get_json()
        fields = set(required_fields)
        missing_fields = fields - set(data)
        if missing_fields:
            missing_fields = ', '.join(missing_fields)
            return make_response(400, "The following Required Field(s) are Missing: {}".format(missing_fields))
        empty_fields = []
        [empty_fields.append(field) for field in required_fields if not data[field] or len(str(data[field]).strip())<=0]
        if empty_fields:
            empty_fields = ', '.join(empty_fields)
            return make_response(400, "The following Field(s) are Empty: {}".format(empty_fields))
        return f(*args, **kwargs)
    return func_wrapper


def event_parser(event):
    new_event = {
        "id": event.id,
        "name": event.name,
        "address": event.address,
        "start_date": event.start_date,
        "end_date": event.end_date,
        "user_id": event.user.id,
        "price": event.price,
        "description": event.description,
        "category_id": event.category.id
    }
    return new_event


def user_parser(user):
    new_user = {
        "id": user.id,
        "name": user.name,
        "email": user.email,
    }
    return new_user


# helper function used to return the message when login fails
def failed_login():
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


def parse_list(list_type, data):
    """
    Helper function which will be responsible for converting(parsing) list of either User or Event models
    to list of dictionaries, caller will pass in string argument(data_type) with value of either
    "users" or "events" and data arguments and parsed dictionary will be returned
    :param list_type
    :param data
    :return parsed_dictionary:
    """
    if list_type == 'users':
        dict_users = []
        for user in data:
            dict_users.append(user_parser(user))
        return dict_users
    else:
        events_list = []
        for event in data:
            events_list.append(event_parser(event))
        return events_list
