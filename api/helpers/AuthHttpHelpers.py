from flask import json

from api.helpers.tests_dummy_data import BASE_URL, fake_link


class AuthHttpHelpers:
    def __init__(self, client):
        self.client = client

    def user_registration(self, user):
        response = self.client.post("{}/api/v1/auth/register".format(BASE_URL),
                                    data=json.dumps(user), content_type='application/json')
        data = json.loads(response.data.decode())
        return {
            "status": response.status_code,
            "data": data
        }

    def login(self, user):
        response = self.client.post("{}/api/v1/auth/login".format(BASE_URL),
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

        :param self:
        :param user:
        :param correct:
        :return:
        """
        self.user_registration(user)
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
