# standard imports
from datetime import datetime
import uuid
import os
import json

# third party imports
from sqlalchemy.orm import relationship

# local imports
from server import app
from app import db
from app.ref.hashes_list import HASHS_LIST
from app.helpers.files import FilesHelper
from app.models.cracks.entity import Crack


class CrackRequest(db.Model):
    __tablename__ = 'cracks_requests'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    celery_request_id = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    session_id = db.Column(db.Text, nullable=False, default=str(uuid.uuid4()))
    _hashes_type_code = db.Column(db.Integer, nullable=False)
    hashed_file_contains_usernames = db.Column(db.Boolean, nullable=False, default=False)
    hashes_path = db.Column(db.Text, nullable=False)
    _dictionary_paths = db.Column(db.Text, nullable=False)
    mask_path = db.Column(db.Text, nullable=True)
    bruteforce = db.Column(db.Boolean, nullable=False, default=False)
    _extra_options = db.Column(db.Text, nullable=True)
    start_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    duration = db.Column(db.Integer, nullable=False)
    email_end_job_sent = db.Column(db.Boolean, nullable=False, default=False)

    cracks = relationship("Crack", backref="request")

    def __init__(self):
        self.session_id = str(uuid.uuid4())

    @property
    def hashes_type_code(self):
        return self._hashes_type_code

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

    @property
    def rules(self):
        for d in self.rules_path.split(','):
            yield d

    @rules.setter
    def rules(self, rules_paths):
        if isinstance(rules_paths, basestring):
            rules_paths = [rules_paths]

        current_options = self.extra_options
        for rp in rules_paths:
            current_options.append({
                "option": "--rules-file",
                "value": os.path.join(app.config["DIR_LOCATIONS"]["rules"], str(rp))
            })

        self._extra_options = json.dumps(current_options, indent=4)

    @property
    def extra_options(self):
        if self._extra_options:
            print("extra options: "+str(self._extra_options))
            return json.loads(self._extra_options)

        return []

    def prepare_cracks(self):

        for wordlist_file_path in self.dictionary_paths.split(','):
            # create new crack
            new_dict_crack = Crack()
            new_dict_crack.working_folder = self.crack_folder
            db.session.add(new_dict_crack)
            self.cracks.append(new_dict_crack)
            new_dict_crack.build_crack_cmd(
                attack_mode=0,
                attack_file=wordlist_file_path
            )

        if self.mask:
            new_mask_crack = Crack()
            new_mask_crack.working_folder = self.crack_folder
            db.session.add(new_mask_crack)
            self.cracks.append(new_mask_crack)
            new_mask_crack.build_crack_cmd(
                attack_mode=3,
                attack_file=new_mask_crack
            )

        if self.bruteforce:
            new_bf_crack = Crack()
            new_bf_crack.working_folder = self.crack_folder
            db.session.add(new_bf_crack)
            self.cracks.append(new_bf_crack)
            new_bf_crack.build_crack_cmd(
                attack_mode=3,
                attack_file=None
            )

        db.session.commit()

    def run_cracks(self):
        for c in self.cracks:
            c.run()


