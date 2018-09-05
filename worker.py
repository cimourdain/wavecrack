from server import app
from app import make_celery
from app.tasks import *

celery = make_celery(app)
