import os
# third party imports
from flask_migrate import Migrate, upgrade

# local imports
from app import create_app, db, register_routes, make_celery
from app.models.user import User


# initialize app
app = create_app(os.getenv('FLASK_CONFIG') or 'default')
migrate = Migrate(app, db)

from app.models.cracks.request import CrackRequest  # do not remove
from app.models.cracks.entity import Crack  # do not remove

@app.cli.command()
def deploy():
    # init migration


    """
    Delare commande to perform db deployment
    usage : $ flask deploy
    """

    # upragde db
    upgrade()

    # insert default users
    User.insert_default_users()
