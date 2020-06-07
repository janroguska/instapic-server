import json


def register_user(self):
    return self.client.post(
        '/user/',
        data=json.dumps(dict(
            email='joe@gmail.com',
            username='username',
            password='123456'
        )),
        content_type='application/json'
    )


def login_user(self):
    return self.client.post(
        '/auth/login',
        data=json.dumps(dict(
            email='joe@gmail.com',
            password='123456'
        )),
        content_type='application/json'
    )


def login_registered_user(self):
    return self.client.post(
        '/auth/login',
        data=json.dumps(dict(
            email='bob@bob.com',
            password='password'
        )),
        content_type='application/json'
    )