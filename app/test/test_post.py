import unittest
from io import BytesIO
from PIL import Image
import json
import sys

from app.main import db
from app.test.base import BaseTestCase
from app.test.utils.auth_helpers import register_user
from app.test.utils.post_helpers import new_post


class TestPostBlueprint(BaseTestCase):
    def test_new_post(self):
        """ Test for new post """
        with self.client:
            resp_register = register_user(self)
            auth_data = json.loads(resp_register.data.decode())
            token = auth_data['Authorization']
            file = BytesIO()
            image = Image.new('RGBA', size=(50, 50), color=(155, 0, 0))
            image.save(file, 'png')
            file.name = 'test.png'
            file.seek(0)
            post_data = dict(
                image=file,
                caption='This is a caption'
            )
            response = new_post(token, post_data, self)
            data = json.loads(response.data)
            self.assertTrue(data['status'] == 'success')
            self.assertTrue(data['message'] == 'Successfully added post to db.')
            self.assertTrue(response.content_type == 'application/json')
            self.assertEqual(response.status_code, 201)

    def test_new_post_no_image(self):
        """ Test for new post without image upload """
        with self.client:
            resp_register = register_user(self)
            auth_data = json.loads(resp_register.data.decode())
            token = auth_data['Authorization']
            post_data = dict(
                caption='This is a caption'
            )
            response = new_post(token, post_data, self)
            data = json.loads(response.data)
            self.assertTrue(data['message'] == 'The browser (or proxy) sent a request that this server could not understand.')
            self.assertTrue(response.content_type == 'application/json')
            self.assertEqual(response.status_code, 400)

    def test_new_post_no_caption(self):
        """ Test for new post without caption """
        with self.client:
            resp_register = register_user(self)
            auth_data = json.loads(resp_register.data.decode())
            token = auth_data['Authorization']
            file = BytesIO()
            image = Image.new('RGBA', size=(50, 50), color=(155, 0, 0))
            image.save(file, 'png')
            file.name = 'test.png'
            file.seek(0)
            post_data = dict(
                image=file,
            )
            response = new_post(token, post_data, self)
            data = json.loads(response.data)
            self.assertTrue(data['message'] == 'The browser (or proxy) sent a request that this server could not understand.')
            self.assertTrue(response.content_type == 'application/json')
            self.assertEqual(response.status_code, 400)

    def test_new_post_invalid_file_type(self):
        """ Test for new post wrong file type """
        with self.client:
            resp_register = register_user(self)
            auth_data = json.loads(resp_register.data.decode())
            token = auth_data['Authorization']
            post_data = dict(
                image=(BytesIO(b"this is a test"), 'test.pdf'),
                caption='This is a caption'
            )
            response = new_post(token, post_data, self)
            data = json.loads(response.data)
            self.assertTrue(data['status'] == 'fail')
            self.assertTrue(data['message'] == 'Please upload a valid file type')
            self.assertTrue(response.content_type == 'application/json')
            self.assertEqual(response.status_code, 400)
