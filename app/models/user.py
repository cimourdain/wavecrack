# local imports
from app import db, login_manager

from flask_login import UserMixin, AnonymousUserMixin
from werkzeug.security import generate_password_hash, check_password_hash


class User(UserMixin, db.Model):
    """
    User model based on User mixin from flask-login

    """

    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.Text)
    email = db.Column(db.Text)
    password_hash = db.Column(db.Text)
    is_admin = db.Column(db.Boolean, default=False)

    cracks_requests = db.relationship("CrackRequest", back_populates='user')

    # GETTERS
    @property
    def password(self):
        """
        Forbid direct access to password property
        :return:
        """
        raise AttributeError('password is not a readable attribute')

    # SETTERS
    @password.setter
    def password(self, password):
        """
        Generate password with standard generate_password_hash method from werkzeug.security
        :param password:<str>
        :return: <bool>
        """
        self.password_hash = generate_password_hash(password)
        return True

    # METHODS
    def verify_password(self, password):
        """
        Verify password with standard check_password_hash method from werkzeug.security
        :param password: <str>
        :return: <bool>
        """
        return check_password_hash(self.password_hash, password)

    # STATICS METHODS
    @staticmethod
    def get_user(user_id=None, login=None, email=None, name=None):
        """
        method used to fetch a user from one of its parameters

        :param user_id: <str>
        :param login: <str>
        :param email: <str>
        :param name: <str>
        :return: <User> or None
        """
        if user_id:
            return User.query.filter(User.id == user_id).first()
        elif login:
            return User.query.filter((User.email == login) | (User.name == login)).first()
        elif email:
            return User.query.filter(User.email == email).first()
        elif name:
            return User.query.filter(User.name == name).first()

        return None

    @staticmethod
    def insert_default_users():
        """
        Method used in migrations (flask deploy command) to create default users from config.

        :return: True
        """
        from server import app
        if "DEFAULT_USERS" in app.config:
            for u in app.config['DEFAULT_USERS']:

                new_user = User()
                new_user.name = u["name"]
                new_user.email = u["email"]
                new_user.password = u["password"]
                new_user.is_admin = u["admin"] if "admin" in u and isinstance(u["admin"], bool) else False
                db.session.add(new_user)
                db.session.commit()

        return True


class AnonymousUser(AnonymousUserMixin):
    pass


login_manager.anonymous_user = AnonymousUser


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))