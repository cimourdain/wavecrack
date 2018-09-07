# standard imports
from datetime import datetime

# local imports
from app import db


class Crack(db.Model):
    __tablename__ = 'cracks'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    crack_request_id = db.Column(db.Integer, db.ForeignKey('cracks_requests.id'))
    cmd = db.Column(db.Text, nullable=False)
    start_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
