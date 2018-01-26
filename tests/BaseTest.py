from unittest import TestCase

from api import create_app, db
from api.models import Category


class BaseTestCase(TestCase):
    def setUp(self):
        super(BaseTestCase, self).setUp()
        self.category = Category(name="noma sana")
        self.app = create_app("testing")
        self.client = self.app.test_client()
        self.test_db = db.init_app(self.app)

        with self.app.app_context():
            db.init_app(self.app)
            db.drop_all()
            db.create_all()
            db.session.add(self.category)
            db.session.commit()