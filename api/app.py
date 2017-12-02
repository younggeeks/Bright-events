import uuid
from collections import Counter

from flask import Flask, request, jsonify, redirect
from flask_restful import Resource, Api, reqparse

from database.data_mocks import DataMocks
from database.models import User, Event
from helpers import event_parser, user_parser, failed_login

app = Flask(__name__)
api = Api(app)


@app.errorhandler(404)
def page_not_found(e):
    return jsonify(error=404, text=str(e)), 404


@app.route("/", methods=["GET"])
def index():
    return redirect("https://bright-event.herokuapp.com/api/v1/events")


class Register(Resource):
    def post(self):
        data = request.get_json()
        user = [user for user in DataMocks.users if user.email == data["email"]]
        if not user:
            new_user = User(id=uuid.uuid4(), full_name=data["full_name"],
                            email=data["email"], password=data["password"])
            DataMocks.users.append(new_user)
            response = jsonify(
                {"message": "Successfully created User",
                 "user": user_parser(new_user)}
            )
            response.status_code = 201
            return response
        resp = jsonify(
            {"message": "Account With Email {} Already Exists".format(data["email"])})
        resp.status_code = 400

        return resp


class Login(Resource):
    def post(self):
        credentials = request.get_json()
        user = [found_user for found_user in DataMocks.users
                if found_user.email == credentials["email"]]
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
        user = [found_user for found_user in
                DataMocks.users if found_user.email == credentials["email"]]
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


class PasswordReset(Resource):
    def post(self):
        data = request.get_json()
        user = [found_user for found_user in DataMocks.users if found_user.email == data["email"]]
        if not user:
            resp = jsonify({"message": "Email {} is not associated with any Account,"
                                       " Reset Failed".format(data["email"])})
            resp.status_code = 401
            return resp

        user = user[0]
        user.password = data["password"]

        updated_users = [temp_user for temp_user in
                         DataMocks.users if str(temp_user.email) != str(data["email"])]
        updated_users.append(user)

        data_mocks = DataMocks()
        data_mocks.update_users(updated_users)

        resp = jsonify({"message": "Password Reset Is Successful"})
        resp.status_code = 201
        return resp


class Events(Resource):
    def get(self):
        return jsonify({
            "message": "successfully Fetched Events",
            "status": 200,
            "events": DataMocks.get_data("events", data=DataMocks.events)
        })

    def post(self):
        data = request.get_json()
        event = [found_event for found_event in DataMocks.events if found_event.name == data["name"]]
        if not event:
            event = Event(id=uuid.uuid4(), price=data["price"], name=data["name"],
                          address=data["address"], start_date=data["start_date"],
                          end_date=data["end_date"], user=data["user"],
                          description=data["description"],
                          category=data["category"])
            DataMocks.events.append(event)
            resp = jsonify({"message": "Event Successfully Created!", "event": event_parser(event)})
            resp.status_code = 201
            return resp
        else:
            resp = jsonify({"message": "Event Name Must Be unique"})
            resp.status_code = 400
            return resp


class UserEvents(Resource):
    def get(self, user):
        found_users = [found_user for found_user in DataMocks.users if found_user.full_name == user]

        if not found_users:
            resp = jsonify({"message": "User Not Found, Fetch Failed"})
            resp.status_code = 404
            return resp

        user_events = [found_event for found_event in DataMocks.events if str(found_event.user) == str(user)]

        resp = jsonify(
            {"message": "Successfully Fetched Events", "events": DataMocks.get_data("events", data=user_events)})
        resp.status_code = 200
        return resp


