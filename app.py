import uuid
from collections import Counter
from flask import Flask, request, jsonify, render_template, abort
from flask_restful import Resource, Api
from database.data_mocks import DataMocks
from database.models import User, Event
from helpers import event_parser, user_parser, failed_login, make_response

app = Flask(__name__)
api = Api(app)


def get_events_by_id(event_id):
    return [found_event for found_event in DataMocks.events if str(found_event.id) == str(event_id)]


def get_events_by_user(user):
    return [found_event for found_event in DataMocks.events if str(found_event.user) == str(user)]


def get_events_by_category(category):
    return [found_event for found_event in DataMocks.events if str(found_event.category) == str(category)]


def get_user_by_email(email):
    return [temp_user for temp_user in DataMocks.users if str(temp_user.email) == str(email)]


def get_user_by_id(user_id):
    return [temp_user for temp_user in DataMocks.users if str(temp_user.id) == str(user_id)]


def update_fields(event, event_id, data, ):
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
    return event


@app.errorhandler(404)
def page_not_found(e):
    """
    Catches 404 errors and returns json with error information
    :param e:
    :return json:
    """
    return jsonify(error=404, text=str(e)), 404


@app.route("/", methods=["GET"])
def index():
    """
    Handles displaying Api documentation
    :return:
    """
    return render_template("docs.html")


class Register(Resource):
    """handles users registration """

    def post(self):
        """
        User registration, It uses list of
        dictionaries stored in memory to store users
        Checks for existence of user email and returns
        400 if user exists otherwise user is
        added to the list
        :return:
        """
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
        return make_response(status=400,
                             message="Account With Email {} Already Exists".format(data["email"]))


class Login(Resource):
    def post(self):
        """
        Handles authentication of user ,
         if user credentials match the ones in the list
         json response is sent with user details otherwise
         error response is sent
         """
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
        """
        Logged in users can logout, credentials are removed
        from the list, if user doesn't exist
        Error message will be sent with status of 401
        :return:
        """
        credentials = request.get_json()
        user = [found_user for found_user in
                DataMocks.users if found_user.email == credentials["email"]]
        if not user:
            return make_response(status=401, message="User is already Signed out")
        user = user_parser(user[0])
        if credentials["password"] not in user.values():
            return make_response(status=401, message="User is already Signed out")
        return make_response(status=200, message="Sign out Successfully")


class PasswordReset(Resource):
    def post(self):
        """Users who have created an account
           before can reset their password
           This method checks if an account
           associated with the email exists , if not
           Error is sent otherwise it resets the password"""
        data = request.get_json()
        user = [found_user for found_user in
                DataMocks.users if found_user.email == data["email"]]
        if not user:
            return make_response(status=401,
                                 message="Email {} is not associated with any Account,"
                                         " Reset Failed".format(data["email"]))
        user = user[0]
        user.password = data["password"]

        updated_users = [temp_user for temp_user in
                         DataMocks.users if str(temp_user.email) != str(data["email"])]
        updated_users.append(user)
        data_mocks = DataMocks()
        data_mocks.update_users(updated_users)
        return make_response(status=200,
                             message="Password Reset Is Successful")


class Events(Resource):
    """
    Fetches all events from the data structure
    """

    def get(self):
        return jsonify({
            "message": "successfully Fetched Events",
            "status": 200,
            "events": DataMocks.get_data("events", data=DataMocks.events)
        })

    def post(self):
        """Handles event registration,
            checks if event with same name is registered first
           If event exists error message is sent with status
            400 otherwise event is added to
           Events list"""
        data = request.get_json()
        event = [found_event for found_event in DataMocks.events
                 if found_event.name == data["name"]]
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
            return make_response(status=400, message="Event Name Must Be unique")


class UserEvents(Resource):
    def get(self, user):
        """
        Fetching All events of Specified user,
         if user doesn't exist an error is sent ,
          otherwise response is sent with message
          and list of events posted by specified user
        :param user:
        :return json:
        """
        found_users = [found_user for found_user in DataMocks.users if found_user.full_name == user]
        if not found_users:
            return make_response(status=404, message="User Not Found, Fetch Failed")
        user_events = [found_event for found_event in DataMocks.events if str(found_event.user) == str(user)]
        return jsonify({"message": "Successfully Fetched Events",
                        "events": DataMocks.get_data("events", data=user_events)})


