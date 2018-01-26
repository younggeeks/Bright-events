from api.helpers.AuthHttpHelpers import AuthHttpHelpers
from tests.BaseTest import BaseTestCase


class UserRegistrationTestCase(BaseTestCase):
    def setUp(self):
        super(UserRegistrationTestCase, self).setUp()
        self.http_helpershttp_helpers = AuthHttpHelpers(client=self.http_helpersclient)
