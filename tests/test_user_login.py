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
