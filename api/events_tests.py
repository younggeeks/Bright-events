import json
import unittest
import app
from data_mocks import events

BASE_URL = "http://localhost:5000"


class UsersTester(unittest.TestCase):
    pass


class EventTester(unittest.TestCase):
    def setUp(self):
        self.app = app.app.test_client()
        app.app.testing = True

    def test_fetch_events(self):
        response = self.app.get("{}/api/v1/events".format(BASE_URL))
        data = json.loads(response.get_data())
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(data["events"]), 4)

    def test_save_event_successfully(self):
        event = {
            "name": "new event",
            "address": "nairobi",
            "start_date": "4/2/201",
            "end_date": "3/34/3434",
            "description": ".l3dfkasdjfklasdjfkljalskdjflkasdfas",
            "user": "Masoud Masoud",
            "id": "4894509430",
            "category": " Wedding"
        }

        # testing if it returns number of events in our list
        self.assertEqual(len(events), 4)
        response = self.app.post("{}/api/v1/events".format(BASE_URL),
                                 data=json.dumps(event), content_type='application/json')

        # testing if adding event is successful
        self.assertEqual(response.status_code, 201)

        # testing if adding new user increases length of out list
        self.assertEqual(len(events), 5)

    def test_duplicate_event_name(self):
        event = {
            "name": "Angular Conference 2018",
            "address": "nairobi",
            "start_date": "4/2/201",
            "end_date": "3/34/3434",
            "description": ".l3dfkasdjfklasdjfkljalskdjflkasdfas",
            "user": "Masoud Masoud",
            "id": "4894509430",
            "category": " Wedding"
        }
        response = self.app.post("{}/api/v1/events".format(BASE_URL),
                                 data=json.dumps(event), content_type='application/json')
        self.assertEqual(response.status_code, 422)

    def test_successful_updating_event(self):
        event = {
            "name": "Angular Conference 2018",
            "address": "ijumaa",
            "id": "9494dfasd",
            "category": " Wedding",
            "start_date": "1/2/323",
            "end_date": "1/3/343",
            "user": "Samaki",
            "description": "awesome event You would'nt want to miss it"
        }
        response = self.app.put("{}/api/v1/events/{}".format(BASE_URL, event["id"]),
                                data=json.dumps(event), content_type='application/json')
        self.assertEqual(response.status_code, 200)

    def test_id_not_found_updating_event(self):
        event = {
            "name": "Angular Conference 2018",
            "address": "ijumaa",
            "id": "9494dfasd",
            "category": " Wedding",
            "start_date": "1/2/323",
            "end_date": "1/3/343",
            "user": "Samaki",
            "description": "awesome event You would'nt want to miss it"
        }
        response = self.app.put("{}/api/v1/events/{}".format(BASE_URL, event["id"]),
                                data=json.dumps(event), content_type='application/json')
        self.assertEqual(response.status_code, 404)

    def test_delete_successful(self):
        event_id = 9494
        response = self.app.delete("{}/api/v1/events/{}".format(BASE_URL, event_id))
        self.assertEqual(response.status_code, 200)

    def test_delete_wrong_id(self):
        event_id = "9494fds"
        response = self.app.delete("{}/api/v1/events/{}".format(BASE_URL, event_id))
        self.assertEqual(response.status_code, 404)

    def test_rsvp_wrong_id(self):
        event_id = "9494fds"
        response = self.app.post("{}/api/v1/events/{}/rsvp".format(BASE_URL, event_id))
        self.assertEqual(response.status_code, 404)

    def test_successful_rsvp(self):
        event_id = "9494"
        response = self.app.post("{}/api/v1/events/{}/rsvp".format(BASE_URL, event_id))
        self.assertEqual(response.status_code, 200)

    def test_retrieve_guest_successful(self):
        event_id = 9494
        response = self.app.get("{}/api/v1/events/{}/guests".format(BASE_URL, event_id))
        data = json.loads(response.get_data())
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(data["attendees"]), 6)

    def test_retrieve_guest_unsuccessful(self):
        event_id = 99494
        response = self.app.get("{}/api/v1/events/{}/guests".format(BASE_URL, event_id))
        self.assertEqual(response.status_code, 404)




