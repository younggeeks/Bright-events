import json
import unittest

import app
from config.config import environments


class DocsPageTester(unittest.TestCase):
    def setUp(self):
        self.BASE_URL = environments["testing"].BASE_URL
        self.app = app.app.test_client()
        app.app.testing = True

    def test_docs_route(self):
        response = self.app.get("{}/".format(self.BASE_URL))
        self.assertEqual(response.status_code, 200)

