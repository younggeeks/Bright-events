from api.helpers.EventsHttpHelpers import EventsHttpHelper
from tests.BaseTest import BaseTestCase


class EventBaseTestCase(BaseTestCase):
    def __init__(self, *args, **kwargs):
        super(EventBaseTestCase, self).__init__(*args, **kwargs)
        self.http_helpers = EventsHttpHelper(client=self.client)

    def setUp(self):
        super(EventBaseTestCase, self).setUp()
        self.http_helpers = EventsHttpHelper(client=self.client)
