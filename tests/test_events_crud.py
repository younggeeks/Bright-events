from api.helpers.EventsHttpHelpers import EventsHttpHelper
from api.helpers.tests_dummy_data import correct_event, missing_field_event, correct_user, correct_user2
from tests.BaseTest import BaseTestCase
from tests.EventsBaseTest import EventBaseTestCase


class EventCrud(BaseTestCase):

    def setUp(self):
        """
        We make initial configurations before running the tests
        We make sure to run setUp() from super class first
        and then we add our file specific variable(http_helper)
        :return:
        :return:
        """
        super(EventCrud, self).setUp()
        self.http_helpers = EventsHttpHelper(client=self.client)

    def test_fetch_all_events(self):
        """
        User Should be able to see all the posted events
        :return json :
        """
        response = self.http_helpers.fetch_all()
        self.assertEqual(response["status"], 200)
        self.assertEqual(response["data"]["message"], "Events Retrieved Successfully")

    def test_register_missing_token(self):
        """
        User should get 401 status code with relevant message when the token is
        missing from the header
        :return:
        """
        response = self.http_helpers.register(correct_event)
        self.assertEqual(response["status"], 401)
        self.assertEqual(response["data"]["message"], "Token is missing")


    def test_register_missing_field(self):
        """
        Upon registering an event if one of the required fields is missing, user should get 400
        status code with relevant message
        :return:
        """
        response = self.http_helpers.register(missing_field_event, token=self.http_helpers.get_token())
        self.assertEqual(response["status"], 400)
        self.assertEqual(response["data"]["message"], "The following Required Field(s) are Missing: name")

    def test_register_successful(self):
        """
        User should be able to register(Post) an event , provided all the required fields are
        correctly entered
        :return:
        """
        response = self.http_helpers.register(correct_event, token=self.http_helpers.get_token())
        self.assertEqual(response["status"], 201)
        self.assertEqual(response["data"]["message"], "Event Registration Successfully")

    def test_register_duplicate_event_name(self):
        """
        When User tries to register an event with the name that already exists in the database
        they should get 400 status code with relevant message
        :return:
        """
        self.http_helpers.register(correct_event, token=self.http_helpers.get_token())
        response = self.http_helpers.register(correct_event, token=self.http_helpers.get_token())
        self.assertEqual(response["status"], 400)
        self.assertEqual(response["data"]["message"], "Event Name Must be Unique")

    def test_update_event_successful(self):
        """
        Provided user has entered all valid inputs they should be able to update an event
        they've created
        :return:
        """
        token = self.http_helpers.get_token()
        self.http_helpers.register(correct_event, token=token)
        response = self.http_helpers.update(token=token)
        self.assertEqual(response["status"], 200)
        self.assertEqual(response["data"]["message"], "Event Updated Successfully")

    def test_update_event_not_found(self):
        """
        When User tries to update an event which does not exist in the database
        they should get 404 status code with relevant message
        :return:
        """
        token = self.http_helpers.get_token(user=correct_user)
        self.http_helpers.register(correct_event, token=token)
        response = self.http_helpers.update(token=token, event_id=3)
        self.assertEqual(response["status"], 404)
        self.assertEqual(response["data"]["message"], "Event With ID 3 is not found")

    def test_update_event_only_update_your_events(self):
        """
        When User tries to update an event they have'nt created they should
        get 403 status code with relevant message
        :return:
        """
        token = self.http_helpers.get_token(user=correct_user)
        self.http_helpers.register(correct_event, token=token)
        token2 = self.http_helpers.get_token(user=correct_user2)
        response = self.http_helpers.update(token=token2)
        self.assertEqual(response["status"], 403)
        self.assertEqual(response["data"]["message"], "You can only Update Events You Created")

    def test_update_event_missing_fields(self):
        """
        When Updating an event user should provide all the required fields
        otherwise they should get 400 status code with relevant message
        :return:
        """
        token = self.http_helpers.get_token(user=correct_user)
        self.http_helpers.register(correct_event, token=token)
        response = self.http_helpers.update(token=token, empty=True)
        self.assertEqual(response["status"], 400)
        self.assertEqual(response["data"]["message"], "Update Failed, Please check your input")

    def test_fetch_single_event_successful(self):
        """
        User should get be able to view a single event
        :return:
        """
        token = self.http_helpers.get_token(user=correct_user)
        self.http_helpers.register(correct_event, token=token)
        response = self.http_helpers.fetch_one()
        self.assertEqual(response["status"], 200)
        self.assertEqual(response["data"]["message"], "Event Retrieved Successfully")

    def test_fetch_single_event_not_found(self):
        """
        When User tries to view an event that does not exist they should get
        404 status code with relevant message
        :return:
        """
        response = self.http_helpers.fetch_one(event_id=3)
        self.assertEqual(response["status"], 404)
        self.assertEqual(response["data"]["message"], "Event With ID 3 is not found")

    def test_delete_event_not_found(self):
        """
        When User tries to delete an event with an Id that does not exist
        they should get 404 status code with relevant message
        :return:
        """
        token = self.http_helpers.get_token(user=correct_user)
        self.http_helpers.register(correct_event, token=token)
        response = self.http_helpers.delete(token=token, event_id=3)
        self.assertEqual(response["status"], 404)
        self.assertEqual(response["data"]["message"], "Event With ID 3 is not found")

    def test_delete_event_successful(self):
        """
        When Event exists and the user is the owner of specified event
        then user should get 200 status code with relevant message
        :return:
        """
        token = self.http_helpers.get_token(user=correct_user)
        self.http_helpers.register(correct_event, token=token)
        response = self.http_helpers.delete(token=token)
        self.assertEqual(response["status"], 200)
        self.assertEqual(response["data"]["message"], "Event Deletion Successful")

    def test_delete_event_forbidden(self):
        """
        When User tries to delete an event and they are not the owner
        they should get 403 status code with relevant message
        :return:
        """
        token = self.http_helpers.get_token(user=correct_user)
        self.http_helpers.register(correct_event, token=token)
        token2 = self.http_helpers.get_token(user=correct_user2)
        response = self.http_helpers.delete(token=token2)
        self.assertEqual(response["status"], 403)
        self.assertEqual(response["data"]["message"], "You can only Delete Events You Created")


