from .. import db, login_manager
from .. import bcrypt
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from datetime import datetime


@login_manager.user_loader
def user_loader(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.png')
    about_me = db.Column(db.String(120), nullable=True)
    last_seen = db.Column(db.DateTime, default=datetime.now())
    password = db.Column(db.String(60), nullable=False)
    tasks_owned = db.relationship('Task', backref='owner', lazy='dynamic')
    comments = db.relationship('Comment', backref='users', lazy='dynamic')

    @property
    def password_hash(self):
        raise AttributeError('Is not readable')

    @password_hash.setter
    def password_hash(self, password_hash):
        self.password = bcrypt.generate_password_hash(password_hash).decode('utf8')

    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.password_hash = password

    def verify_password(self, password_hash):
        return bcrypt.check_password_hash(self.password, password_hash)

    def __repr__(self):
        return f"User : {self.username}, Email: {self.email}"