class EventList(Resource):
    def get(self, event_id):
        event = [found_event for found_event in DataMocks.events if str(found_event.id) == str(event_id)]
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
        event = [found_event for found_event in DataMocks.events if str(found_event.id) == str(event_id)]
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
        if "price" in data:
            event.price = data["price"]
        event.id = event_id

        updated_events = [temp_event for temp_event in
                          DataMocks.events if str(temp_event.id) != str(event_id)]
        updated_events.append(event)

        data_mocks = DataMocks()
        data_mocks.update_events(updated_events)

        return jsonify({
            "message": "Event Updated Successfully",
            "status": 200,
            "event": event_parser(event)
        })

    def delete(self, event_id):
        event_list = [temp_event for temp_event in
                      DataMocks.events if str(temp_event.id) == event_id]
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
        """
        Fetching Event Guests from Our Data Structure, if event is not found 404 error is returned otherwise
        list of attendees is returned
        :param event_id:
        :return List<attendees>:
        """
        matching_events = [found_event for found_event in DataMocks.events if str(found_event.id) == str(event_id)]

        if not matching_events:
            resp = jsonify({"message": "Event Not found, Retrieval Failed"})
            resp.status_code = 404
            return resp

        guests = [event for event in DataMocks.rsvps if str(event["event_id"]) == str(event_id)]

        print guests
        if guests:
            guests = guests[0]
            rsvp_guests = DataMocks.get_data("users", guests["users"])
            return jsonify({
                "message": "Successfully Fetched Attendees",
                "status": 200,
                "attendees": rsvp_guests
            })

        return jsonify({
            "message": "Currently there are no guests registered for {}".format(matching_events[0].name),
            "status": 200,
            "attendees": None
        })


class RSVP(Resource):
    """
    Handle Subscription to an event
    """

    def post(self, event_id):

        """
        Inputs user_id and event_id , Before user can rsvp we check to see if event exists and if user exists
        if not 404 status code is set and error is returned , other wise user can rsvp to an event
        :return json response :
        :param event_id
        """
        data = request.get_json()
        event = [temp_event for temp_event in DataMocks.events if str(temp_event.id) == str(event_id)]
        if not event:
            response = jsonify({"message": "Event Not found, RSVP Failed"})
            response.status_code = 404
            return response
        user = [temp_user for temp_user in DataMocks.users if str(temp_user.id) == str(data["user_id"])]
        if not user:
            response = jsonify({"message": "User Not found, RSVP Failed"})
            response.status_code = 404
            return response
        user = user[0]
        # checking if event exists in rsvp array
        rsvp_events = [found_event for found_event in DataMocks.rsvps if str(found_event["event_id"]) == str(event_id)]

        if event[0].user == user.full_name:
            response = jsonify({"message": "You can not RSVP To your own event", "owner": True})
            response.status_code = 400
            return response

        new_user = User(id=user.id, full_name=user.full_name, email=user.email, password=user.password)
        # if event has at least one guest  we fetch guests to check if our current guest has already rsvp'ed
        if rsvp_events:
            # we get all guests from that event
            event_guests = [guest for guest in rsvp_events[0]["users"] if str(guest.id) == str(data["user_id"])]

            # we check to see the user who wants to rsvp is existing guest
            existing_users = [found_user for found_user in event_guests if str(found_user.id) == str(user.id)]
            if existing_users:
                return jsonify({
                    "message": "Your name is already in guest list of  {}".format(event[0].name),
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
        return jsonify({
            "message": "You've successfully RSVP'ed to {}".format(event[0].name),
            "status": 200
        })


class GetEventByCategory(Resource):
    def get(self, category):
        """
        Fetching Events by CAtegory
        :param category:
        :return:
        """
        found_events = [event for event in DataMocks.events if event.category == category]

        if not found_events:
            response = jsonify({"message": "Category Not found, Fetching Events Failed"})
            response.status_code = 404
            return response

        response = jsonify(
            {
                "message": "Successfully Fetched events",
                "events": DataMocks.get_data("events", found_events)
            })
        response.status_code = 200
        return response


class Reports(Resource):
    def get(self, user):
        my_events = [event for event in DataMocks.events if event.user == user]
        counter = Counter()
        for event in my_events:
            counter[event.category] += 1
        resp = {
            "categories": counter.keys(),
            "count": counter.values()
        }
        return resp


# routes for events managements
api.add_resource(Events, '/api/v1/events')
api.add_resource(RSVP, '/api/v1/events/<event_id>/rsvp')
api.add_resource(EventList, '/api/v1/events/<event_id>')
api.add_resource(Attendees, '/api/v1/events/<event_id>/guests')
api.add_resource(UserEvents, '/api/v1/<user>/events')
api.add_resource(Reports, '/api/v1/events/<user>/charts')
api.add_resource(GetEventByCategory, '/api/v1/category/<category>/events')

# routes for Authentication
api.add_resource(Register, '/api/v1/auth/register')
api.add_resource(Login, '/api/v1/auth/login')
api.add_resource(Logout, '/api/v1/auth/logout')
api.add_resource(PasswordReset, '/api/v1/auth/reset-password')

if __name__ == '__main__':
    app.run(debug=True)
