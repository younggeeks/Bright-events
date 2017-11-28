import uuid

from flask import Flask, request, jsonify
from flask_restful import Resource, Api, reqparse

from database.data_mocks import DataMocks
from database.models import User, Event
from helpers import event_parser, user_parser, failed_login

app = Flask(__name__)
api = Api(app)

events = DataMocks().events


class Register(Resource):
    def post(self):
        data = request.get_json()
        user = [user for user in DataMocks.users if user.email == data["email"]]
        print user
        if not user:
            new_user = User(id=data["id"], full_name=data["full_name"], email=data["email"], password=data["password"])
            DataMocks.users.append(new_user)
            response = jsonify({"message": "Successfully created User", "user": user_parser(new_user)})
            response.status_code = 201
            return response
        resp = jsonify({"message": "Account With Email {} Already Exists".format(data["email"])})
        resp.status_code = 400
        return resp


class Login(Resource):
    def post(self):
        credentials = request.get_json()
        user = [found_user for found_user in DataMocks.users if found_user.email == credentials["email"]]
        if not user:
            return failed_login()
        user = user_parser(user[0])
        if credentials["password"] not in user.values():
            return failed_login()
        return jsonify({
            "message": "User Login Successfully",
            "status": 200,
            "user": user
        })


class Logout(Resource):
    def post(self):
        credentials = request.get_json()
        user = [found_user for found_user in DataMocks.users if found_user.email == credentials["email"]]
        if not user:
            resp = jsonify({"message": "User is already Signed out"})
            resp.status_code = 401
            return resp

        user = user_parser(user[0])

        if credentials["password"] not in user.values():
            resp = jsonify({"message": "User is already Signed out"})
            resp.status_code = 401
            return resp

        # destroying session
        resp = jsonify({"message": "Sign out Successfully"})
        resp.status_code = 200
        return resp


class SearchEvent(Resource):
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('query', type=str, help='Please Specify query ')
        args = parser.parse_args()

        print args


class PasswordReset(Resource):
    def post(self):
        data = request.get_json()
        user = [found_user for found_user in DataMocks.users if found_user.email == data["email"]]
        if not user:
            resp = jsonify({"message": "Email {} is not associated with any Account,"
                                       " Reset Failed".format(data["email"])})
            resp.status_code = 401
            return resp
        #
        # user = user[0]
        # user["password"] = data["password"]
        # new_users = filter(lambda ne: found_user["email"] != data["email"], get_data("users"))
        # new_users.append(user)

        # in real data base we could update the existing list with new user details

        resp = jsonify({"message": "Password Reset Is Successful", "event": user})
        resp.status_code = 201
        return resp


class Events(Resource):
    def get(self):
        return jsonify({
            "message": "successfully Fetched Events",
            "status": 200,
            "events": DataMocks().get_data("events")
        })

    def post(self):
        data = request.get_json()
        event = [found_event for found_event in events if found_event.name == data["name"]]
        if not event:
            event = Event(id=uuid.uuid4(), name=data["name"], address=data["address"], start_date=data["start_date"],
                          end_date=data["end_date"], user=data["user"], description=data["description"],
                          category=data["category"])
            events.append(event)
            resp = jsonify({"message": "Event Successfully Created!", "event": event_parser(event)})
            resp.status_code = 201
            return resp
        else:
            resp = jsonify({"message": "Event Name Must Be unique"})
            resp.status_code = 422
            return resp


