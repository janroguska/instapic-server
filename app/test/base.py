from flask_testing import TestCase
import uuid
import datetime

from app.main import db
from app.main.model import User, Post
from manage import app
from app.main.config import store

MOCK_USERS = [
    {
        'public_id': str(uuid.uuid4()),
        'email': 'bob@bob.com',
        'password': 'password',
        'username': 'bob',
        'registered_on': datetime.datetime.utcnow(),
        'admin': True,
    }
]


class BaseTestCase(TestCase):
    """ Base Tests """

    def create_app(self):
        app.config.from_object('app.main.config.TestingConfig')
        return app

    def setUp(self):
        db.create_all()

        # Mock db
        for user in MOCK_USERS:
            db.session.add(User(public_id=user['public_id'], \
                email=user['email'], username=user['username'], \
                password=user['password'], registered_on=user['registered_on'], \
                admin=user['admin']))
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
