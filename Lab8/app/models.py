from . import db, login_manager
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin


class Message(db.Model):
    __tablename__ = "messages"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(15), unique=False, nullable=True)
    email = db.Column(db.String(40), unique=False, nullable=True)
    phone = db.Column(db.String(15), unique=False, nullable=True)
    library = db.Column(db.String(15), unique=False, nullable=True)
    message = db.Column(db.Text, unique=False, nullable=True)

    def __repr__(self):
        return f"Name : {self.name}, Email: {self.email}"


@login_manager.user_loader
def user_loader(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    password = db.Column(db.String(60), nullable=False)

    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.password = generate_password_hash(password=password)

    def verify_password(self, password):
        return check_password_hash(self.password, password)

    def __repr__(self):
        return f"User : {self.username}, Email: {self.email}"
