import uuid
import datetime

def new_post(token, post_data, self):
    return self.client.post(
        '/post/',
        headers={
        	'Authorization': token,
        	'Content-Type': 'multipart/form-data'
        },
        data=post_data
    )