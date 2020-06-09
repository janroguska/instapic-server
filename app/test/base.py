from flask_testing import TestCase

from app.main import db
from app.main.model.user import User
from app. main.model.post import Post
from manage import app
from app.main.config import store


class BaseTestCase(TestCase):
    """ Base Tests """

    def create_app(self):
        app.config.from_object('app.main.config.TestingConfig')
        return app

    def setUp(self):
        db.create_all()
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
