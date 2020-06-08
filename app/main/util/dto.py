from flask_restplus import Namespace, fields
from werkzeug.datastructures import FileStorage


class PostDto:
    api = Namespace('post', description='post related operations')
    post_model = api.model('post', {
        'caption': fields.String(required=True, description='post caption'),
        'owner': fields.String(required=True, description='user who posted'),
        'image': fields.String(required=True, description='post image'),
        'uploaded_at': fields.DateTime(required=True, description='time of post'),
    })
    post = api.parser()
    post.add_argument('caption', required=True),
    post.add_argument('image', type=FileStorage, location='files', required=True)


class UserDto:
    api = Namespace('user', description='user related operations')
    user = api.model('user', {
        'email': fields.String(
            required=True,
            description='user email address',
            min_length=6
        ),
        'username': fields.String(
            required=True,
            description='user username',
            min_length=6
        ),
        'password': fields.String(
            required=True,
            description='user password',
            min_length=6
        ),
        'public_id': fields.String(description='user Identifier'),
        'posts': fields.Nested(PostDto.post_model)
    })


class AuthDto:
    api = Namespace('auth', description='authentication related operations')
    user_auth = api.model('auth_details', {
        'email': fields.String(required=True, description='The email address'),
        'password': fields.String(required=True, description='The user password'),
    })
