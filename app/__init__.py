# coding: utf8
# standard imports
import os

# third party imports
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# local imports
from config import config

db = SQLAlchemy()


def create_app(config_name):
    app = Flask(__name__)

    if config_name not in config:
        config_name = "default"

    app.config.from_object(config[config_name])

    db.init_app(app)

    check_app_folders(app)

    @app.teardown_request
    def teardown_request(exception):
        # Close db connexion after each request
        db.session.close()

    return app


def check_app_folders(app):
    for k, folder in app.config['APP_LOCATIONS'].items():
        if not os.path.exists(folder):
            if not os.makedirs(folder):
                raise OSError(
                    "Impossible to find or create folder for {} ({})".format(str(k), str(folder))
                )
    return True


def register_routes(app):
    from app.routes.home.get import home_get
    app.register_blueprint(home_get)

    return True