class EventList(Resource):
    def get(self, event_id):
        event = [found_event for found_event in events if str(found_event.id) == str(event_id)]
        if not event:
            resp = jsonify({"message": "Event Not Found, Fetch Failed", "status": 404})
            resp.status_code = 404
            return resp

        return jsonify({
            "message": "Event Fetch Successfully",
            "status": 200,
            "event": event_parser(event[0])
        })

    def put(self, event_id):
        data = request.get_json()
        event = [found_event for found_event in events if str(found_event.id) == str(event_id)]
        if not event:
            resp = jsonify({"message": "Event Not Found, Update Failed", "status": 404})
            resp.status_code = 404
            return resp

        event = event[0]

        if "name" in data:
            event.name = data["name"]
        if "address" in data:
            event.address = data["address"]
        if "start_date" in data:
            event.start_date = data["start_date"]
        if "end_date" in data:
            event.end_date = data["end_date"]
        if "user" in data:
            event.user = data["user"]
        if "description" in data:
            event.description = data["description"]
        if "category" in data:
            event.category = data["category"]
        event.id = event_id

        updated_events = [temp_event for temp_event in DataMocks.events if str(temp_event.id) != str(event_id)]
        updated_events.append(event)

        data_mocks = DataMocks()
        data_mocks.update_events(updated_events)

        return jsonify({
            "message": "Event Updated Successfully",
            "status": 201,
            "event": event_parser(event)
        })

    def delete(self, event_id):
        event_list = [temp_event for temp_event in DataMocks.events if str(temp_event.id) == event_id]
        if not event_list:
            response = jsonify({"message": "Event ID Not Found, Deletion Failed"})
            response.status_code = 404
            return response

        updated_events = [event_to_remove for event_to_remove in DataMocks.events
                          if str(event_to_remove.id) != str(event_id)]
        data_mocks = DataMocks()
        data_mocks.update_events(updated_events)

        response = jsonify({"message": "Event Deleted Successfully", "status": 200})
        response.status_code = 200
        return response


class Attendees(Resource):
    def get(self, event_id):
        event = filter(lambda found_event: str(found_event["id"]) == str(event_id), get_data("events"))

        if not event:
            resp = jsonify({
                "message": "Event Not found, Retrieval Failed"
            })
            resp.status_code = 404
            return resp

        guests = filter(lambda found_event: str(found_event["event_id"]) == str(event_id), rsvps)

        if guests:
            guests = guests[0]
            rsvp_guests = get_data("users", guests["users"])
            return jsonify({
                "message": "Successfully Fetched Attendees",
                "status": 200,
                "attendees": rsvp_guests
            })
        else:
            return jsonify({
                "message": "Currently there are no guests registered for {}".format(event[0]["name"]),
                "status": 200,
            })


class RSVP(Resource):
    def post(self, event_id):
        data = request.get_json()
        event = filter(lambda found_event: str(found_event["id"]) == str(event_id), get_data("events"))
        if not event:
            response = jsonify({"message": "Event Not found, RSVP Failed"})
            response.status_code = 404
            return response

        user = filter(lambda found_user: str(found_user["id"]) == str(data["user_id"]), get_data("users"))
        if not user:
            response = jsonify({"message": "User Not found, RSVP Failed"})
            response.status_code = 404
            return response
        # filter method above returns an array so we pass in index 0 to get the first one
        user = user[0]

        rsvp_events = filter(lambda found_event: str(found_event["event_id"]) == str(event_id), rsvps)
        new_user = User(id=user["id"], full_name=user["full_name"], email=user["email"], password=user["password"])
        if rsvp_events:
            event_guests = filter(lambda found_user: str(found_user["id"]) == str(data["user_id"]),
                                  get_data("users", rsvp_events[0]["users"]))

            existing_users = filter(lambda found_user: str(found_user["id"]) == str(user["id"]), event_guests)
            if existing_users:
                return jsonify({
                    "message": "Your name is already in guest list of  {}".format(event[0]["name"]),
                    "status": 400
                })
            rsvp_events[0]["users"].append(new_user)

        else:
            rsvp_events.append(
                {
                    "event_id": event_id,
                    "users": [new_user]
                }
            )
        # event is found we can add event_id and user_id to user_event_table
        return jsonify({
            "message": "You've successfully RSVP'ed to {}".format(event[0]["name"]),
            "status": 200
        })


# routes for events managements
api.add_resource(Events, '/api/v1/events')
api.add_resource(RSVP, '/api/v1/events/<event_id>/rsvp')
api.add_resource(EventList, '/api/v1/events/<event_id>')
api.add_resource(Attendees, '/api/v1/events/<event_id>/guests')
api.add_resource(SearchEvent, '/api/v1/events/search')

# routes for Authentication
api.add_resource(Register, '/api/v1/auth/register')
api.add_resource(Login, '/api/v1/auth/login')
api.add_resource(Logout, '/api/v1/auth/logout')
api.add_resource(PasswordReset, '/api/v1/auth/reset-password')

if __name__ == '__main__':
    app.run(debug=True)
