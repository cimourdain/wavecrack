#!/usr/bin/python
# coding: utf8

# standard imports
import os

# third party imports
from flask_migrate import Migrate, upgrade

# local imports
from app import create_app, db, register_routes, make_celery, db_init_content


# initialize app
app = create_app(os.getenv('FLASK_CONFIG') or 'default')

# Celery initalization
celery = make_celery(app)

# init migrations
migrate = Migrate(app, db)
from app.models import *


@app.cli.command()
def deploy():
    """
    Delare commande to perform db deployment
    usage : $ flask deploy
    """

    db_init_content()


if __name__ == '__main__':
    register_routes(app)
    # Run the app
    app.run(host=app.config['HOST'], port=app.config['PORT'], debug=app.config['DEBUG'], threaded=True)
