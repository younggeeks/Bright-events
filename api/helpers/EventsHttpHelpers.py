import json

import time

from api.helpers.tests_dummy_data import BASE_URL, correct_user, updated_correct_event, encode_token
from tests.test_users import UsersTester


class EventsHttpHelper:
    def __init__(self, client):
        self.client = client

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
            headers = dict(Authorization='Bearer ' + token)
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
            headers = dict(Authorization='Bearer ' + token)
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