class EventList(Resource):
    def get(self, event_id):
        """
        Fetching Single Event from data structure ,
         if event is not found error message is sent
        with 404 status otherwise response is sent
         with message and found event
        :param event_id:
        :return:
        """
        event = get_events_by_id(event_id)
        if not event:
            return make_response(status=404, message="Event Not Found, Fetch Failed")
        return jsonify({"message": "Event Fetch Successfully",
                        "status": 200, "event": event_parser(event[0])})

    def put(self, event_id):
        """
        Handles updating specified event, uses passed
        event id to lookup and if an event is not found
        error is sent with 404, otherwise event is updated
         according to user input and response is
        sent with message and updated event
        :param event_id:
        :return:
        """
        data = request.get_json()
        event = get_events_by_id(event_id)
        if not event:
            return make_response(status=404, message="Event Not Found, Update Failed")
        event = event[0]
        event = update_fields(event, event_id, data)
        updated_events = [temp_event for temp_event in
                          DataMocks.events if str(temp_event.id) != str(event_id)]
        updated_events.append(event)
        data_mocks = DataMocks()
        data_mocks.update_events(updated_events)
        return jsonify({"message": "Event Updated Successfully", "event": event_parser(event)})

    def delete(self, event_id):
        """
        Handling deletion of specified event ,
        uses event id to lookup , if event with that is is
        found it is deleted otherwise error response is
        sent with message and status of 404
        :param event_id:
        :return:
        """
        event_list = [temp_event for temp_event in
                      DataMocks.events if str(temp_event.id) == event_id]
        if not event_list:
            return make_response(status=404, message="Event ID Not Found, Deletion Failed")

        updated_events = [event_to_remove for event_to_remove in DataMocks.events
                          if str(event_to_remove.id) != str(event_id)]
        data_mocks = DataMocks()
        data_mocks.update_events(updated_events)
        return make_response(status=200, message="Event Deleted Successfully")


class Attendees(Resource):
    def get(self, event_id):
        """
        Fetching Event Guests from Our Data Structure,
         if event is not found 404 error is returned otherwise
        list of attendees is returned
        :param event_id:
        :return List<attendees>:
        """
        matching_events = [found_event for found_event in DataMocks.events if str(found_event.id) == str(event_id)]

        if not matching_events:
            return make_response(status=404, message="Event Not found, Retrieval Failed")
        guests = [event for event in DataMocks.rsvps if str(event["event_id"]) == str(event_id)]
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
        checks to see if event exists and if user exists
        if not 404 status code is set and error is returned
         , other wise user can rsvp to an event
        :return json response :
        :param event_id
        """
        data = request.get_json()
        event = get_events_by_id(event_id)
        if not event:
            abort(404, "Event  Not found, RSVP Failed")
        user = get_user_by_id(data.get("user_id"))
        if not user:
            abort(404, "User Not found, RSVP Failed")
        user = user[0]
        if event[0].user == user.full_name:
            abort(400, "You can not RSVP To your own event")
        rsvp_events = [found_event for found_event in DataMocks.rsvps if str(found_event["event_id"]) == str(event_id)]
        if rsvp_events:
            event_guests = [guest for guest in rsvp_events[0]["users"] if str(guest.id) == str(user.id)]
            existing_users = [found_user for found_user in event_guests if str(found_user.id) == str(user.id)]
            if existing_users:
                abort(400, "Your name is already in guest list of  {}".format(event[0].name))
            rsvp_events[0]["users"].append(user)
        else:
            DataMocks.rsvps.append({"event_id": event_id, "users": [user]})
        abort(200, "You've successfully RSVP'ed to {}".format(event[0].name))


class GetEventByCategory(Resource):
    def get(self, category):
        """
        Fetching Events by category, if
         category is not found error is sent with 404 status
        otherwise response is sent with
         with list of events in that category
        :param category:
        :return List<event>:
        """
        found_events = get_events_by_category(category)
        if not found_events:
            return make_response(status=404, message="Category Not found, Fetching Events Failed")
        response = jsonify(
            {
                "message": "Successfully Fetched events",
                "events": DataMocks.get_data("events", found_events)
            })
        response.status_code = 200
        return response


class Reports(Resource):
    def get(self, user):
        """
        Fetches reports for a specified user
        :param user:
        :return:
        """
        my_events = get_events_by_user(user=user)
        counter = Counter()
        for event in my_events:
            counter[event.category] += 1
        categories = []
        counts = []
        if counter:
            # fetch categories from events and use them as titles for graph
            [categories.append(category) for category in counter.keys()]
            # fetch counts  from events and use them as titles for graph
            [counts.append(num) for num in counter.values()]
        response = jsonify({
            "categories": categories,
            "values": counts

        })
        return response


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
