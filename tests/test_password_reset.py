from flask import json

from api.helpers.AuthHttpHelpers import AuthHttpHelpers
from api.helpers.tests_dummy_data import correct_user, incorrect_reset_email, wrong_email_user, new_password, BASE_URL, \
    new_password_wrong, new_password_empty_fields, empty_input_user
from tests.BaseTest import BaseTestCase


class PasswordResetTestCase(BaseTestCase):
    def setUp(self):
        """
        We make initial configurations before running the tests
        We make sure to run setUp() from super class first
        and then we add our file specific variable(http_helper)
        :return:
        """
        super(PasswordResetTestCase, self).setUp()
        self.http_helpers = AuthHttpHelpers(client=self.client)

    def test_send_password_reset_link_success(self):
        """
        Users should be able to reset password upon entering their email, we check if it exists
        they should be able to get back reset link
        :return:
        """
        self.http_helpers.user_registration(correct_user)
        response = self.http_helpers.reset_link(email=correct_user["email"])
        data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data["message"], "Password Reset Link Successfully Generated")

    def test_password_reset_email_not_found(self):
        """
        User should get 404 response when they enter email that does not exist
        :return json:
        """
        response = self.http_helpers.reset_link(email=incorrect_reset_email)
        data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 404)
        self.assertEqual(data["message"], "Email not found , Password reset Failed")

    def test_password_reset_missing_input(self):
        """
        When Input(email) is missing user should get 400 status code with error message
        :return json:
        """
        response = self.http_helpers.reset_link()
        data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 400)
        self.assertEqual(data["message"], "Email field is required, Password Reset failed")

    def test_password_reset_verify_token_successful(self):
        """
        Upon clicking the link with valid token, user should be able to proceed to next
        step which is verifying the token before resetting the password
        :return:
        """
        verification = self.http_helpers.do_verify_token(correct_user)
        self.assertEqual(verification["status"], 200)
        self.assertEqual(verification["data"]["message"], "Password Reset Link Verified Successfully")

    def test_password_reset_verify_token_email_not_found(self):
        """
        When token link is clicked we check for integrity of data passed in passed token
        if email is not found user should get 404 status code with relevant message
        :return:
        """
        verification = self.http_helpers.do_verify_token(wrong_email_user)
        self.assertEqual(verification["status"], 404)
        self.assertEqual(verification["data"]["message"], "Email not found , Password reset Failed")

    def test_password_reset_verify_token_invalid_or_expired_token(self):
        """
        If token is invalid or expired user should get 400 status code with relevant message
        :return:
        """
        verification = self.http_helpers.do_verify_token(correct_user, correct=False)
        self.assertEqual(verification["status"], 400)
        self.assertEqual(verification["data"]["message"], "Password Reset Link is invalid, or Expired")

    def test_password_reset_change_password_successful(self):
        """
        If token passed is valid user should be able to enter their new password and password confirmation
        to reset the password
        :return:
        """
        verification = self.http_helpers.do_verify_token(correct_user)
        token = verification["data"]["token"]
        response_get = self.http_helpers.client.get("{}/api/v1/auth/reset-password/{}".format(BASE_URL, token))
        data = json.loads(response_get.data.decode())
        new_token = data["token"]
        response = self.http_helpers.client.post("{}/api/v1/auth/reset-password/{}".format(BASE_URL, new_token),
                                                 data=json.dumps(new_password), content_type="application/json")
        data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data["message"], "Password Reset Successfully")

    def test_password_reset_change_password_not_matching_password_confirmation(self):
        """
        When User Enters password that does not match password confirmation they should
        get  400 status code with relevant message
        :return:
        """
        verification = self.http_helpers.do_verify_token(correct_user)
        token = verification["data"]["token"]
        response_get = self.http_helpers.client.get("{}/api/v1/auth/reset-password/{}".format(BASE_URL, token))
        data = json.loads(response_get.data.decode())
        new_token = data["token"]
        response = self.http_helpers.client.post("{}/api/v1/auth/reset-password/{}".format(BASE_URL, new_token),
                                                 data=json.dumps(new_password_wrong), content_type="application/json")
        data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 400)
        self.assertEqual(data["message"], "Password and Password Confirmation do not match")

    def test_password_reset_change_password_missing_field(self):
        """
        When either of the required inputs(password,password_confirmation) is missing User should get 400 status code
        with relevant message
        :return:
        """
        verification = self.http_helpers.do_verify_token(correct_user)
        token = verification["data"]["token"]
        response_get = self.http_helpers.client.get("{}/api/v1/auth/reset-password/{}".format(BASE_URL, token))
        data = json.loads(response_get.data.decode())
        new_token = data["token"]
        response = self.http_helpers.client.post("{}/api/v1/auth/reset-password/{}".format(BASE_URL, new_token),
                                                 data=json.dumps({}), content_type="application/json")
        data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 400)
        self.assertEqual(data["message"], "The following Required Field(s) are Missing: password, password_confirmation")

    def test_password_reset_change_password_empty_field(self):
        """
        When the required fields exists but they are empty , User should get 400 status code
        with relevant message
        :return:
        """
        verification = self.http_helpers.do_verify_token(correct_user)
        token = verification["data"]["token"]
        response_get = self.http_helpers.client.get("{}/api/v1/auth/reset-password/{}".format(BASE_URL, token))
        data = json.loads(response_get.data.decode())
        new_token = data["token"]
        response = self.http_helpers.client.post("{}/api/v1/auth/reset-password/{}".format(BASE_URL, new_token),
                                                 data=json.dumps(new_password_empty_fields),
                                                 content_type="application/json")
        data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 400)
        self.assertEqual(data["message"], "The following Field(s) are Empty: password, password_confirmation")
