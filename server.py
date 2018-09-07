#!/usr/bin/python
# coding: utf8

# standard imports
import os

# third party imports
from flask_migrate import Migrate, upgrade

# local imports
from app import create_app, db, register_routes, make_celery
from app.models.user import User
from app.models.cracks.request import CrackRequest # do not remove
from app.models.cracks.entity import Crack # do not remove


# initialize app
app = create_app(os.getenv('FLASK_CONFIG') or 'default')
# init migration
migrate = Migrate(app, db)

# Celery initalization
celery = make_celery(app)


@app.cli.command()
def deploy():
    """
    Delare commande to perform db deployment
    usage : $ flask deploy
    """


    # upragde db
    upgrade()

    # insert default users
    User.insert_default_users()


if __name__ == '__main__':
    register_routes(app)
    # Run the app
    app.run(host=app.config['HOST'], port=app.config['PORT'], debug=app.config['DEBUG'], threaded=True)
