from flask import json

from api.helpers.AuthHttpHelpers import AuthHttpHelpers
from api.helpers.tests_dummy_data import correct_user, incorrect_reset_email, wrong_email_user, new_password, BASE_URL, \
    new_password_wrong, new_password_empty_fields, empty_input_user
from tests.BaseTest import BaseTestCase


class PasswordResetTestCase(BaseTestCase):
    def setUp(self):
        super(PasswordResetTestCase, self).setUp()
        self.http_helpers = AuthHttpHelpers(client=self.client)

    def test_send_password_reset_link_success(self):
        self.http_helpers.user_registration(correct_user)
        response = self.http_helpers.reset_link(email=correct_user["email"])
        data = json.loads(response.data.decode())

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data["message"], "Password Reset Link Successfully Generated")

    def test_password_reset_email_not_found(self):
        response = self.http_helpers.reset_link(email=incorrect_reset_email)
        data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 404)
        self.assertEqual(data["message"], "Email not found , Password reset Failed")

    def test_password_reset_missing_input(self):
        response = self.http_helpers.reset_link()
        data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 400)
        self.assertEqual(data["message"], "Email field is required, Password Reset failed")

    def test_password_reset_verify_token_successful(self):
        verification = self.http_helpers.do_verify_token(correct_user)
        self.assertEqual(verification["status"], 200)
        self.assertEqual(verification["data"]["message"], "Password Reset Link Verified Successfully")

    def test_password_reset_verify_token_email_not_found(self):
        verification = self.http_helpers.do_verify_token(wrong_email_user)
        self.assertEqual(verification["status"], 404)
        self.assertEqual(verification["data"]["message"], "Email not found , Password reset Failed")

    def test_password_reset_verify_token_invalid_or_expired_token(self):
        verification = self.http_helpers.do_verify_token(correct_user, correct=False)
        self.assertEqual(verification["status"], 400)
        self.assertEqual(verification["data"]["message"], "Password Reset Link is invalid, or Expired")

    def test_password_reset_change_password_successful(self):
        verification = self.http_helpers.do_verify_token(correct_user)
        token = verification["data"]["token"]
        response_get = self.http_helpers.client.get("{}/api/v1/auth/reset-password/{}".format(BASE_URL, token))
        data = json.loads(response_get.data.decode())
        new_token = data["token"]
        response = self.http_helpers.client.post("{}/api/v1/auth/reset-password/{}".format(BASE_URL, new_token),
                                                 data=json.dumps(new_password), content_type="application/json")
        data = json.loads(response.data.decode())
        print(data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data["message"], "Password Reset Successfully")

    def test_password_reset_change_password_not_matching_password_confirmation(self):
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

    def test_password_reset_change_password_missing_data(self):
        verification = self.http_helpers.do_verify_token(correct_user)
        token = verification["data"]["token"]
        response_get = self.http_helpers.client.get("{}/api/v1/auth/reset-password/{}".format(BASE_URL, token))
        data = json.loads(response_get.data.decode())
        new_token = data["token"]
        response = self.http_helpers.client.post("{}/api/v1/auth/reset-password/{}".format(BASE_URL, new_token),
                                                 data=json.dumps(empty_input_user), content_type="application/json")
        data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 400)
        self.assertEqual(data["message"], "The following Required Field(s) are Missing: password_confirmation")
