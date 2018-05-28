import uuid
from collections import Counter
import os
from flask import Blueprint, request, jsonify, g, url_for
from flask_cors import CORS
from flask_restful import Api, Resource
from sqlalchemy import asc
from api.helpers.response_helpers import protected_route, make_response, validate_inputs, validate_event_form
from api.helpers.tests_dummy_data import required_event_fields

events = Blueprint("events", __name__, url_prefix="/api/v1/events")
CORS(events)
api = Api(events, catch_all_404s=True)

from api.models import Event, Category, User
from api.helpers import response_helpers


def uploadImage(local_dir, image):
    newpath = local_dir
    if not os.path.exists(newpath):
        os.makedirs(newpath)
    ext = image.filename.strip()
    image_name = uuid.uuid4().hex + ext
    saved_path = os.path.join(os.getenv("UPLOAD_FOLDER"), image_name)
    image.save(saved_path)
    return image_name


def removeImage(image):
    saved_path = os.path.join(os.getenv("UPLOAD_FOLDER"), image)
    if os.path.isfile(saved_path):
        os.remove(saved_path)
    else:
        print("Image {} Not found", format(saved_path))


def search(search_type):
    q = request.args.get("q")
    if not q or q == "":
        response = jsonify({
            "message": "Query Not Specified, Search Failed"
        })
        response.status_code = 400
        return response
    if search_type == "name":
        found_events = Event.query.filter(Event.name.ilike('%{}%'.format(q))).all()
    elif search_type == "location":
        found_events = Event.query.filter(Event.address.ilike('%{}%'.format(q))).all()

    if found_events and len(found_events) > 0:
        response = jsonify({
            "message": "Successfully Retrieved Events Matching {}".format(q),
            "events": response_helpers.parse_list("events", found_events)
        })
        response.status_code = 200
        return response
    else:
        response = jsonify({
            "message": "Event Matching {} Was not found".format(q)
        })
        response.status_code = 404
        return response


class Categories(Resource):
    def get(self):
        all_categories = Category.query.all()
        categories_dict = []
        [categories_dict.append({'id': category.id, 'name': category.name}) for category in all_categories]
        response = jsonify({
            "categories": categories_dict
        })
        response.status_code = 200
        return response


class EventList(Resource):
    def get(self):
        page = 1
        limit = 3
        if "limit" in request.args and request.args.get("limit"):
            limit = int(request.args.get('limit', 3))

        if "page" in request.args and request.args.get("page"):
            page = max(0, int(request.args.get("page")))

        print("data is ", page,limit)

        paginated_events = Event.query.paginate(page,limit,False)
        all_events = paginated_events.items
        response = jsonify({
            "message": "Events Retrieved Successfully",
            "events": response_helpers.parse_list("events", all_events),
            "has_next":paginated_events.has_next
        })
        response.status_code = 200
        return response

    @protected_route
    @validate_event_form(required_event_fields)
    def post(self):
        data = request.form
        event = Event.query.filter_by(name=data["name"]).first()
        if event:
            return make_response(400, "Event Name Must be Unique")
        else:
            category = Category.query.filter_by(name=data["category"]).first()
            if category:
                category_id = category.id
            else:
                new_category = Category(name=data["category"])
                new_category.save()
                category_id = new_category.id
            if request.files.get('image'):
                img = uploadImage(os.getenv("UPLOAD_FOLDER"), request.files['image'])
            else:
                img = None

            new_event = Event(name=data.get("name"), image=img, address=data.get("address"),
                              start_date=data.get("start_date"),
                              end_date=data.get("end_date"), description=data.get("description"),
                              price=data.get("price"),
                              category_id=category_id)
            user = g.user
            user.events.append(new_event)
            try:
                user.save()
            except Exception as e:
                return make_response(400, "Category With id {} is not found,"
                                          " Event Creating Failed".format(data["category_id"]), e.message)
            response = jsonify({"message": "Event Registration Successfully"})
            response.status_code = 201
            return response


class MyEvents(Resource):
    @protected_route
    def get(self):
        user = g.user
        events = Event.query.filter_by(user_id=user.id).all()
        response = jsonify({
            "message": "Events Retrieved Successfully",
            "events": response_helpers.parse_list("events", events)
        })
        response.status_code = 200
        return response


class MyRsvps(Resource):
    @protected_route
    def get(self):
        user = g.user
        mine_rsvps = []
        eventz = Event.query.all()
        for event in eventz:
            [mine_rsvps.append(event) for foundUser in event.rsvps if foundUser.id == user.id]

        response = jsonify({
            "message": "Events Retrieved Successfully",
            "events": response_helpers.parse_list("events", mine_rsvps)
        })
        response.status_code = 200
        return response


