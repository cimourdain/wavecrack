# local imports
from server import app
from app import make_celery

# import all celery tasks
from app.tasks import *

celery = make_celery(app)
