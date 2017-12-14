from functools import wraps

from flask import Blueprint, request, jsonify, g
from flask_restplus import Api, Resource

events = Blueprint("events", __name__, url_prefix="/api/v1/events")


api = Api(events, version='1.0', title='Bright Events API',
          description='Awesome Api for managing events', catch_all_404s=True, doc=True
          )

from api.models import Event, User
from api import response_helpers


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


@api.route("")
@api.doc
class EventList(Resource):
    def get(self):
        all_events = Event.query.all()
        print(response_helpers.event_parser(all_events[0]))
        response = jsonify({
            "message": "Events Retrieved Successfully",
            "events": response_helpers.parse_list("events", all_events)
        })
        response.status_code = 200
        return response

    @protected_route
    def post(self):
        data = request.get_json()

        if "name" in data and "address" in data and "start_date" in data and "end_date" in data and "description" \
                in data and "price" in data and "category_id" in data:
            event = Event.query.filter_by(name=data["name"]).first()
            if event:
                response = jsonify({"message": "Event name must be unique"})
                response.status_code = 400
                return response
            else:
                new_event = Event(name=data["name"], address=data["address"], start_date=data["start_date"],
                                  end_date=data["end_date"], description=data["description"], price=data["price"],
                                  category_id=data["category_id"])
                user = g.user
                user.events.append(new_event)
                user.save()
                response = jsonify({"message": "Event Registration Successfully"})
                response.status_code = 201
                return response
        else:
            response = jsonify({
                "message": "Event Registration failed, Please check your input"
            })
            response.status_code = 400
            return response
