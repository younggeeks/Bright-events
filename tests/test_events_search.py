from api.helpers.EventsHttpHelpers import EventsHttpHelper
from api.helpers.tests_dummy_data import correct_event
from tests.BaseTest import BaseTestCase


class EventsSearchTestCase(BaseTestCase):
    def setUp(self):
        super(EventsSearchTestCase, self).setUp()
        self.http_helpers = EventsHttpHelper(client=self.client)


    def test_search_event_name_successfully(self):
        self.http_helpers.register(correct_event, token=self.http_helpers.get_token())
        response = self.http_helpers.search(search_by="name", query=correct_event["name"])

        self.assertEqual(response["status"], 200)
        self.assertEqual(response["data"]["message"], "Successfully Retrieved Events Matching Coders Campusess")


    def test_search_event_location_successfully(self):
        self.http_helpers.register(correct_event, token=self.http_helpers.get_token())
        response = self.http_helpers.search(search_by="location", query="Magomeni")

        self.assertEqual(response["status"], 200)
        self.assertEqual(response["data"]["message"], "Successfully Retrieved Events Matching Magomeni")
    #

    def test_search_query_not_found(self):
        self.http_helpers.register(correct_event, token=self.http_helpers.get_token())
        response = self.http_helpers.search(search_by="location")
        self.assertEqual(response["status"], 400)
        self.assertEqual(response["data"]["message"], "Query Not Specified, Search Failed")


    def test_search_event_not_found(self):
        self.http_helpers.register(correct_event, token=self.http_helpers.get_token())
        response = self.http_helpers.search(search_by="location", query="Mwananyamala")
        self.assertEqual(response["status"], 404)
        self.assertEqual(response["data"]["message"], "Event Matching Mwananyamala Was not found")


    def test_pagination_success(self):
        self.http_helpers.register(correct_event, token=self.http_helpers.get_token())
        response = self.http_helpers.paginate()
        events = response["data"]["events"]
        self.assertEqual(response["status"], 200)
        self.assertEqual(isinstance(events, list), True)


    def test_pagination_success_offset_4(self):
        self.http_helpers.register(correct_event, token=self.http_helpers.get_token())
        response = self.http_helpers.paginate(offset=4)
        events = response["data"]["events"]
        self.assertEqual(response["status"], 200)
        self.assertEqual(isinstance(events, list), True)


    def test_pagination_no_events(self):
        response = self.http_helpers.paginate()
        self.assertEqual(response["status"], 200)
        self.assertEqual(response["data"]["message"], "It seems there no events in the system")
