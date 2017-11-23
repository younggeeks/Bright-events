from flask import Flask, request, jsonify
from models import User, Event
from flask_restful import Resource, Api
from helpers import event_parser, user_parser, failed_login
from data_mocks import events, get_data, users
import uuid

app = Flask(__name__)
api = Api(app)


class Register(Resource):
    def post(self):
        data = request.get_json()
        user = filter(lambda found_user: found_user["email"] == data["email"], get_data("users"))
        if not user:
            new_user = User(id=data["id"], full_name=data["full_name"], email=data["email"], password=data["password"])
            users.append(new_user)
            response = jsonify({"message": "Successfully created User", "user": user_parser(new_user)})
            response.status_code = 201
            return response
        resp = jsonify({"message": "Account With Email {} Already Exists".format(data["email"])})
        resp.status_code = 400
        return resp


class Login(Resource):
    def post(self):
        credentials = request.get_json()
        user = filter(lambda found_user: found_user["email"] == credentials["email"], get_data("users"))
        if not user:
            return failed_login()
        if credentials["password"] not in user[0].values():
            return failed_login()
        return jsonify({
            "message": "User Login Successfully",
            "status": 200,
            "user": user
        })


class Logout(Resource):
    def post(self):
        credentials = request.get_json()
        user = filter(lambda found_user: found_user["email"] == credentials["email"], get_data("users"))

        if not user:
            resp = jsonify({"message": "User is already Signed out"})
            resp.status_code = 401
            return resp

        if credentials["password"] not in user[0].values():
            resp = jsonify({"message": "User is already Signed out"})
            resp.status_code = 401
            return resp

        # destroying session
        resp = jsonify({"message": "Sign out Successfully"})
        resp.status_code = 200
        return resp


class PasswordReset(Resource):
    def post(self):
        data = request.get_json()
        user = filter(lambda found_user: found_user["email"] == data["email"], get_data("users"))

        if not user:
            resp = jsonify({"message": "Email {} is not associated with any Account,"
                                       " Reset Failed".format(data["email"])})
            resp.status_code = 401
            return resp

        user = user[0]
        user["password"] = data["password"]

        new_users = filter(lambda found_user: found_user["email"] != data["email"], get_data("users"))
        new_users.append(user)

        # in real data base we could update the existing list with new user details

        resp = jsonify({"message": "Password Reset Is Successful", "event": user})
        resp.status_code = 201
        return resp


class Events(Resource):
    def get(self):
        return jsonify({
            "message": "successfully Fetched Events",
            "status": 200,
            "events": get_data("events")
        })

    def post(self):
        data = request.get_json()
        event = filter(lambda found_event: found_event["name"] == data["name"], get_data("events"))
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
    def put(self, event_id):
        data = request.get_json()
        event = filter(lambda found_event: str(found_event["id"]) == str(event_id), get_data("events"))
        if not event:
            resp = jsonify({"message": "Event Not Found, Update Failed", "status": 404})
            resp.status_code = 404
            return resp
        event = event[0]
        if "name" in data:
            event["name"] = data["name"]
        if "address" in data:
            event["address"] = data["address"]
        if "start_date" in data:
            event["start_date"] = data["start_date"]
        if "end_date" in data:
            event["end_date"] = data["end_date"]
        if "user " in data:
            event["user"] = data["user"]
        if "description" in data:
            event["description"] = data["description"]
        if "category" in data:
            event["category"] = data["category"]
        event["id"] = event_id

        new_events = filter(lambda found_event: found_event["id"] != event_id, get_data("events"))
        new_events.append(event)

        return jsonify({
            "message": "Event Updated Successfully",
            "status": 201,
            "event": event
        })

    def delete(self, event_id):
        event = filter(lambda found_event: str(found_event["id"]) == str(event_id), get_data("events"))
        if not event:
            response = jsonify({"message": "Event ID Not Found, Deletion Failed"})
            response.status_code = 404
            return response
        # simulating removal of event from database , we are using lambda function to remove it from the list
        # new_events = filter(lambda found_event: found_event["id"] != event_id, self.get_data("events"))

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

        # event is found get event_id and user_id from data["user_id"] search from db
        return jsonify({
            "message": "Successfully Fetched Attendees",
            "status": 200,
            "attendees": get_data("users")
        })


class RSVP(Resource):
    def post(self, event_id):
        data = request.get_data()
        event = filter(lambda found_event: str(found_event["id"]) == str(event_id), get_data("events"))
        if not event:
            response = jsonify({"message": "Event Not found, RSVP Failed"})
            response.status_code = 404
            return response

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


# routes for Authentication
api.add_resource(Register, '/api/v1/auth/register')
api.add_resource(Login, '/api/v1/auth/login')
api.add_resource(Logout, '/api/v1/auth/logout')
api.add_resource(PasswordReset, '/api/v1/auth/reset-password')


if __name__ == '__main__':
    app.run(debug=True)

