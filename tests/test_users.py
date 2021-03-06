import json
import unittest
import app
from config.config import environments
from database.data_mocks import DataMocks


class UsersTester(unittest.TestCase):
    def setUp(self):
        self.app = app.app.test_client()
        self.BASE_URL = environments["testing"].BASE_URL
        app.app.testing = True

    def test_register_successful(self):
        user = {
            "full_name": "Kilango Jumiya",
            "email": "naiifg@gmadfadsfsdfsdfil.comd",
            "password": "secret",
            "id": "549853"
        }

        # testing if it returns correct number of users in our list
        self.assertEqual(len(DataMocks.users), 6)
        response = self.app.post("{}/api/v1/auth/register".format(self.BASE_URL),
                                 data=json.dumps(user), content_type='application/json')
        # testing if it returns correct number after inserting
        self.assertEqual(len(DataMocks.users), 7)
        # testing if adding event is successful
        self.assertEqual(response.status_code, 201)

    def test_register_email_exists(self):
        user = {
            "full_name": "Kilango Jumiya",
            "email": "younggeeks101@gmail.com",
            "password": "secret",
            "id": "549853"
        }

        # testing if it returns correct number of users in our list
        self.assertEqual(len(DataMocks.users), 6)
        response = self.app.post("{}/api/v1/auth/register".format(self.BASE_URL),
                                 data=json.dumps(user), content_type='application/json')

        # testing if it returns the same number after failed registration
        self.assertEqual(len(DataMocks.users), 6)

        # testing if adding event is successful
        self.assertEqual(response.status_code, 400)

    def test_login_successful(self):
        credentials = {
            "email": "younggeeks101@gmail.com",
            "password": "secret",
        }

        response = self.app.post("{}/api/v1/auth/login".format(self.BASE_URL),
                                 data=json.dumps(credentials), content_type='application/json')

        # testing if Login is successful
        self.assertEqual(response.status_code, 200)

    def test_login_unsuccessful_wrong_email(self):
        credentials = {
            "email": "younggeeks101@gmail.comd",
            "password": "secret",
        }

        response = self.app.post("{}/api/v1/auth/login".format(self.BASE_URL),
                                 data=json.dumps(credentials), content_type='application/json')

        # testing if Login is unsuccessful
        self.assertEqual(response.status_code, 401)

    def test_login_unsuccessful_wrong_password(self):
        credentials = {
            "email": "younggeeks101@gmail.com",
            "password": "secretj",
        }

        response = self.app.post("{}/api/v1/auth/login".format(self.BASE_URL),
                                 data=json.dumps(credentials), content_type='application/json')

        # testing if Login is unsuccessful
        self.assertEqual(response.status_code, 401)

    def test_logout_successful(self):
        credentials = {
            "email": "younggeeks101@gmail.com",
            "password": "secret",
        }

        response = self.app.post("{}/api/v1/auth/logout".format(self.BASE_URL),
                                 data=json.dumps(credentials), content_type='application/json')

        # testing if Login is unsuccessful
        self.assertEqual(response.status_code, 200)

    def test_logout_unsuccessful_wrong_email(self):
        credentials = {
            "email": "younggeeks101@gmail.comw",
            "password": "secret",
        }
        response = self.app.post("{}/api/v1/auth/logout".format(self.BASE_URL),
                                 data=json.dumps(credentials), content_type='application/json')

        # testing if Login is unsuccessful
        self.assertEqual(response.status_code, 401)

    def test_logout_unsuccessful_wrong_password(self):
        credentials = {
            "email": "younggeeks101@gmail.com",
            "password": "secretdfd",
        }
        response = self.app.post("{}/api/v1/auth/logout".format(self.BASE_URL),
                                 data=json.dumps(credentials), content_type='application/json')

        # testing if Login is unsuccessful
        self.assertEqual(response.status_code, 401)

    def test_password_reset_successful(self):
        credentials = {
            "email": "younggeeks101@gmail.com",
            "password": "secretd",
        }
        response = self.app.post("{}/api/v1/auth/reset-password".format(self.BASE_URL),
                                 data=json.dumps(credentials), content_type='application/json')

        # testing if Login is unsuccessful
        self.assertEqual(response.status_code, 200)

    def test_password_reset_unsuccessful(self):
        credentials = {
            "email": "younggeeks101@gmail.comd",
            "password": "secretd",
        }

        response = self.app.post("{}/api/v1/auth/reset-password".format(self.BASE_URL),
                                 data=json.dumps(credentials), content_type='application/json')
        # testing if Login is unsuccessful
        self.assertEqual(response.status_code, 401)




