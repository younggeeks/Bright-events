from api.helpers.AuthHttpHelpers import AuthHttpHelpers
from api.helpers.tests_dummy_data import correct_user, wrong_input_user
from tests.BaseTest import BaseTestCase


class UserRegistrationTestCase(BaseTestCase):
    def setUp(self):
        super(UserRegistrationTestCase, self).setUp()
        self.http_helpers = AuthHttpHelpers(client=self.client)

    def test_register_successful(self):
        response = self.http_helpers.user_registration(correct_user)
        self.assertEqual(response["status"], 201)
        self.assertEqual(response["data"]["message"], "Successfully Registered")

    def test_register_email_exists(self):
        self.http_helpers.user_registration(correct_user)
        response = self.http_helpers.user_registration(correct_user)
        self.assertEqual(response["status"], 401)
        self.assertEqual(response["data"]["message"], "User Already Exists, Please Login")

    def test_wrong_registration_input(self):
        response = self.http_helpers.user_registration(wrong_input_user)
        self.assertEqual(response["status"], 400)
        self.assertEqual(response["data"]["message"], "The following Required Field(s) are Missing: email")
