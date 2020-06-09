from flask import request, send_from_directory
from flask_restplus import Resource

from app.main.util.decorator import token_required, allowed_file, file_size_limit
from app.main.config import store
from ..util.dto import PostDto
from ..service.post_service import save_new_post, get_all_posts

api = PostDto.api
_post = PostDto.post
_post_model = PostDto.post_model


@api.route('/')
class PostList(Resource):
    @api.doc('list_of_all_posts')
    @token_required
    @api.marshal_list_with(_post_model, envelope='data')
    def get(self):
        """Get a list of all posts"""
        params = request.args
        return get_all_posts(params=params)

    @api.expect(_post, validate=True)
    @token_required
    @allowed_file
    @file_size_limit
    @api.response(201, 'Post successfully created.')
    @api.doc('create a new post')
    def post(self):
        """Creates a new Post """
        return save_new_post(request=request)

@api.route('/image/<path:filename>')
class Post(Resource):
    @api.doc('get the image')
    def get(self, filename):
        return send_from_directory(store, filename)
