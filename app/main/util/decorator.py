import sys
from functools import wraps
from flask import request

from app.main.service.auth_helper import Auth
from app.main.config import file_types, max_file_size


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):

        data, status = Auth.get_logged_in_user(request)
        token = data.get('data')

        if not token:
            return data, status

        return f(*args, **kwargs)

    return decorated


def admin_token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):

        data, status = Auth.get_logged_in_user(request)
        token = data.get('data')

        if not token:
            return data, status

        admin = token.get('admin')
        if not admin:
            response_object = {
                'status': 'fail',
                'message': 'admin token required'
            }
            return response_object, 401

        return f(*args, **kwargs)

    return decorated


def allowed_file(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        file = request.files['image']
        if not '.' in file.filename or not \
            file.filename.rsplit('.', 1)[1].lower() in file_types:
           response_object = {
            'status': 'fail',
            'message': 'Please upload a valid file type'
           }
           return response_object, 400
        
        return f(*args, **kwargs)

    return decorated


def file_size_limit(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        file = request.files['image']
        blob = file.read(max_file_size + 1)
        file.seek(0)
        if len(blob) > max_file_size:
            response_object = {
                'status': 'fail',
                'message': 'Maximum file size is 2MB'
            }
            return response_object, 400

        return f(*args, **kwargs)

    return decorated
