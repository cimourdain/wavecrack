# standard imports
from datetime import datetime

# third party imports
from sqlalchemy.orm import relationship

# local imports
from app import db


class CrackRequest(db.Model):
    __tablename__ = 'cracks_requests'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    crack_folder = db.Column(db.Text, nullable=False)
    start_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    crack_duration = db.Column(db.Integer, nullable=False)
    email_end_job_sent = db.Column(db.Boolean, nullable=False, default=False)

    cracks = relationship("Crack", backref="request")
