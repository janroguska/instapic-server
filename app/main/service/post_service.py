import os
import uuid
import datetime
from werkzeug.utils import secure_filename
from sqlalchemy import desc, asc
from uuid import uuid4

from app.main import db
from app.main.config import store
from app.main.model.post import Post
from app.main.model.user import User


def save_new_post(request):
    # Get the auth token.
    auth_token = request.headers.get('Authorization')
    data = request.form
    if auth_token:
        # Decode the token to get user details.
        resp = User.decode_auth_token(auth_token)
        if not isinstance(resp, str):
            user = User.query.filter_by(id=resp).first()
            # Save the image and return the path.
            image_url = save_image(request.files['image'])
            # Add the post to the DB.
            new_post = Post(
                public_id=str(uuid.uuid4()),
                caption=data['caption'],
                uploaded_at=datetime.datetime.utcnow(),
                owner=user.username,
                image=image_url,
            )
            save_changes(new_post)
            response_object = {
                'status': 'success',
                'message': 'Successfully added post to db.'
            }
            return response_object, 201
        response_object = {
            'status': 'fail',
            'message': resp
        }
        return response_object, 401
    else:
        response_object = {
            'status': 'fail',
            'message': 'Provide a valid auth token.'
        }
        return response_object, 401


def get_all_posts(params):
    page = params.get('page')
    sort_by = params.get('sort_by')
    user = params.get('user')
    # Get the page to query
    if page is not None and page.isdigit():
        page_to_search = int(page)
    else:
        page_to_search = 1

    # Filter by user if it's in the query
    data = { 'owner': user }
    filter_data = {
        key: value for (key, value) in data.items() if value
    } 

    # Sort by user or date
    if sort_by == 'user':
        return Post.query.filter_by(**filter_data).order_by(desc(Post.owner)) \
        .paginate(page=page_to_search, per_page=18, error_out=False).items
    elif sort_by == 'newest':
        return Post.query.filter_by(**filter_data).order_by(desc(Post.uploaded_at)) \
        .paginate(page=page_to_search, per_page=18, error_out=False).items
    elif sort_by == 'oldest':
        return Post.query.filter_by(**filter_data).order_by(asc(Post.uploaded_at)) \
        .paginate(page=page_to_search, per_page=18, error_out=False).items
    else:
        return Post.query.filter_by(**filter_data) \
        .paginate(page=page_to_search, per_page=18, error_out=False).items


def save_image(image):
    # Ensure the filename is safe
    filename = secure_filename(image.filename)
    # Ensure the filename is unique
    unique_id = uuid4().__str__()[:8]
    unique_filename = f"{unique_id}-{filename}"
    # Generate an images directory if it doesn't exist ye
    if not os.path.exists(store):
        os.makedirs(store)
    # Save the file
    path = os.path.join(store, unique_filename)
    image.save(path)
    return unique_filename


def save_changes(data):
    db.session.add(data)
    db.session.commit()
