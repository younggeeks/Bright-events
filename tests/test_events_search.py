from api.helpers.EventsHttpHelpers import EventsHttpHelper
from api.helpers.tests_dummy_data import correct_event
from tests.BaseTest import BaseTestCase


class EventsSearchTestCase(BaseTestCase):
    def setUp(self):
        """
        We make initial configurations before running the tests
        We make sure to run setUp() from super class first
        and then we add our file specific variable(http_helper)
        :return:
        """
        super(EventsSearchTestCase, self).setUp()
        self.http_helpers = EventsHttpHelper(client=self.client)


    def test_search_event_name_successfully(self):
        """
        User should be able to filter events by name
        :return:
        """
        self.http_helpers.register(correct_event, token=self.http_helpers.get_token())
        response = self.http_helpers.search(search_by="name", query=correct_event["name"])
        self.assertEqual(response["status"], 200)
        self.assertEqual(response["data"]["message"], "Successfully Retrieved Events Matching Coders Campusess")


    def test_search_event_location_successfully(self):
        """
        User should be able to filter locations according to address
        :return:
        """
        self.http_helpers.register(correct_event, token=self.http_helpers.get_token())
        response = self.http_helpers.search(search_by="location", query="Magomeni")
        self.assertEqual(response["status"], 200)
        self.assertEqual(response["data"]["message"], "Successfully Retrieved Events Matching Magomeni")
    #

    def test_search_query_not_found(self):
        """
        When User tries to search without search query
        User should get 400 status code with relevant error message
        :return:
        """
        self.http_helpers.register(correct_event, token=self.http_helpers.get_token())
        response = self.http_helpers.search(search_by="location")
        self.assertEqual(response["status"], 400)
        self.assertEqual(response["data"]["message"], "Query Not Specified, Search Failed")


    def test_search_event_not_found(self):
        """
        When None of the registered events matches the search query
        User should get 404 status code with relevant error message
        :return:
        """
        self.http_helpers.register(correct_event, token=self.http_helpers.get_token())
        response = self.http_helpers.search(search_by="location", query="Mwananyamala")
        self.assertEqual(response["status"], 404)
        self.assertEqual(response["data"]["message"], "Event Matching Mwananyamala Was not found")


    def test_pagination_success(self):
        """
        User should be able to decide the number of events they want in a single fetch
        :return:
        """
        self.http_helpers.register(correct_event, token=self.http_helpers.get_token())
        response = self.http_helpers.paginate()
        events = response["data"]["events"]
        self.assertEqual(response["status"], 200)
        self.assertEqual(isinstance(events, list), True)


    def test_pagination_success_offset_4(self):
        """
        User should be able to specify the starting page when they are fetching events
        and number of events they want per single fetch
        :return:
        """
        self.http_helpers.register(correct_event, token=self.http_helpers.get_token())
        response = self.http_helpers.paginate(offset=4)
        events = response["data"]["events"]
        self.assertEqual(response["status"], 200)
        self.assertEqual(isinstance(events, list), True)


    def test_pagination_no_events(self):
        """
        When user tries to search but no event is registered in the database
        User should get 200 status with relevant message
        :return:
        """
        response = self.http_helpers.paginate()
        self.assertEqual(response["status"], 200)
        self.assertEqual(response["data"]["message"], "It seems there no events in the system")