class Events(Resource):
    @protected_route
    def put(self, event_id):
        event = Event.query.filter_by(id=event_id).first()
        if not event:
            return make_response(404, "Event With ID {} is not found".format(event_id))

        if event.user_id != g.user.id:
            return make_response(403, "You can only Update Events You Created")

        data = request.form
        if not data:
            return make_response(400, "Update Failed, Please check your input")

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

    def get(self, event_id):
        event = Event.query.filter_by(id=event_id).first()
        if not event:
            return make_response(404, "Event With ID {} is not found".format(event_id))

        category = Category.query.filter_by(id=event.category_id).first()

        event = response_helpers.event_parser(event=event, category=category.name)
        response = jsonify({"message": "Event Retrieved Successfully", "event": event})
        response.status_code = 200
        return response

    @protected_route
    def delete(self, event_id):
        event = Event.query.filter_by(id=event_id).first()
        if not event:
            return make_response(404, "Event With ID {} is not found".format(event_id))

        if event.user_id != g.user.id:
            return make_response(403, "You can only Delete Events You Created")

        event.delete()
        removeImage(event.image)
        response = jsonify({
            "message": "Event Deletion Successful"
        })
        response.status_code = 200
        return response


class RSVP(Resource):
    @protected_route
    def post(self, event_id):
        data = request.get_json()
        if "user_id" not in data:
            return make_response(400, "RSVP Failed, Please check your input")

        event = Event.query.filter_by(id=event_id).first()
        if not event:
            return make_response(404, "Event With ID {} is not found".format(event_id))

        guest = g.user

        if event.user_id == guest.id:
            return make_response(403, "You can not RSVP To your own event")

        existing_user = [user for user in event.rsvps if user.id == guest.id]
        if existing_user:
            return make_response(403, "Your Name is already in {}'s Guest List".format(event.name))

        event.rsvps.append(guest)
        event.save()
        response = jsonify({
            "message": "RSVP successfully"
        })
        response.status_code = 200
        return response


class Guests(Resource):
    @protected_route
    def get(self, event_id):
        event = Event.query.filter_by(id=event_id).first()
        if not event:
            return make_response(404, "Event With ID {} is not found".format(event_id))

        user = g.user

        if event.user_id != user.id:
            return make_response(403, "You can only See the guests of the event you created")

        guests = response_helpers.parse_list("users", event.rsvps)

        response = jsonify({
            "message": "Successfully Retrieved Event Guests",
            "guests": guests
        })
        response.status_code = 200
        return response


class Search(Resource):
    def get(self):
        return search("name")


class SearchLocation(Resource):
    def get(self):
        return search("location")


class Paginate(Resource):
    # TODO add start and end links to pagination
    def get(self):
        if "limit" in request.args and request.args.get("limit"):
            limit = int(request.args.get('limit', 3))

        if "page" in request.args and request.args.get("page"):
            page = max(0, int(request.args.get("page")))

        ordered_events = Event.query.order_by(asc(Event.id)).all()
        if ordered_events:
            next_page = page + limit
            maximum_index = len(ordered_events) - 1
            if page > maximum_index:
                last_id = ordered_events[maximum_index].id
                next_page = page
            else:
                last_id = ordered_events[page].id

            all_events = Event.query.filter(Event.id >= last_id).limit(limit).all()

            next_url = url_for("events.paginate", limit=limit, page=next_page)
            prev_url = url_for("events.paginate", limit=limit, page=max(0, next_page - limit))

            return jsonify({
                "events": response_helpers.parse_list("events", all_events),
                "prev_url": prev_url,
                "next_url": next_url
            })
        else:
            return jsonify({
                "message": "It seems there no events in the system"
            })


class Reports(Resource):
    @protected_route
    def get(self):
        """
        Fetches reports for a specified user
        :param user:
        :return:
        """

        my_events = Event.query.filter(Event.user_id == g.user.id).all()

        counter = Counter()
        for event in my_events:
            if len(event.rsvps) > 0:
                counter[event.name] = len(event.rsvps)

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


api.add_resource(EventList, "/")
api.add_resource(Events, "/<int:event_id>")
api.add_resource(RSVP, "/<int:event_id>/rsvp")
api.add_resource(Guests, "/<int:event_id>/guests")
api.add_resource(Search, "/search")
api.add_resource(SearchLocation, "/location")
api.add_resource(Paginate, "/filter")
api.add_resource(Reports, "/reports")
api.add_resource(Categories, "/categories")
api.add_resource(MyEvents, "/my-events")
api.add_resource(MyRsvps, "/my-rsvps")
