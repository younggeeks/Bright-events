from api.helpers.EventsHttpHelpers import EventsHttpHelper
from api.helpers.tests_dummy_data import correct_event, missing_field_event, correct_user, correct_user2
from tests.BaseTest import BaseTestCase
from tests.EventsBaseTest import EventBaseTestCase


class EventCrud(BaseTestCase):

    def setUp(self):
        super(EventCrud, self).setUp()
        self.http_helpers = EventsHttpHelper(client=self.client)

    def test_fetch_all_events(self):

        """ Tests the retrieval of all events """
        response = self.http_helpers.fetch_all()
        self.assertEqual(response["status"], 200)
        self.assertEqual(response["data"]["message"], "Events Retrieved Successfully")

    def test_register_missing_token(self):

        """Tests to see whether endpoint will return error if token is missing"""
        response = self.http_helpers.register(correct_event)
        self.assertEqual(response["status"], 401)
        self.assertEqual(response["data"]["message"], "Token is missing")


    def test_register_missing_field(self):

        response = self.http_helpers.register(missing_field_event, token=self.http_helpers.get_token())
        self.assertEqual(response["status"], 400)
        self.assertEqual(response["data"]["message"], "The following Required Field(s) are Missing: name")

    def test_register_successful(self):

        response = self.http_helpers.register(correct_event, token=self.http_helpers.get_token())
        self.assertEqual(response["status"], 201)
        self.assertEqual(response["data"]["message"], "Event Registration Successfully")

    def test_register_duplicate_event_name(self):

        self.http_helpers.register(correct_event, token=self.http_helpers.get_token())
        response = self.http_helpers.register(correct_event, token=self.http_helpers.get_token())
        self.assertEqual(response["status"], 400)
        self.assertEqual(response["data"]["message"], "Event Name Must be Unique")

    def test_update_event_successful(self):
        token = self.http_helpers.get_token()
        self.http_helpers.register(correct_event, token=token)
        response = self.http_helpers.update(token=token)
        self.assertEqual(response["status"], 200)
        self.assertEqual(response["data"]["message"], "Event Updated Successfully")

    def test_update_event_not_found(self):
        token = self.http_helpers.get_token(user=correct_user)
        self.http_helpers.register(correct_event, token=token)
        response = self.http_helpers.update(token=token, event_id=3)
        self.assertEqual(response["status"], 404)
        self.assertEqual(response["data"]["message"], "Event With ID 3 is not found")

    def test_update_event_only_update_your_events(self):
        token = self.http_helpers.get_token(user=correct_user)
        self.http_helpers.register(correct_event, token=token)
        token2 = self.http_helpers.get_token(user=correct_user2)
        response = self.http_helpers.update(token=token2)
        self.assertEqual(response["status"], 403)
        self.assertEqual(response["data"]["message"], "You can only Update Events You Created")

    def test_update_event_missing_fields(self):
        token = self.http_helpers.get_token(user=correct_user)
        self.http_helpers.register(correct_event, token=token)
        response = self.http_helpers.update(token=token, empty=True)
        self.assertEqual(response["status"], 400)
        self.assertEqual(response["data"]["message"], "Update Failed, Please check your input")

    def test_fetch_single_event_successful(self):
        token = self.http_helpers.get_token(user=correct_user)
        self.http_helpers.register(correct_event, token=token)
        response = self.http_helpers.fetch_one()
        self.assertEqual(response["status"], 200)
        self.assertEqual(response["data"]["message"], "Event Retrieved Successfully")

    def test_fetch_single_event_not_found(self):
        response = self.http_helpers.fetch_one(event_id=3)
        self.assertEqual(response["status"], 404)
        self.assertEqual(response["data"]["message"], "Event With ID 3 is not found")

    def test_delete_event_not_found(self):
        token = self.http_helpers.get_token(user=correct_user)
        self.http_helpers.register(correct_event, token=token)
        response = self.http_helpers.delete(token=token, event_id=3)
        self.assertEqual(response["status"], 404)
        self.assertEqual(response["data"]["message"], "Event With ID 3 is not found")

    def test_delete_event_successful(self):
        token = self.http_helpers.get_token(user=correct_user)
        self.http_helpers.register(correct_event, token=token)
        response = self.http_helpers.delete(token=token)
        self.assertEqual(response["status"], 200)
        self.assertEqual(response["data"]["message"], "Event Deletion Successful")

    def test_delete_event_forbidden(self):
        token = self.http_helpers.get_token(user=correct_user)
        self.http_helpers.register(correct_event, token=token)
        token2 = self.http_helpers.get_token(user=correct_user2)
        response = self.http_helpers.delete(token=token2)
        self.assertEqual(response["status"], 403)
        self.assertEqual(response["data"]["message"], "You can only Delete Events You Created")


