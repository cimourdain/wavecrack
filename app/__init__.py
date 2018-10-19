# coding: utf8
# standard imports
import os
import glob
import importlib

# third party imports
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from celery import Celery

# local imports
from config import config

db = SQLAlchemy()
login_manager = LoginManager()
login_manager.login_view = '/login'


def create_app(config_name):
    app = Flask(__name__)

    if config_name not in config:
        config_name = "default"

    app.config.from_object(config[config_name])

    db.init_app(app)

    login_manager.init_app(app)

    check_app_folders(app)

    @app.teardown_request
    def teardown_request(exception):
        # Close db connexion after each request
        db.session.close()

    return app

def db_init_content():
    from app.models.user import User

    User.insert_default_users()


def check_app_folders(app):
    for k, folder in app.config['DIR_LOCATIONS'].items():
        if not os.path.exists(folder):
            if not os.makedirs(folder):
                raise OSError(
                    "Impossible to find or create folder for {} ({})".format(str(k), str(folder))
                )
    return True


def register_routes(app):
    for root, dirnames, filenames in os.walk("app/routes"):
        for path in glob.glob(os.path.join(root, '*.py')):
            folders, filename = os.path.split(path)
            if filename != '__init__.py':
                # set import path in import format ( "." instead of "/" in path)
                import_path = path[:-3].replace(os.sep, '.')
                # get module name (folder_name)_(file_name)
                module_name = import_path[import_path.rfind('.', 0, import_path.rfind('.'))+1:].replace('.', '_')
                try:
                    print("Register "+str(module_name) + " from "+ str(import_path))
                    loaded_module = importlib.import_module(import_path)
                    module_var = getattr(loaded_module, module_name)
                    app.register_blueprint(module_var)
                except Exception as e:
                    print("Impossible to load route for "+str(import_path)+" : "+str(module_name)+" : "+str(e))

    return True


def make_celery(app):
    celery = Celery(
        app.import_name,
        backend=app.config['CELERY_RESULT_BACKEND'],
        broker=app.config['CELERY_BROKER_URL']
    )
    celery.conf.update(app.config)

    TaskBase = celery.Task

    class ContextTask(TaskBase):
        abstract = True

        def __call__(self, *args, **kwargs):
            with app.app_context():
                return TaskBase.__call__(self, *args, **kwargs)

    celery.Task = ContextTask

    return celery

