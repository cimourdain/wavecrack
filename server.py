#!/usr/bin/python
# coding: utf8

# standard imports
import os

# third party imports
from flask_migrate import Migrate, upgrade
from celery import Celery

# local imports
from app import create_app, db, register_routes
from app.models.user import User
from app.models.cracks.entity import Crack
from app.models.cracks.options import CracksOption

# initialize app
app = create_app(os.getenv('FLASK_CONFIG') or 'default')


# Celery initalization
celery = Celery(
    app.name,
    backend=app.config['CELERY_RESULT_BACKEND'],
    broker=app.config['CELERY_BROKER_URL']
)
celery.conf.update(app.config)


@app.cli.command()
def deploy():
    """
    Delare commande to perform db deployment
    usage : $ flask deploy
    """
    # init migration
    migrate = Migrate(app, db)

    # upragde db
    upgrade()

    # insert default users
    User.insert_default_users()


if __name__ == '__main__':
    register_routes(app)
    # Run the app
    app.run(host=app.config['HOST'], port=app.config['PORT'], debug=app.config['DEBUG'], threaded=True)
