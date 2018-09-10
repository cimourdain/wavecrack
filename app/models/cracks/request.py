# standard imports
from datetime import datetime
import uuid
import os
# third party imports
from sqlalchemy.orm import relationship

# local imports
from server import app
from app import db
from app.ref.hashes_list import HASHS_LIST
from app.helpers.files import FilesHelper


class CrackRequest(db.Model):
    __tablename__ = 'cracks_requests'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    session_id = db.Column(db.Text, nullable=False, default=str(uuid.uuid4()))
    _hashes_type_code = db.Column(db.Integer, nullable=False)
    hashed_file_contains_usernames = db.Column(db.Boolean, nullable=False, default=False)
    hashes_path = db.Column(db.Text, nullable=False)
    _dictionary_paths = db.Column(db.Text, nullable=False)
    mask_path = db.Column(db.Text, nullable=True)
    rules = db.Column(db.Text, nullable=True)
    bruteforce = db.Column(db.Boolean, nullable=False, default=False)
    start_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    duration = db.Column(db.Integer, nullable=False)
    email_end_job_sent = db.Column(db.Boolean, nullable=False, default=False)

    cracks = relationship("Crack", backref="request")

    def __init__(self):
        self.session_id = str(uuid.uuid4())

    @property
    def hashes_type_code(self):
        return self.hashes_type_code

    @hashes_type_code.setter
    def hashes_type_code(self, code):
        for h in HASHS_LIST:
            if int(h["code"]) == int(code):
                self._hashes_type_code = int(code)

    @property
    def crack_folder(self):
        folder_path = os.path.join(app.config["DIR_LOCATIONS"]["hashcat_outputs"], self.session_id)
        if not os.path.isdir(folder_path):
            os.mkdir(folder_path)

        return folder_path

    @property
    def hashes(self):
        return FilesHelper.get_file_content(self.hashes_path)

    @hashes.setter
    def hashes(self, hashes):
        self.hashes_path = FilesHelper.create_new_file(
            file_path=self.crack_folder,
            file_name="hashes.txt",
            content=hashes
        )

    @property
    def dictionary_paths(self):
        return self._dictionary_paths

    def add_dictionary_paths(self, list_of_wordlists, ref=False):
        if not isinstance(list_of_wordlists, list):
            list_of_wordlists = [list_of_wordlists]

        current_dict_path_list = self._dictionary_paths.split(',') if self._dictionary_paths else []

        if ref:
            prepath = app.config["DIR_LOCATIONS"]["wordlists"]
        else:
            prepath = self.crack_folder

        for d in list_of_wordlists:
            if d not in current_dict_path_list:
                current_dict_path_list.append(os.path.join(prepath, d))

        self._dictionary_paths = ','.join(current_dict_path_list)

    @property
    def keywords(self):
        for d in self.dictionary_paths.split(','):
            if not d.startswith(app.config["DIR_LOCATIONS"]["wordlists"]):
                return FilesHelper.get_file_content(d)

    @keywords.setter
    def keywords(self, keywords):
        keyword_file_path = FilesHelper.create_new_file(
            file_path=self.crack_folder,
            file_name="keywords.txt",
            content=keywords
        )

        self.add_dictionary_paths(keyword_file_path, ref=False)

    @property
    def mask(self):
        return FilesHelper.get_file_content(self.mask_path)

    @mask.setter
    def mask(self, mask):
        self.mask_path = FilesHelper.create_new_file(
            file_path=self.crack_folder,
            file_name="mask.hcmask",
            content=mask
        )

