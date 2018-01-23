from api.helpers.EventsHttpHelpers import EventsHttpHelper


class EventCrud:
    def __init__(self, helpers):
        self.http_helpers = helpers

    def test_fetch_all_events(self):
        """ Tests the retrieval of all events """
        response = self.http_helpers.fetch_all()
        self.assertEqual(response["status"], 200)
        self.assertEqual(response["data"]["message"], "Events Retrieved Successfully")
