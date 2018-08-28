# local imports
from app import db


class CracksOption(db.Model):
    __tablename__ = 'cracks_options'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    crack_id = db.Column(db.Text,  db.ForeignKey('cracks.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    option = db.Column(db.Text, nullable=False)
