import json
import unittest

import time

from api import create_app, db
from api.helpers.AuthHttpHelpers import AuthHttpHelpers
from api.helpers.tests_dummy_data import BASE_URL, correct_user, wrong_input_user, empty_input_user, wrong_email_user, \
    wrong_password_user, incorrect_reset_email, new_password, new_password_wrong, new_password_empty_fields, \
    fake_link, fake_token, encode_token
from tests.BaseTest import BaseTestCase


class UserLoginTestCase(BaseTestCase):
    def setUp(self):
        super(UserLoginTestCase, self).setUp()
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

    def test_login_successful(self):
        self.http_helpers.user_registration(correct_user)
        response = self.http_helpers.login(correct_user)

        self.assertEqual(response["status"], 200)
        self.assertEqual(response["data"]["message"], "Login successful")

    def test_login_unsuccessful_missing_fields(self):
        response = self.http_helpers.login(wrong_input_user)

        self.assertEqual(response["status"], 400)
        self.assertEqual(response["data"]["message"], "The following Required Field(s) are Missing: email")

    def test_login_unsuccessful_empty_fields(self):
        response = self.http_helpers.login(empty_input_user)

        self.assertEqual(response["status"], 400)
        self.assertEqual(response["data"]["message"], "Email and password fields are required to login")

    def test_login_unsuccessful_wrong_email(self):
        response = self.http_helpers.login(wrong_email_user)

        self.assertEqual(response["status"], 401)
        self.assertEqual(response["data"]["message"],
                         "No Account is associated with Email juma@gmail.com, Login Failed")

    def test_login_unsuccessful_wrong_password(self):
        self.http_helpers.user_registration(correct_user)
        response = self.http_helpers.login(wrong_password_user)

        self.assertEqual(response["status"], 401)
        self.assertEqual(response["data"]["message"],
                         "Wrong Combination of Email and password, Login Failed")

    def test_logout_succesful(self):
        self.http_helpers.user_registration(correct_user)
        response = self.http_helpers.login(correct_user)

        logout_response = self.http_helpers.logout(response["data"]["token"])
        logout_data = json.loads(logout_response.data.decode())

        # testing if Logout is successful
        self.assertEqual(logout_response.status_code, 200)
        self.assertEqual(logout_data["message"], "Logout Successful")

    def test_logout_missing_token(self):
        logout_response = self.http_helpers.logout()
        logout_data = json.loads(logout_response.data.decode())

        self.assertEqual(logout_response.status_code, 401)
        self.assertEqual(logout_data["message"], "Token is missing from your header")

    def test_logout_already_signed_out(self):
        self.http_helpers.user_registration(correct_user)
        response = self.http_helpers.login(correct_user)
        token = response["data"]["token"]
        self.http_helpers.logout(token)

        second_logout_resp = self.http_helpers.logout(token)
        second_logout_data = json.loads(second_logout_resp.data.decode())

        self.assertEqual(second_logout_resp.status_code, 401)
        self.assertEqual(second_logout_data["message"], "User is already signed out")

    def test_logout_invalid_token(self):
        response = self.http_helpers.logout(fake_token)
        data = json.loads(response.data.decode())

        # testing if Logout is unsuccessful
        self.assertEqual(response.status_code, 400)
        self.assertEqual(data["message"], "Invalid Token , Please Login again")

    def test_logout_expired_token(self):
        token = encode_token()
        time.sleep(1)
        response = self.http_helpers.logout(token.decode())
        data = json.loads(response.data.decode())

        # testing if Logout is unsuccessful
        self.assertEqual(response.status_code, 400)
        self.assertEqual(data["message"], "Token Expired , Please Login Again")

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
        self.assertEqual(data["message"], "Password Reset failed, Please check your input")

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

        self.assertEqual(response.status_code, 401)
        self.assertEqual(data["message"], "Password and Password confirmation do not match")

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
        self.assertEqual(data["message"], "Password Reset Failed, Please check your input")

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
        self.assertEqual(data["message"], "Password Reset Failed, All fields are required")

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
        self.assertEqual(data["message"], "Password Reset Failed, Please check your input")
