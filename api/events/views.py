from functools import wraps

from flask import Blueprint, request, jsonify, g, abort
from flask_restplus import Api, Resource

events = Blueprint("events", __name__, url_prefix="/api/v1/events")

api = Api(events, version='1.0', title='Bright Events API',
          description='Awesome Api for managing events', catch_all_404s=True
          )

from api.models import Event, User
from api import response_helpers


def search(search_type):
    parser = api.parser()
    parser.add_argument('q', type=str, help='Event Name', location='args')
    args = parser.parse_args()
    if not args['q']:
        response = jsonify({
            "message": "Query Not Specified, Search Failed"
        })
        response.status_code = 400
        return response
    if search_type == "name":
        found_events = Event.query.filter(Event.name.ilike('%{}%'.format(args['q']))).all()
    elif search_type == "location":
        found_events = Event.query.filter(Event.address.ilike('%{}%'.format(args['q']))).all()
    elif search_type == "category":
        found_events = Event.query.filter(Event.category.name.ilike('%{}%'.format(args['q']))).all()
    else:
        found_events = Event.query.filter(Event.name.ilike('%{}%'.format(args['q']))).all()

    if found_events and len(found_events) > 0:
        response = jsonify({
            "message": "Successfully Retrieved Events Matching {}".format(args['q']),
            "guests": response_helpers.parse_list("events", found_events)
        })
        response.status_code = 200
        return response
    else:
        response = jsonify({
            "message": "Event Matching {} Was not found".format(args['q'])
        })
        response.status_code = 404
        return response


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


@api.route("/<event_id>")
class Events(Resource):
    @protected_route
    def put(self, event_id):
        event = Event.query.filter_by(id=event_id).first()
        if event.user_id != g.user.id:
            response = jsonify({
                "message": "You can only Update Events You Created"
            })
            response.status_code = 403
            return response
        if not event:
            response = jsonify({
                "message": "Event With ID {} is not found".format(event_id)
            })
            response.status_code = 404
            return response
        data = request.get_json()
        if not data:
            response = jsonify({
                "message": "Update Failed, Please check your input"
            })
            response.status_code = 400
            return response

        if "name" in data:
            event.name = data["name"]
        if "address" in data:
            event.address = data["address"]
        if "start_date" in data:
            event.start_date = data["start_date"]
        if "end_date" in data:
            event.end_date = data["end_date"]
        if "user_id" in data:
            event.user_id = data["user_id"]
        if "description" in data:
            event.description = data["description"]
        if "category_id" in data:
            event.category_id = data["category_id"]
        if "price" in data:
            event.price = data['price']

        event.save()
        response = jsonify({"message": "Event Updated Successfully"})
        response.status_code = 200
        return response

    @protected_route
    def delete(self, event_id):
        event = Event.query.filter_by(id=event_id).first()
        if not event:
            response = jsonify({
                "message": "Event With ID {} is not found".format(event_id)
            })
            response.status_code = 404
            return response
        if event.user_id != g.user.id:
            response = jsonify({
                "message": "You can only Delete Events You Created"
            })
            response.status_code = 403
            return response

        event.delete()
        response = jsonify({
            "message": "Event Deletion Successfully"
        })
        response.status_code = 200
        return response


@api.route("/<event_id>/rsvp")
class RSVP(Resource):
    @protected_route
    def post(self, event_id):
        data = request.get_json()
        if "user_id" not in data:
            response = jsonify({
                "message": "RSVP Failed, Please check your input"
            })
            response.status_code = 400
            return response
        event = Event.query.filter_by(id=event_id).first()
        if not event:
            response = jsonify({
                "message": "Event With ID {} is not found".format(event_id)
            })
            response.status_code = 404
            return response

        guest = g.user

        if event.user_id == guest.id:
            response = jsonify({
                "message": "You can not RSVP To your own event"
            })
            response.status_code = 404
            return response

        existing_user = [user for user in event.rsvps if user.id == guest.id]
        if existing_user:
            response = jsonify({
                "message": "Your Name is already in {}'s Guest List".format(event.name)
            })
            response.status_code = 404
            return response

        event.rsvps.append(guest)
        event.save()
        response = jsonify({
            "message": "RSVP successfully"
        })
        response.status_code = 200
        return response


@api.route("/<event_id>/guests")
class Guests(Resource):
    @protected_route
    def get(self, event_id):
        event = Event.query.filter_by(id=event_id).first()
        if not event:
            response = jsonify({
                "message": "Event With ID {} is not found".format(event_id)
            })
            response.status_code = 404
            return response

        user = g.user

        if event.user_id != user.id:
            response = jsonify({
                "message": "You can only See the guests of the event you created"
            })
            response.status_code = 403
            return response

        guests = response_helpers.parse_list("users", event.rsvps)

        response = jsonify({
            "message": "Successfully Retrieved Event Guests",
            "guests": guests
        })
        response.status_code = 200
        return response


@api.route("/search")
class Search(Resource):
    def get(self):
        return search("name")


@api.route("/location")
class SearchLocation(Resource):
    def get(self):
        return search("location")

