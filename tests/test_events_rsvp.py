from api.helpers.EventsHttpHelpers import EventsHttpHelper
from api.helpers.tests_dummy_data import correct_user, correct_event, correct_user2
from tests.BaseTest import BaseTestCase


class EventRSVP(BaseTestCase):
    def setUp(self):
        """
        We make initial configurations before running the tests
        We make sure to run setUp() from super class first
        and then we add our file specific variable(http_helper)
        :return:
        """
        super(EventRSVP, self).setUp()
        self.http_helpers = EventsHttpHelper(client=self.client)


    def test_rsvp_successful(self):
        """
        Authenticated users should be able to rsvp to an event
        :return:
        """
        token = self.http_helpers.get_token(user=correct_user)
        self.http_helpers.register(correct_event, token=token)
        token2 = self.http_helpers.get_token(user=correct_user2)
        response = self.http_helpers.rsvp(token=token2)
        self.assertEqual(response["status"], 200)
        self.assertEqual(response["data"]["message"], "RSVP successfully")

    def test_rsvp_missing_field(self):
        """
        When User does not specify an event id they should get
        400 status code with relevant error message
        :return:
        """
        token = self.http_helpers.get_token(user=correct_user)
        self.http_helpers.register(correct_event, token=token)
        token2 = self.http_helpers.get_token(user=correct_user2)
        response = self.http_helpers.rsvp(token=token2, empty_field=True)
        self.assertEqual(response["status"], 400)
        self.assertEqual(response["data"]["message"], "RSVP Failed, Please check your input")

    def test_rsvp_event_not_found(self):
        """
        When User tries to rsvp to an event which does not exist
        They should get 404 status code with relevant error message
        :return:
        """
        token = self.http_helpers.get_token(user=correct_user)
        self.http_helpers.register(correct_event, token=token)
        token2 = self.http_helpers.get_token(user=correct_user2)
        response = self.http_helpers.rsvp(token=token2, event_id=4)
        self.assertEqual(response["status"], 404)
        self.assertEqual(response["data"]["message"], "Event With ID 4 is not found")

    def test_rsvp_forbidden(self):
        """
        User should not be allowed to rsvp to the events they've created
        :return:
        """
        token = self.http_helpers.get_token(user=correct_user)
        self.http_helpers.register(correct_event, token=token)
        response = self.http_helpers.rsvp(token=token)
        self.assertEqual(response["status"], 403)
        self.assertEqual(response["data"]["message"], "You can not RSVP To your own event")

    def test_rsvp_already_in_the_list(self):
        """
        User should not be allowed to rsvp more than once
        
        :return:
        """
        token = self.http_helpers.get_token(user=correct_user)
        self.http_helpers.register(correct_event, token=token)
        token2 = self.http_helpers.get_token(user=correct_user2)
        self.http_helpers.rsvp(token=token2)
        response = self.http_helpers.rsvp(token=token2)
        self.assertEqual(response["status"], 403)
        self.assertEqual(response["data"]["message"], "Your Name is already in Coders Campusess's Guest List")
