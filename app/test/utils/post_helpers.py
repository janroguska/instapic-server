import uuid
import datetime

def new_post(token, post_data, self):
    return self.client.post(
        '/post/',
        authorization=token,
        data=post_data
        content_type='multipart/form-data'
    )