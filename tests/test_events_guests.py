from api.helpers.EventsHttpHelpers import EventsHttpHelper
from api.helpers.tests_dummy_data import correct_event, correct_user, correct_user2
from tests.BaseTest import BaseTestCase
from tests.EventsBaseTest import EventBaseTestCase


class EventGuestsTestCase(BaseTestCase):
    def setUp(self):
        """
        We make initial configurations before running the tests
        We make sure to run setUp() from super class first
        and then we add our file specific variable(http_helper)
        :return:
        """
        super(EventGuestsTestCase, self).setUp()
        self.http_helpers = EventsHttpHelper(client=self.client)


    def test_retrieve_guest_list_successful(self):
        """
        Owners of a specified event should be able to retrieve event guests
        :return:
        """
        token = self.http_helpers.get_token(user=correct_user)
        self.http_helpers.register(correct_event, token=token)
        response = self.http_helpers.guests(token=token)
        self.assertEqual(response["status"], 200)
        self.assertEqual(response["data"]["message"], "Successfully Retrieved Event Guests")

    def test_retrieve_guest_list_event_not_found(self):
        """
        If User tries to retrieve guests of an event that doesn't exist
        User should get 404 status code and relevant error message
        :return:
        """
        token = self.http_helpers.get_token(user=correct_user)
        self.http_helpers.register(correct_event, token=token)
        response = self.http_helpers.guests(token=token, event_id=3)
        self.assertEqual(response["status"], 404)
        self.assertEqual(response["data"]["message"], "Event With ID 3 is not found")

    def test_retrieve_guest_list_forbidden(self):
        """
        User should be able to see guests of an event they've created
        :return:
        """
        token = self.http_helpers.get_token(user=correct_user)
        self.http_helpers.register(correct_event, token=token)
        token2 = self.http_helpers.get_token(user=correct_user2)
        response = self.http_helpers.guests(token=token2)
        self.assertEqual(response["status"], 403)
        self.assertEqual(response["data"]["message"], "You can only See the guests of the event you created")
