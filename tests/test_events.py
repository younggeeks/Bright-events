
import json
import unittest

import time

from api import create_app, db
from api.helpers.tests_dummy_data import BASE_URL, correct_event, correct_user, missing_field_event, \
    updated_correct_event, correct_user2, encode_token
from api.models import Category
from tests.test_users import UsersTester


class EventsTester(unittest.TestCase):
    def setUp(self):
        self.category = Category(name="noma sana")
        self.app = create_app("testing")
        self.client = self.app.test_client()
        self.test_db = db.init_app(self.app)
        with self.app.app_context():
            db.init_app(self.app)
            db.drop_all()
            db.create_all()
            db.session.add(self.category)
            db.session.commit()

    def user_login(self, user):
        response = UsersTester.login(self, user)
        return response

    def fetch_all(self):
        response = self.client.get("{}/api/v1/events/".format(BASE_URL))
        data = json.loads(response.data.decode())
        return {
            "status": response.status_code,
            "data": data
        }

    def fetch_one(self, event_id=1):
        response = self.client.get("{}/api/v1/events/{}".format(BASE_URL, event_id))
        data = json.loads(response.data.decode())
        return {
            "status": response.status_code,
            "data": data
        }

    def delete(self, token=None, header=True, event_id=1):
        if not token and header:
            headers = {}
        elif token and header:
            headers = dict(
                Authorization='Bearer ' + token
            )
        response = self.client.delete("{}/api/v1/events/{}".format(BASE_URL, event_id), headers=headers)
        data = json.loads(response.data.decode())
        return {
            "status": response.status_code,
            "data": data
        }

    def register(self, user, token=None, header=True):
        if not token and header:
            headers = {}
        elif token and header:
            headers = dict(
                Authorization='Bearer ' + token
            )

        UsersTester.user_registration(self, correct_user)
        response = self.client.post("{}/api/v1/events/".format(BASE_URL),
                                    data=json.dumps(user), headers=headers, content_type='application/json')
        data = json.loads(response.data.decode())

        return {
            "status": response.status_code,
            "data": data
        }

    def update(self, token=None, header=True, event_id=1, empty=False):
        if not token and header:
            headers = {}
        elif token and header:
            headers = dict(
                Authorization='Bearer ' + token
            )
        if not empty:
            event = updated_correct_event
        else:
            event = {}

        UsersTester.user_registration(self, correct_user)
        response = self.client.put("{}/api/v1/events/{}".format(BASE_URL, event_id),
                                   data=json.dumps(event), headers=headers, content_type='application'
                                                                                         '/json')
        data = json.loads(response.data.decode())
        return {
            "status": response.status_code,
            "data": data
        }

    def rsvp(self, token=None, header=True, event_id=1, empty_field=False):
        if not token and header:
            headers = {}
        elif token and header:
            headers = dict(
                Authorization='Bearer ' + token
            )

        if empty_field:
            data = {}
        else:
            data = {"user_id": 1}

        response = self.client.post("{}/api/v1/events/{}/rsvp".format(BASE_URL, event_id),
                                    data=json.dumps(data), headers=headers, content_type='application'
                                                                                         '/json')
        data = json.loads(response.data.decode())
        return {
            "status": response.status_code,
            "data": data
        }

    def guests(self, token=None, header=True, event_id=1):
        if not token and header:
            headers = {}
        elif token and header:
            headers = dict(
                Authorization='Bearer ' + token
            )

        response = self.client.get("{}/api/v1/events/{}/guests".format(BASE_URL, event_id), headers=headers)
        data = json.loads(response.data.decode())
        return {
            "status": response.status_code,
            "data": data
        }

    def get_token(self, user=correct_user, correct=True):
        if not correct:
            token = encode_token()
            time.sleep(1)
            return token
        UsersTester.user_registration(self, user)
        resp = self.user_login(user)
        token = resp["data"]["token"]
        return token

    def search(self, search_by, query=None):
        if not query:
            response = self.client.get("{}/api/v1/events/search?q=".format(BASE_URL))
            return {
                "status": response.status_code,
                "data": json.loads(response.data.decode())
            }
        if search_by == "name":
            response = self.client.get("{}/api/v1/events/search?q={}".format(BASE_URL, query))
        elif search_by == "location":
            response = self.client.get("{}/api/v1/events/location?q={}".format(BASE_URL, query))

        data = json.loads(response.data.decode())
        return {
            "status": response.status_code,
            "data": data
        }

    def paginate(self, limit=3, offset=0):
        response = self.client.get("{}/api/v1/events/filter?limit={}&&offset={}".format(BASE_URL, limit, offset))
        return {
            "status": response.status_code,
            "data": json.loads(response.data.decode())
        }

    def test_fetch_all_events(self):
        response = self.fetch_all()
        self.assertEqual(response["status"], 200)
        self.assertEqual(response["data"]["message"], "Events Retrieved Successfully")

    def test_register_missing_token(self):
        response = self.register(correct_event)
        self.assertEqual(response["status"], 401)
        self.assertEqual(response["data"]["message"], "Token is missing")

    def test_register_missing_field(self):
        response = self.register(missing_field_event, token=self.get_token())

        self.assertEqual(response["status"], 400)
        self.assertEqual(response["data"]["message"], "Event Registration failed, Please check your input")

    def test_register_successful(self):
        response = self.register(correct_event, token=self.get_token())
        self.assertEqual(response["status"], 201)
        self.assertEqual(response["data"]["message"], "Event Registration Successfully")

    def test_register_duplicate_event_name(self):
        self.register(correct_event, token=self.get_token())
        response = self.register(correct_event, token=self.get_token())
        self.assertEqual(response["status"], 400)
        self.assertEqual(response["data"]["message"], "Event name must be unique")

    def test_update_event_successful(self):
        token = self.get_token()
        self.register(correct_event, token=token)
        response = self.update(token=token)
        self.assertEqual(response["status"], 200)
        self.assertEqual(response["data"]["message"], "Event Updated Successfully")

    def test_update_event_not_found(self):
        token = self.get_token(user=correct_user)
        self.register(correct_event, token=token)
        response = self.update(token=token, event_id=3)
        self.assertEqual(response["status"], 404)
        self.assertEqual(response["data"]["message"], "Event With ID 3 is not found")

    def test_update_event_only_update_your_events(self):
        token = self.get_token(user=correct_user)
        self.register(correct_event, token=token)
        token2 = self.get_token(user=correct_user2)
        response = self.update(token=token2)
        self.assertEqual(response["status"], 403)
        self.assertEqual(response["data"]["message"], "You can only Update Events You Created")

    def test_update_event_missing_fields(self):
        token = self.get_token(user=correct_user)
        self.register(correct_event, token=token)
        response = self.update(token=token, empty=True)
        self.assertEqual(response["status"], 400)
        self.assertEqual(response["data"]["message"], "Update Failed, Please check your input")

    def test_fetch_single_event_successful(self):
        token = self.get_token(user=correct_user)
        self.register(correct_event, token=token)
        response = self.fetch_one()
        self.assertEqual(response["status"], 200)
        self.assertEqual(response["data"]["message"], "Event Retrieved Successfully")

    def test_fetch_single_event_not_found(self):
        response = self.fetch_one(event_id=3)
        self.assertEqual(response["status"], 404)
        self.assertEqual(response["data"]["message"], "Event With ID 3 is not found")

    def test_delete_event_not_found(self):
        token = self.get_token(user=correct_user)
        self.register(correct_event, token=token)
        response = self.delete(token=token, event_id=3)
        self.assertEqual(response["status"], 404)
        self.assertEqual(response["data"]["message"], "Event With ID 3 is not found")

    def test_delete_event_successful(self):
        token = self.get_token(user=correct_user)
        self.register(correct_event, token=token)
        response = self.delete(token=token)
        self.assertEqual(response["status"], 200)
        self.assertEqual(response["data"]["message"], "Event Deletion Successful")

    def test_delete_event_forbidden(self):
        token = self.get_token(user=correct_user)
        self.register(correct_event, token=token)
        token2 = self.get_token(user=correct_user2)
        response = self.delete(token=token2)
        self.assertEqual(response["status"], 403)
        self.assertEqual(response["data"]["message"], "You can only Delete Events You Created")

    def test_rsvp_successful(self):
        token = self.get_token(user=correct_user)
        self.register(correct_event, token=token)
        token2 = self.get_token(user=correct_user2)
        response = self.rsvp(token=token2)

        self.assertEqual(response["status"], 200)
        self.assertEqual(response["data"]["message"], "RSVP successfully")

    def test_rsvp_missing_field(self):
        token = self.get_token(user=correct_user)
        self.register(correct_event, token=token)
        token2 = self.get_token(user=correct_user2)
        response = self.rsvp(token=token2, empty_field=True)

        self.assertEqual(response["status"], 400)
        self.assertEqual(response["data"]["message"], "RSVP Failed, Please check your input")

    def test_rsvp_event_not_found(self):
        token = self.get_token(user=correct_user)
        self.register(correct_event, token=token)
        token2 = self.get_token(user=correct_user2)
        response = self.rsvp(token=token2, event_id=4)
        self.assertEqual(response["status"], 404)
        self.assertEqual(response["data"]["message"], "Event With ID 4 is not found")

    def test_rsvp_forbidden(self):
        token = self.get_token(user=correct_user)
        self.register(correct_event, token=token)
        response = self.rsvp(token=token)
        self.assertEqual(response["status"], 403)
        self.assertEqual(response["data"]["message"], "You can not RSVP To your own event")

    def test_rsvp_already_in_the_list(self):
        token = self.get_token(user=correct_user)
        self.register(correct_event, token=token)
        token2 = self.get_token(user=correct_user2)
        self.rsvp(token=token2)
        response = self.rsvp(token=token2)
        self.assertEqual(response["status"], 403)
        self.assertEqual(response["data"]["message"], "Your Name is already in Coders Campusess's Guest List")

    def test_retrieve_guest_list_successful(self):
        token = self.get_token(user=correct_user)
        self.register(correct_event, token=token)

        response = self.guests(token=token)
        self.assertEqual(response["status"], 200)
        self.assertEqual(response["data"]["message"], "Successfully Retrieved Event Guests")

    def test_retrieve_guest_list_successful(self):
        token = self.get_token(user=correct_user)
        self.register(correct_event, token=token)

        response = self.guests(token=token)
        self.assertEqual(response["status"], 200)
        self.assertEqual(response["data"]["message"], "Successfully Retrieved Event Guests")

    def test_retrieve_guest_list_event_not_found(self):
        token = self.get_token(user=correct_user)
        self.register(correct_event, token=token)

        response = self.guests(token=token, event_id=3)
        self.assertEqual(response["status"], 404)
        self.assertEqual(response["data"]["message"], "Event With ID 3 is not found")

    def test_retrieve_guest_list_forbidden(self):
        token = self.get_token(user=correct_user)
        self.register(correct_event, token=token)
        token2 = self.get_token(user=correct_user2)

        response = self.guests(token=token2)
        self.assertEqual(response["status"], 403)
        self.assertEqual(response["data"]["message"], "You can only See the guests of the event you created")

    def test_search_event_name_successfully(self):
        self.register(correct_event, token=self.get_token())
        response = self.search(search_by="name", query=correct_event["name"])

        self.assertEqual(response["status"], 200)
        self.assertEqual(response["data"]["message"], "Successfully Retrieved Events Matching Coders Campusess")

    def test_search_event_location_successfully(self):
        self.register(correct_event, token=self.get_token())
        response = self.search(search_by="location", query="Magomeni")

        self.assertEqual(response["status"], 200)
        self.assertEqual(response["data"]["message"], "Successfully Retrieved Events Matching Magomeni")

    def test_search_query_not_found(self):
        self.register(correct_event, token=self.get_token())
        response = self.search(search_by="location")
        self.assertEqual(response["status"], 400)
        self.assertEqual(response["data"]["message"], "Query Not Specified, Search Failed")

    def test_search_event_not_found(self):
        self.register(correct_event, token=self.get_token())
        response = self.search(search_by="location", query="Mwananyamala")
        self.assertEqual(response["status"], 404)
        self.assertEqual(response["data"]["message"], "Event Matching Mwananyamala Was not found")

    def test_pagination_success(self):
        self.register(correct_event, token=self.get_token())
        response = self.paginate()
        events = response["data"]["events"]
        self.assertEqual(response["status"], 200)
        self.assertEqual(isinstance(events, list), True)

    def test_pagination_no_events(self):
        response = self.paginate()
        self.assertEqual(response["status"], 200)
        self.assertEqual(response["data"]["message"], "It seems there no events in the system")
