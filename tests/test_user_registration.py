from api.helpers.AuthHttpHelpers import AuthHttpHelpers
from api.helpers.tests_dummy_data import correct_user, wrong_input_user, invalid_email_user
from tests.BaseTest import BaseTestCase


class UserRegistrationTestCase(BaseTestCase):
    def setUp(self):
        """
        We make initial configurations before running the tests
        We make sure to run setUp() from super class first
        and then we add our file specific variable(http_helper)
        :return:
        """
        super(UserRegistrationTestCase, self).setUp()
        self.http_helpers = AuthHttpHelpers(client=self.client)

    def test_register_successful(self):
        """
        Upon should be able to create and account
        :return:
        """
        response = self.http_helpers.user_registration(correct_user)
        self.assertEqual(response["status"], 201)
        self.assertEqual(response["data"]["message"], "Successfully Registered")

    def test_register_wrong_email_format(self):
        """
        User registration should fail when wrong email format is entered
        and 400 status code with relevant message should be the response
        :return:
        """
        response = self.http_helpers.user_registration(invalid_email_user)
        self.assertEqual(response["status"], 400)
        self.assertEqual(response["data"]["message"], "{} is invalid Email Address".format(invalid_email_user[
                                                                                               'email']))

    def test_register_email_exists(self):
        """
        When User tries to register new account with email that already exists
        they should get 401 status code with relevant error message
        :return:
        """
        self.http_helpers.user_registration(correct_user)
        response = self.http_helpers.user_registration(correct_user)
        self.assertEqual(response["status"], 401)
        self.assertEqual(response["data"]["message"], "User Already Exists, Please Login")

    def test_wrong_registration_input(self):
        """
        When user enters wrong inputs they should get 400 status code and relevant error message
        :return:
        """
        response = self.http_helpers.user_registration(wrong_input_user)
        self.assertEqual(response["status"], 400)
        self.assertEqual(response["data"]["message"], "The following Required Field(s) are Missing: email")
