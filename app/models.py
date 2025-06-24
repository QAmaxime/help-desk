from . import db
from flask_login import UserMixin
from . import login_manager

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), unique=True, nullable=False)

class Admin(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), unique=True, nullable=False)

@login_manager.user_loader
def load_user(user_id):
    user = User.query.get(int(user_id))
    if user:
        return user
    return Admin.query.get(int(user_id))