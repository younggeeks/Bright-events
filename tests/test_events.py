import json
import unittest
from database.data_mocks import DataMocks
import app
from settings import BASE_URL


class UsersTester(unittest.TestCase):
    pass


class EventTester(unittest.TestCase):
    def setUp(self):
        self.app = app.app.test_client()
        app.app.testing = True

    def test_afetch_events(self):
        response = self.app.get("{}/api/v1/events".format(BASE_URL))
        data = json.loads(response.get_data())
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(data["events"]), 5)

    def test_afetch_reports(self):
        user = "sam"
        response = self.app.get("{}/api/v1/events/{}/charts".format(BASE_URL, user))
        self.assertEqual(response.status_code, 200)

    def test_bsave_event_successfully(self):
        event = {
            "name": "new event",
            "address": "nairobi",
            "start_date": "4/2/201",
            "end_date": "3/34/3434",
            "description": ".l3dfkasdjfklasdjfkljalskdjflkasdfas",
            "user": "Masoud Masoud",
            "id": "4894509430",
            "price": "free",
            "category": " Wedding"
        }

        # testing if it returns number of events in our list
        self.assertEqual(len(DataMocks.events), 5)
        response = self.app.post("{}/api/v1/events".format(BASE_URL),
                                 data=json.dumps(event), content_type='application/json')

        # testing if adding event is successful
        self.assertEqual(response.status_code, 201)

        # testing if adding new user increases length of out list
        self.assertEqual(len(DataMocks.events), 6)

    def test_cduplicate_event_name(self):
        event = {
            "name": "Mobile Museum of Art",
            "address": "nairobi",
            "start_date": "4/2/201",
            "end_date": "3/34/3434",
            "description": ".l3dfkasdjfklasdjfkljalskdjflkasdfas",
            "user": "Masoud Masoud",
            "id": "4894509430",
            "price": "Free",
            "category": " Wedding"
        }
        response = self.app.post("{}/api/v1/events".format(BASE_URL),
                                 data=json.dumps(event), content_type='application/json')
        self.assertEqual(response.status_code, 400)

    def test_esuccessful_updating_event(self):
        event = {
            "name": "Angular Conference 2018",
            "address": "ijumaa",
            "id": "9494",
            "category": " Wedding",
            "start_date": "1/2/323",
            "end_date": "1/3/343",
            "user": "Samaki",
            "price": "frees",
            "description": "awesome event You would'nt want to miss it"
        }
        response = self.app.put("{}/api/v1/events/{}".format(BASE_URL, event["id"]),
                                data=json.dumps(event), content_type='application/json')
        self.assertEqual(response.status_code, 200)

    def test_fid_not_found_updating_event(self):
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

    def test_gdelete_successful(self):
        event_id = 9494
        response = self.app.delete("{}/api/v1/events/{}".format(BASE_URL, event_id))
        self.assertEqual(response.status_code, 200)

    def test_hdelete_wrong_id(self):
        event_id = "9494fds"
        response = self.app.delete("{}/api/v1/events/{}".format(BASE_URL, event_id))
        self.assertEqual(response.status_code, 404)

    def test_irsvp_wrong_id(self):
        event_id = "9494fds"
        response = self.app.post("{}/api/v1/events/{}/rsvp".format(BASE_URL, event_id))
        self.assertEqual(response.status_code, 404)

    def test_zrsvp_correct_id(self):
        event_id = 5221
        data = {
            "user_id": 4
        }
        response = self.app.post("{}/api/v1/events/{}/rsvp".format(BASE_URL, event_id),
                                 data=json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 200)

    def test_irsvp_own_event(self):
        event_id = 894
        data = {"user_id": 2}
        response = self.app.post("{}/api/v1/events/{}/rsvp".format(BASE_URL, event_id),
                                 data=json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 400)

    def test_jsuccessful_rsvp(self):
        event_id = 5879
        data = {
            "user_id": 4
        }
        response = self.app.post("{}/api/v1/events/{}/rsvp".format(BASE_URL, event_id),
                                 data=json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 200)

    def test_j_rsvp_name_exists(self):
        event_id = 987
        data = {
            "user_id": 4
        }
        response = self.app.post("{}/api/v1/events/{}/rsvp".format(BASE_URL, event_id),
                                 data=json.dumps(data), content_type='application/json')

        self.assertEqual(response.status_code, 200)

    def test_kretrieve_guest_successful(self):
        event_id = 987
        response = self.app.get("{}/api/v1/events/{}/guests".format(BASE_URL, event_id))
        json.loads(response.get_data())
        self.assertEqual(response.status_code, 200)

    def test_lretrieve_guest_unsuccessful(self):
        event_id = 9949454
        response = self.app.get("{}/api/v1/events/{}/guests".format(BASE_URL, event_id))
        self.assertEqual(response.status_code, 404)

    def test_lretrieve_guest_ok_but_none(self):
        event_id = 5221
        response = self.app.get("{}/api/v1/events/{}/guests".format(BASE_URL, event_id))
        self.assertEqual(response.status_code, 200)

    def test_helper_methods(self):
        events = DataMocks.get_data("events")
        self.assertEqual(len(events), 5)
        users = DataMocks.get_data("users")
        self.assertEqual(len(users), 6)

        all_users = DataMocks.users

        all_users = DataMocks.get_data("users", all_users)

        self.assertEqual(len(all_users), 6)

    def test_404_response(self):
        response = self.app.get("{}/api/v1/eventasdfs/{}/guests")
        self.assertEqual(response.status_code, 404)

    def test_redirect_index(self):
        response = self.app.get("{}".format(BASE_URL))
        self.assertEqual(response.status_code, 301)

    def test_user_events_ok(self):
        response = self.app.get("{}/api/v1/sam/events".format(BASE_URL))
        self.assertEqual(response.status_code, 200)

    def test_user_events_404(self):
        response = self.app.get("{}/api/v1/samakid/events".format(BASE_URL))
        self.assertEqual(response.status_code, 404)

    def test_fetch_single_event_success(self):
        event_id = 894
        response = self.app.get("{}/api/v1/events/{}".format(BASE_URL, event_id))
        self.assertEqual(response.status_code, 200)

    def test_fetch_single_event_unsuccess(self):
        event_id = 88994
        response = self.app.get("{}/api/v1/events/{}".format(BASE_URL, event_id))

        self.assertEqual(response.status_code, 404)

    def test_fetch_guest_success(self):
        event_id = 9494
        response = self.app.get("{}/api/v1/events/{}/guests".format(BASE_URL, event_id))
        self.assertEqual(response.status_code, 200)

    def test_fetch_by_category_success(self):
        category = "Meetup"
        response = self.app.get("{}/api/v1/category/{}/events".format(BASE_URL, category))
        self.assertEqual(response.status_code, 200)

    def test_fetch_by_category_failed(self):
        category = "Meetuep"
        response = self.app.get("{}/api/v1/category/{}/events".format(BASE_URL, category))
        self.assertEqual(response.status_code, 404)









