# third party imports
from sqlalchemy.orm import relationship

# local imports
from app import db


class Crack(db.Model):
    __tablename__ = 'cracks'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    crack_id = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    output_file = db.Column(db.Text, nullable=False)
    start_date = db.Column(db.DateTime, nullable=False)
    hashes_number = db.Column(db.Integer, nullable=False)
    crack_duration = db.Column(db.Integer, nullable=False)
    email_end_job_sent = db.Column(db.Integer, nullable=False)
