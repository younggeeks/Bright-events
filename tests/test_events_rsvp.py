from api.helpers.EventsHttpHelpers import EventsHttpHelper
from api.helpers.tests_dummy_data import correct_user, correct_event, correct_user2
from tests.BaseTest import BaseTestCase


class EventRSVP(BaseTestCase):
    def setUp(self):
        super(EventRSVP, self).setUp()
        self.http_helpers = EventsHttpHelper(client=self.client)


    def test_rsvp_successful(self):
        token = self.http_helpers.get_token(user=correct_user)
        self.http_helpers.register(correct_event, token=token)
        token2 = self.http_helpers.get_token(user=correct_user2)
        response = self.http_helpers.rsvp(token=token2)
        self.assertEqual(response["status"], 200)
        self.assertEqual(response["data"]["message"], "RSVP successfully")

    def test_rsvp_missing_field(self):
        token = self.http_helpers.get_token(user=correct_user)
        self.http_helpers.register(correct_event, token=token)
        token2 = self.http_helpers.get_token(user=correct_user2)
        response = self.http_helpers.rsvp(token=token2, empty_field=True)
        self.assertEqual(response["status"], 400)
        self.assertEqual(response["data"]["message"], "RSVP Failed, Please check your input")

    def test_rsvp_event_not_found(self):
        token = self.http_helpers.get_token(user=correct_user)
        self.http_helpers.register(correct_event, token=token)
        token2 = self.http_helpers.get_token(user=correct_user2)
        response = self.http_helpers.rsvp(token=token2, event_id=4)
        self.assertEqual(response["status"], 404)
        self.assertEqual(response["data"]["message"], "Event With ID 4 is not found")

    def test_rsvp_forbidden(self):
        token = self.http_helpers.get_token(user=correct_user)
        self.http_helpers.register(correct_event, token=token)
        response = self.http_helpers.rsvp(token=token)
        self.assertEqual(response["status"], 403)
        self.assertEqual(response["data"]["message"], "You can not RSVP To your own event")

    def test_rsvp_already_in_the_list(self):
        token = self.http_helpers.get_token(user=correct_user)
        self.http_helpers.register(correct_event, token=token)
        token2 = self.http_helpers.get_token(user=correct_user2)
        self.http_helpers.rsvp(token=token2)
        response = self.http_helpers.rsvp(token=token2)
        self.assertEqual(response["status"], 403)
        self.assertEqual(response["data"]["message"], "Your Name is already in Coders Campusess's Guest List")
