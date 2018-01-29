import time
from flask import json

from api.helpers.AuthHttpHelpers import AuthHttpHelpers
from api.helpers.tests_dummy_data import correct_user, fake_token, encode_token
from tests.BaseTest import BaseTestCase


class LogoutTestCase(BaseTestCase):
    def setUp(self):
        """
        We make initial configurations before running the tests
        We make sure to run setUp() from super class first
        and then we add our file specific variable(http_helper)
        :return:
        :return:
        """
        super(LogoutTestCase, self).setUp()
        self.http_helpers = AuthHttpHelpers(client=self.client)


    def test_logout_succesful(self):
        """
        User should be able to logout
        :return:
        """
        self.http_helpers.user_registration(correct_user)
        response = self.http_helpers.login(correct_user)
        logout_response = self.http_helpers.logout(response["data"]["token"])
        logout_data = json.loads(logout_response.data.decode())
        self.assertEqual(logout_response.status_code, 200)
        self.assertEqual(logout_data["message"], "Logout Successful")

    def test_logout_missing_token(self):
        """
        When User tries to logout with missing token
        User should get 401 with relevant error message
        :return:
        """
        logout_response = self.http_helpers.logout()
        logout_data = json.loads(logout_response.data.decode())
        self.assertEqual(logout_response.status_code, 401)
        self.assertEqual(logout_data["message"], "Token is missing from your header")

    def test_logout_already_signed_out(self):
        """
        If user token is already blacklisted
        User should get 401 with relevant error message
        :return:
        """
        self.http_helpers.user_registration(correct_user)
        response = self.http_helpers.login(correct_user)
        token = response["data"]["token"]
        self.http_helpers.logout(token)
        second_logout_resp = self.http_helpers.logout(token)
        second_logout_data = json.loads(second_logout_resp.data.decode())
        self.assertEqual(second_logout_resp.status_code, 401)
        self.assertEqual(second_logout_data["message"], "User is already signed out")

    def test_logout_invalid_token(self):
        """
        When user tries to logout with invalid token
        User should get 400 with relevant error message
        :return:
        """
        response = self.http_helpers.logout(fake_token)
        data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 400)
        self.assertEqual(data["message"], "Invalid Token , Please Login again")

    def test_logout_expired_token(self):
        """
        When user tries to logout with expired token
        User should get 400 with relevant error message
        :return:
        """
        token = encode_token()
        time.sleep(1)
        response = self.http_helpers.logout(token.decode())
        data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 400)
        self.assertEqual(data["message"], "Token Expired , Please Login Again")
