import json
import unittest

import time

from api import create_app, db
from api.helpers.tests_dummy_data import BASE_URL, correct_user, wrong_input_user, empty_input_user, wrong_email_user, \
    wrong_password_user, incorrect_reset_email, new_password, new_password_wrong, new_password_empty_fields, \
    fake_link, fake_token, encode_token


class UsersTester(unittest.TestCase):
    def setUp(self):
        self.app = create_app("testing")
        self.client = self.app.test_client()
        self.test_db = db.init_app(self.app)
        with self.app.app_context():
            db.init_app(self.app)
            db.drop_all()
            db.create_all()

    @staticmethod
    def user_registration(cls, user):

        response = cls.client.post("{}/api/v1/auth/register".format(BASE_URL),
                                   data=json.dumps(user), content_type='application/json')
        data = json.loads(response.data.decode())
        return {
            "status": response.status_code,
            "data": data
        }

    @staticmethod
    def login(cls, user):
        response = cls.client.post("{}/api/v1/auth/login".format(BASE_URL),
                                   data=json.dumps(user), content_type='application/json')

        data = json.loads(response.data.decode())
        return {
            "status": response.status_code,
            "data": data
        }

    def logout(self, token=None):

        if not token:
            headers = None
        else:
            headers = dict(
                Authorization='Bearer ' + token
            )

        response = self.client.post("{}/api/v1/auth/logout".format(BASE_URL), data={}, headers=headers)
        return response

    def reset_link(self, email=None):
        if not email:
            data = {}
        else:
            data = {"email": email}
        return self.client.post("{}/api/v1/auth/reset".format(BASE_URL),
                                data=json.dumps(data), content_type='application/json')

    def verify_token_request(self, link):
        return self.client.get(link)

    def do_verify_token(self, user, correct=True):
        """
        Test token verification, if correct parameter is set to true, It'll send
        request with correct reset link otherwise it'll send expired link

        :param user:
        :param correct:
        :return:
        """
        self.user_registration(self, user)
        response = self.reset_link(email=user["email"])
        data = json.loads(response.data.decode())
        if "link" not in data:
            return {
                "data": data,
                "status": response.status_code
            }
        if not correct:
            link = fake_link
        else:
            link = data["link"]

        verify_response = self.verify_token_request(link=link)
        verify_data = json.loads(verify_response.data.decode())

        return {
            "status": verify_response.status_code,
            "data": verify_data
        }

    def test_register_successful(self):
        response = self.user_registration(self, correct_user)
        self.assertEqual(response["status"], 201)
        self.assertEqual(response["data"]["message"], "Successfully Registered")

    def test_register_email_exists(self):
        self.user_registration(self, correct_user)
        response = self.user_registration(self, correct_user)

        self.assertEqual(response["status"], 401)
        self.assertEqual(response["data"]["message"], "User Already Exists, Please Login")

    def test_wrong_registration_input(self):
        response = self.user_registration(self, wrong_input_user)

        self.assertEqual(response["status"], 400)
        self.assertEqual(response["data"]["message"], "Registration Failed, Please check your input")

    def test_login_successful(self):
        self.user_registration(self, correct_user)
        response = self.login(self, correct_user)

        self.assertEqual(response["status"], 200)
        self.assertEqual(response["data"]["message"], "Login successful")

    def test_login_unsuccessful_missing_fields(self):
        response = self.login(self, wrong_input_user)

        self.assertEqual(response["status"], 400)
        self.assertEqual(response["data"]["message"], "Login Failed, Please check your input")

    def test_login_unsuccessful_empty_fields(self):
        response = self.login(self, empty_input_user)

        self.assertEqual(response["status"], 400)
        self.assertEqual(response["data"]["message"], "Email and password fields are required to login")

    def test_login_unsuccessful_wrong_email(self):
        response = self.login(self, wrong_email_user)

        self.assertEqual(response["status"], 401)
        self.assertEqual(response["data"]["message"],
                         "No Account is associated with Email juma@gmail.com, Login Failed")

    def test_login_unsuccessful_wrong_password(self):
        self.user_registration(self, correct_user)
        response = self.login(self, wrong_password_user)

        self.assertEqual(response["status"], 401)
        self.assertEqual(response["data"]["message"], "Wrong Combination of Email and password, Login Failed")

    def test_logout_succesful(self):
        self.user_registration(self, correct_user)
        response = self.login(self, correct_user)

        logout_response = self.logout(response["data"]["token"])
        logout_data = json.loads(logout_response.data.decode())

        # testing if Logout is successful
        self.assertEqual(logout_response.status_code, 200)
        self.assertEqual(logout_data["message"], "Logout Successful")

    def test_logout_missing_token(self):

        logout_response = self.logout()
        logout_data = json.loads(logout_response.data.decode())

        self.assertEqual(logout_response.status_code, 401)
        self.assertEqual(logout_data["message"], "Token is missing from your header")

    def test_logout_already_signed_out(self):
        self.user_registration(self, correct_user)
        response = self.login(self, correct_user)
        token = response["data"]["token"]
        self.logout(token)

        second_logout_resp = self.logout(token)
        second_logout_data = json.loads(second_logout_resp.data.decode())

        self.assertEqual(second_logout_resp.status_code, 401)
        self.assertEqual(second_logout_data["message"], "User is already signed out")

    def test_logout_invalid_token(self):
        response = self.logout(fake_token)
        data = json.loads(response.data.decode())

        # testing if Logout is unsuccessful
        self.assertEqual(response.status_code, 400)
        self.assertEqual(data["message"], "Invalid Token , Please Login again")

    def test_logout_expired_token(self):
        token = encode_token()
        print(token)
        time.sleep(1)
        response = self.logout(token)
        data = json.loads(response.data.decode())

        # testing if Logout is unsuccessful
        self.assertEqual(response.status_code, 400)
        self.assertEqual(data["message"], "Token Expired , Please Login Again")

    def test_send_password_reset_link_success(self):
        self.user_registration(self, correct_user)
        response = self.reset_link(email=correct_user["email"])
        data = json.loads(response.data.decode())

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data["message"], "Password Reset Link Successfully Generated")

    def test_password_reset_email_not_found(self):
        response = self.reset_link(email=incorrect_reset_email)
        data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 404)
        self.assertEqual(data["message"], "Email not found , Password reset Failed")

    def test_password_reset_missing_input(self):
        response = self.reset_link()
        data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 400)
        self.assertEqual(data["message"], "Password Reset failed, Please check your input")

    def test_password_reset_verify_token_successful(self):
        verification = self.do_verify_token(correct_user)

        self.assertEqual(verification["status"], 200)
        self.assertEqual(verification["data"]["message"], "Password Reset Link Verified Successfully")

    def test_password_reset_verify_token_email_not_found(self):
        verification = self.do_verify_token(wrong_email_user)
        self.assertEqual(verification["status"], 404)
        self.assertEqual(verification["data"]["message"], "Email not found , Password reset Failed")

    def test_password_reset_verify_token_invalid_or_expired_token(self):
        verification = self.do_verify_token(correct_user, correct=False)
        self.assertEqual(verification["status"], 400)
        self.assertEqual(verification["data"]["message"], "Password Reset Link is invalid, or Expired")

    def test_password_reset_change_password_successful(self):
        verification = self.do_verify_token(correct_user)

        token = verification["data"]["token"]
        response_get = self.client.get("{}/api/v1/auth/reset-password/{}".format(BASE_URL, token))
        data = json.loads(response_get.data.decode())

        new_token = data["token"]
        response = self.client.post("{}/api/v1/auth/reset-password/{}".format(BASE_URL, new_token),
                                    data=json.dumps(new_password), content_type="application/json")
        data = json.loads(response.data.decode())

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data["message"], "Password Reset Successfully")

    def test_password_reset_change_password_not_matching_password_confirmation(self):
        verification = self.do_verify_token(correct_user)
        token = verification["data"]["token"]
        response_get = self.client.get("{}/api/v1/auth/reset-password/{}".format(BASE_URL, token))
        data = json.loads(response_get.data.decode())

        new_token = data["token"]
        response = self.client.post("{}/api/v1/auth/reset-password/{}".format(BASE_URL, new_token),
                                    data=json.dumps(new_password_wrong), content_type="application/json")
        data = json.loads(response.data.decode())

        self.assertEqual(response.status_code, 401)
        self.assertEqual(data["message"], "Password and Password confirmation do not match")

    def test_password_reset_change_password_missing_field(self):
        verification = self.do_verify_token(correct_user)
        token = verification["data"]["token"]
        response_get = self.client.get("{}/api/v1/auth/reset-password/{}".format(BASE_URL, token))
        data = json.loads(response_get.data.decode())

        new_token = data["token"]
        response = self.client.post("{}/api/v1/auth/reset-password/{}".format(BASE_URL, new_token),
                                    data=json.dumps({}), content_type="application/json")
        data = json.loads(response.data.decode())

        self.assertEqual(response.status_code, 400)
        self.assertEqual(data["message"], "Password Reset Failed, Please check your input")

    def test_password_reset_change_password_empty_field(self):
        verification = self.do_verify_token(correct_user)
        token = verification["data"]["token"]
        response_get = self.client.get("{}/api/v1/auth/reset-password/{}".format(BASE_URL, token))
        data = json.loads(response_get.data.decode())

        new_token = data["token"]
        response = self.client.post("{}/api/v1/auth/reset-password/{}".format(BASE_URL, new_token),
                                    data=json.dumps(new_password_empty_fields), content_type="application/json")
        data = json.loads(response.data.decode())

        self.assertEqual(response.status_code, 400)
        self.assertEqual(data["message"], "Password Reset Failed, All fields are required")

    def test_password_reset_change_password_missing_data(self):
        verification = self.do_verify_token(correct_user)
        token = verification["data"]["token"]
        response_get = self.client.get("{}/api/v1/auth/reset-password/{}".format(BASE_URL, token))
        data = json.loads(response_get.data.decode())

        new_token = data["token"]
        response = self.client.post("{}/api/v1/auth/reset-password/{}".format(BASE_URL, new_token),
                                    data=json.dumps(empty_input_user), content_type="application/json")
        data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 400)
        self.assertEqual(data["message"], "Password Reset Failed, Please check your input")
