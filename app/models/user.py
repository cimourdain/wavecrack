# standard import
from datetime import datetime

# third party import
import ldap
from flask_login import UserMixin, AnonymousUserMixin
from werkzeug.security import generate_password_hash, check_password_hash

# local imports
from server import app
from app import db, login_manager
from app.helpers.text import TextHelper


class User(UserMixin, db.Model):
    """
    User model based on User mixin from flask-login

    """

    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.Text, nullable=False)
    _email = db.Column(db.Text, nullable=False)
    password_hash = db.Column(db.Text, nullable=True)
    ldap_user = db.Column(db.Boolean, default=False)
    is_admin = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.now(), nullable=False)

    cracks_requests = db.relationship("CrackRequest", back_populates='user')

    # GETTERS
    @property
    def password(self):
        """
        Forbid direct access to password property
        :return:
        """
        raise AttributeError('password is not a readable attribute')

    @property
    def email(self):
        return self._email

    # SETTERS
    @password.setter
    def password(self, password):
        """
        Generate password with standard generate_password_hash method from werkzeug.security
        :param password:<str>
        :return: <bool>
        """
        self.password_hash = generate_password_hash(password)

    @email.setter
    def email(self, email):
        if TextHelper.check_email(email):
            self._email = email
        else:
            raise AttributeError('Invalid email : '+str(email))

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
    def login(login, password):
        login = User.clean_login(login)

        # LDAP LOGIN
        if app.config["ENABLE_LDAP"]:
            ldap_email, msg = User.ldap_auth(username=login, password=password)

            if ldap_email:
                # return existing user if found
                existing_user = User.query.filter(
                    User.name == User.clean_login(login),
                    User._email == ldap_email,
                    User.ldap_user is True
                ).first()
                if existing_user:
                    return existing_user

                # create a new user and return it
                new_user = User()
                new_user.name = login
                new_user.email = ldap_email
                new_user.ldap_user = True
                db.session.add(new_user)
                db.session.commit()
                return new_user

        # LOCAL LOGIN
        user = None
        if TextHelper.check_email(login):
            app.logger.debug("Find user by email with "+str(login))
            user = User.query.filter(User._email == login).first()
        else:
            app.logger.debug("Find user by name with " + str(login))
            user = User.query.filter(User.name == login).first()

        if not user or not user.verify_password(password):
            if not user:
                app.logger.debug("User not found")
            else:
                app.logger.debug("Invalid password")
            return None

        return user

    @staticmethod
    def clean_login(login):
        return ''.join([c for c in login if c not in [",", "*", "|", "&", ">", "<", "+", ";", "=", "\\"]]).lower()

    @staticmethod
    def ldap_auth(username, password):
        ldap.set_option(ldap.OPT_X_TLS_REQUIRE_CERT, ldap.OPT_X_TLS_NEVER)
        try:
            conn = ldap.initialize(
                "{}://{}:{}".format(
                    "ldaps" if app.config["LDAP_TLS"] else "ldap",
                    app.config["LDAP_HOST"],
                    str(app.config["LDAP_PORT"])
                )
            )
        except ldap.SERVER_DOWN:
            return None, "Impossible to reach LDAP Server"

        conn.protocol_version = 3
        # Required for the operation
        conn.set_option(ldap.OPT_REFERRALS, 0)

        try:
            # perfom ldap login
            conn.simple_bind_s("{}@{}".format(
                username,
                app.config["LDAP_NAME"]
            ), password)

            # Research parameters to find user's email
            result = conn.search_s(
                app.config["LDAP_BASE_DN"],
                ldap.SCOPE_SUBTREE,
                app.config["LDAP_SEARCH_FILTER"] % username,
                ["mail"]
            )
            return result[0][1]['mail'][0], ""

        except ldap.INVALID_CREDENTIALS:
            return None, "Invalid LDAP Credentials"
        except ldap.UNWILLING_TO_PERFORM:
            return None, "LDAP: UNWILLING_TO_PERFORM"
        except ldap.LDAPError as e:
            return None, "LDAP Error: "+str(e)
        finally:
            conn.unbind_s()

    @staticmethod
    def insert_default_users():
        """
        Method used in migrations (flask deploy command) to create default users from config.

        :return: True
        """
        from server import app
        if "DEFAULT_USERS" in app.config:
            for u in app.config['DEFAULT_USERS']:
                if TextHelper.check_email(u["email"]):
                    new_user = User()
                    new_user.name = User.clean_login(u["name"])
                    new_user.email = u["email"]
                    new_user.password = u["password"]
                    new_user.is_admin = u["admin"] if "admin" in u and isinstance(u["admin"], bool) else False
                    db.session.add(new_user)
                    db.session.commit()
                else:
                    app.logger.error("Invalid email for user "+str(u["email"]))

        return True


class AnonymousUser(AnonymousUserMixin):
    pass


login_manager.anonymous_user = AnonymousUser


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
