# local imports
from app import db

from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash


class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.Text)
    email = db.Column(db.Text)
    password_hash = db.Column(db.Text)

    cracks = db.relationship('Crack', backref='user', lazy=True)

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    @staticmethod
    def insert_default_users():
        from server import app
        if "DEFAULT_USERS" in app.config:
            for u in app.config['DEFAULT_USERS']:
                new_user = User()
                new_user.name = u["name"]
                new_user.email = u["email"]
                new_user.password = u["password"]
                db.session.add(new_user)
                db.session.commit()
