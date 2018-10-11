# standard imports
from datetime import datetime, timedelta
import uuid
import os
import json

# third party imports
from sqlalchemy.orm import relationship
from celery.result import AsyncResult

# local imports
from server import app, celery
from app import db
from app.ref.hashes_list import HASHS_LIST
from app.helpers.files import FilesHelper
from app.models.cracks.entity import Crack
from app.models.user import User
from app.ref.close_modes import REQUESTS_CLOSE_MODES


class CrackRequest(db.Model):
    __tablename__ = 'cracks_requests'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.Text, nullable=False, default="no name")
    celery_request_id = db.Column(db.Text, nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    session_id = db.Column(db.Text, nullable=False, default=str(uuid.uuid4()))
    _hashes_type_code = db.Column(db.Integer, nullable=False)
    hashed_file_contains_usernames = db.Column(db.Boolean, nullable=False, default=False)
    hashes_path = db.Column(db.Text, nullable=False)
    nb_password_to_find = db.Column(db.Integer, nullable=False)
    _dictionary_paths = db.Column(db.Text, nullable=True)
    mask_path = db.Column(db.Text, nullable=True)
    bruteforce = db.Column(db.Boolean, nullable=False, default=False)
    use_potfile = db.Column(db.Boolean, nullable=False, default=False)
    _extra_options = db.Column(db.Text, nullable=True)
    start_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    end_date = db.Column(db.DateTime, nullable=True)
    end_mode = db.Column(db.Text, nullable=True)
    duration = db.Column(db.Integer, nullable=False)
    email_end_job_sent = db.Column(db.Boolean, nullable=False, default=False)

    cracks = relationship("Crack", back_populates="request")
    user = relationship("User", back_populates="cracks_requests")

    def init_request_folder(self):
        self.session_id = str(uuid.uuid4())
        if not FilesHelper.dir_exists(self.request_working_folder):
            app.logger.debug("create directory "+str(self.request_working_folder))
            os.mkdir(self.request_working_folder)
        FilesHelper.file_exists(self.outfile_path, create=True)

    @property
    def hashes_type_code(self):
        return self._hashes_type_code

    @property
    def hashes_type_label(self):
        for h in HASHS_LIST:
            if int(h["code"]) == int(self.hashes_type_code):
                return h["name"]

    @hashes_type_code.setter
    def hashes_type_code(self, code):
        for h in HASHS_LIST:
            if int(h["code"]) == int(code):
                self._hashes_type_code = int(code)

    @property
    def request_working_folder(self):
        return os.path.join(app.config["DIR_LOCATIONS"]["hashcat_outputs"], self.session_id)

    @property
    def outfile_path(self):
        return os.path.join(self.request_working_folder, "output.txt")

    @property
    def potfile_path(self):
        if self.use_potfile:
            potfile_path = os.path.join(self.request_working_folder, "request.pot")
            FilesHelper.file_exists(potfile_path, create=True)
            return potfile_path

        return None

    @property
    def hashes(self):
        return FilesHelper.get_file_content(self.hashes_path)

    @property
    def is_archived(self):
        app.logger.debug("Nb folders in directory {} : {}".format(
                             str(self.request_working_folder),
                             str(FilesHelper.count_folders_in_dir(self.request_working_folder))
                        )
        )
        return True if not FilesHelper.count_folders_in_dir(self.request_working_folder) else False

    @hashes.setter
    def hashes(self, hashes):
        # create hashes file (will be decremented of found passwords during process)
        self.hashes_path = FilesHelper.create_new_file(
            file_path=self.request_working_folder,
            file_name="hashes.txt",
            content=hashes
        )

        # create a copy with reference of original list of required passwords
        FilesHelper.copy_file(
            source=self.hashes_path,
            target=os.path.join(self.request_working_folder, "hashes_original.txt")
        )

        # save nb of password in original file
        self.nb_password_to_find = FilesHelper.nb_lines_in_file(
            os.path.join(self.request_working_folder, "hashes_original.txt")
        )

    @property
    def dictionary_paths(self):
        if self._dictionary_paths:
            for d in self._dictionary_paths.split(','):
                d_folder, d_filename = FilesHelper.split_path(d, return_file_ext=False)
                yield d_filename

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
        for d in self._dictionary_paths.split(','):
            if not d.startswith(app.config["DIR_LOCATIONS"]["wordlists"]):
                return FilesHelper.get_file_content(d)

    @keywords.setter
    def keywords(self, keywords):
        keyword_file_path = FilesHelper.create_new_file(
            file_path=self.request_working_folder,
            file_name="keywords.txt",
            content=keywords
        )

        self.add_dictionary_paths(keyword_file_path, ref=False)

    @property
    def mask(self):
        return FilesHelper.get_file_content(self.mask_path)

    @property
    def has_mask(self):
        if self.mask_path and FilesHelper.file_exists(self.mask_path):
            return True
        return False

    @mask.setter
    def mask(self, mask):
        self.mask_path = FilesHelper.create_new_file(
            file_path=self.request_working_folder,
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
            app.logger.debug("extra options: "+str(self._extra_options))
            return json.loads(self._extra_options)

        return []

    def prepare_cracks(self):
        """
        Create a Crack instance for each hashcat instance to launch
        - cracks for each dictionary
        - crack for keywords
        - crack for mask
        - crack for bruteforce

        :return:
        """
        if self._dictionary_paths:
            for wordlist_file_path in self._dictionary_paths.split(','):
                app.logger.debug("Create new dictionary attack")
                _, dict_filename = FilesHelper.split_path(wordlist_file_path)
                new_dict_crack = Crack("Dictionary: "+str(FilesHelper.remove_ext_from_filename(dict_filename)))
                db.session.add(new_dict_crack)
                db.session.commit()

                self.cracks.append(new_dict_crack)
                new_dict_crack.build_crack_cmd(
                    attack_mode=0,
                    attack_file=wordlist_file_path
                )

        if self.mask_path:
            app.logger.debug("Mask path is "+str(self.mask_path)+": create a mask attack")
            new_mask_crack = Crack(name="Mask crack")
            db.session.add(new_mask_crack)
            db.session.commit()

            self.cracks.append(new_mask_crack)
            new_mask_crack.build_crack_cmd(
                attack_mode=3,
                attack_file=os.path.join(new_mask_crack.working_folder, "mask.hcmask"),
                crack_options=[{
                    "option": "--show"  # mask crack seems to require --show option
                }]
            )

        if self.bruteforce:
            app.logger.info("Create debug crack in request")
            new_bf_crack = Crack(name="Bruteforce")
            db.session.add(new_bf_crack)
            db.session.commit()

            self.cracks.append(new_bf_crack)
            new_bf_crack.build_crack_cmd(
                attack_mode=3,
                attack_file=None
            )

        db.session.commit()

    def is_expired(self):
        return (self.start_date + timedelta(days=self.duration)) <= datetime.now()

    def run_cracks(self):
        for c in self.cracks:
            c.run()

            if FilesHelper.nb_lines_in_file(self.hashes_path) == 0:
                self.close_crack_request("ALL_FOUND")
                break

            if self.is_expired():
                self.close_crack_request("EXPIRED")
                break

        self.close_crack_request("ALL_PERFORMED")
        return True

    def close_crack_request(self, mode):
        app.logger.debug("close request with code "+str(mode))
        if mode not in REQUESTS_CLOSE_MODES:
            mode = "UNDEFINED"

        self.end_mode = mode
        self.end_date = datetime.now()
        db.session.commit()

    @property
    def nb_password_found(self):
        if self.use_potfile:
            return FilesHelper.nb_lines_in_file(self.potfile_path)
        return FilesHelper.nb_lines_in_file(self.outfile_path)

    @property
    def status(self):
        if self.is_archived:
            return "archived"

        if not self.is_finished():
            return "running"

        if self.end_mode:
            return REQUESTS_CLOSE_MODES[self.end_mode]

        return "waiting"

    def is_finished(self):
        for c in self.cracks:
            if not c.end_mode:
                return False

        self.end_mode = "ALL_PERFORMED"
        db.session.commit()

        return True

    def force_close(self):
        # close celery task
        celery.control.revoke(self.celery_request_id)

        # force close all tasks
        for crack in self.cracks:
            crack.force_close()

        self.close_crack_request(mode="MANUAL")

    @property
    def cracks_progress(self):
        if not self.cracks:
            return 0

        nb_finished_cracks = 0
        for c in self.cracks:
            if c.end_date:
                nb_finished_cracks += 1

        return round((float(nb_finished_cracks) / len(self.cracks)) * 100, 2)

    @property
    def password_progress(self):
        if not self.nb_password_to_find:
            return 0

        return round((float(self.nb_password_found) / self.nb_password_to_find)*100, 2)
