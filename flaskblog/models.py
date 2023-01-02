from datetime import datetime
from flaskblog import db, login_manager
from flask_login import UserMixin

# this is for reloading the user from the user ID stored in session,
# and it needs to know how to find the user with that id, so we decorate it
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default="default.jpg")
    password = db.Column(db.String(60), nullable=False)
    posts = db.relationship(
        "Post", backref="author", lazy=True
    )  # backref isn't the actual column in Post, but lets us access who is the user that created that post

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.image_file}')"


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)

    def __repr__(self):
        return f"Post('{self.title}', '{self.date_posted}')"


# the extension(login_manager) will expect user model to have certain atributes and methods
# 4 to be specific(
#   1. is_active is False
#
#   2. is_authenticated is False
#
#   3. is_anonymous is True
#
#   3. get_id() returns None
# )
# that's why we import UserMixin and inherit from to help us
# https://flask-login.readthedocs.io/en/latest/
