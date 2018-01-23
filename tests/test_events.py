import unittest
from api import create_app, db
from api.helpers.EventsHttpHelpers import EventsHttpHelper
from api.helpers.tests_dummy_data import correct_event, correct_user, missing_field_event, \
    correct_user2
from api.models import Category
from tests.test_events_crud import EventCrud


class EventsTester(unittest.TestCase):
    """
    Tests Events Endpoints (creates sample category for testing first)
    Instantiates EventsHttpHelper class with all http test methods
    """
    def setUp(self):
        self.category = Category(name="noma sana")
        self.app = create_app("testing")
        self.client = self.app.test_client()
        self.test_db = db.init_app(self.app)
        self.http_helpers = EventsHttpHelper(client=self.client)
        self.test_crud = EventCrud(self.http_helpers)
        with self.app.app_context():
            db.init_app(self.app)
            db.drop_all()
            db.create_all()
            db.session.add(self.category)
            db.session.commit()

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
        self.assertEqual(response["data"]["message"], "Event Registration failed, Please check your input")

    def test_register_successful(self):
        response = self.http_helpers.register(correct_event, token=self.http_helpers.get_token())
        self.assertEqual(response["status"], 201)
        self.assertEqual(response["data"]["message"], "Event Registration Successfully")

    def test_register_duplicate_event_name(self):
        self.http_helpers.register(correct_event, token=self.http_helpers.get_token())
        response = self.http_helpers.register(correct_event, token=self.http_helpers.get_token())
        self.assertEqual(response["status"], 400)
        self.assertEqual(response["data"]["message"], "Event name must be unique")

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

    def test_retrieve_guest_list_successful(self):
        token = self.http_helpers.get_token(user=correct_user)
        self.http_helpers.register(correct_event, token=token)
        response = self.http_helpers.guests(token=token)
        self.assertEqual(response["status"], 200)
        self.assertEqual(response["data"]["message"], "Successfully Retrieved Event Guests")

    def test_retrieve_guest_list_successful(self):
        token = self.http_helpers.get_token(user=correct_user)
        self.http_helpers.register(correct_event, token=token)
        response = self.http_helpers.guests(token=token)
        self.assertEqual(response["status"], 200)
        self.assertEqual(response["data"]["message"], "Successfully Retrieved Event Guests")

    def test_retrieve_guest_list_event_not_found(self):
        token = self.http_helpers.get_token(user=correct_user)
        self.http_helpers.register(correct_event, token=token)
        response = self.http_helpers.guests(token=token, event_id=3)
        self.assertEqual(response["status"], 404)
        self.assertEqual(response["data"]["message"], "Event With ID 3 is not found")

    def test_retrieve_guest_list_forbidden(self):
        token = self.http_helpers.get_token(user=correct_user)
        self.http_helpers.register(correct_event, token=token)
        token2 = self.http_helpers.get_token(user=correct_user2)
        response = self.http_helpers.guests(token=token2)
        self.assertEqual(response["status"], 403)
        self.assertEqual(response["data"]["message"], "You can only See the guests of the event you created")

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
