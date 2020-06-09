from .. import db
import datetime


class Post(db.Model):
    """ Post Model for storing post related details """
    __tablename__ = "post"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    owner = db.Column(db.Integer, db.ForeignKey('user.username'), nullable=False)
    uploaded_at = db.Column(db.DateTime, nullable=False)
    public_id = db.Column(db.String(100), unique=True)
    image = db.Column(db.String(100), unique=True)
    caption = db.Column(db.String(2200))

    def __repr__(self):
        return "<Post '{}'>".format(self.public_id)