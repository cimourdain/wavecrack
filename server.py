#!/usr/bin/python
# coding: utf8

# standard imports
import os

# third party imports
from flask_migrate import Migrate, upgrade

# local imports
from app import create_app, db, register_routes, make_celery
from app.models.user import User


# initialize app
app = create_app(os.getenv('FLASK_CONFIG') or 'default')


# Celery initalization
celery = make_celery(app)


if __name__ == '__main__':
    register_routes(app)
    # Run the app
    app.run(host=app.config['HOST'], port=app.config['PORT'], debug=app.config['DEBUG'], threaded=True)
