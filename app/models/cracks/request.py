# standard imports
from datetime import datetime, timedelta
import uuid
import os
import json

# third party imports
from sqlalchemy.orm import relationship

# local imports
from server import app, celery
from app import db
from app.ref.hashes_list import HASHS_LIST
from app.classes.Wordlist import Wordlist
from app.helpers.files import FilesHelper
from app.models.cracks.entity import Crack
# do not remove, used in request relationships
from app.models.user import User
from app.ref.close_modes import REQUESTS_CLOSE_MODES


class CrackRequest(db.Model):
    """
    Model used to define Crack Request object.

    A crack request is created by each crack form submission.
    A crack request can trigger multiple cracks depending on form data submitted

    * Stored in cracks_requests table
    """
    __tablename__ = 'cracks_requests'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.Text, nullable=False, default="no name")
    celery_request_id = db.Column(db.Text, nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    session_id = db.Column(db.Text, nullable=False, default=str(uuid.uuid4()))
    _hashes_type_code = db.Column(db.Integer, nullable=False)
    hashed_file_contains_usernames = db.Column(db.Boolean, nullable=False, default=False)
    hashes_path = db.Column(db.Text, nullable=False, default="")
    nb_password_to_find = db.Column(db.Integer, nullable=False, default=0)
    _dictionary_paths = db.Column(db.Text, nullable=True)
    mask_path = db.Column(db.Text, nullable=True)
    bruteforce = db.Column(db.Boolean, nullable=False, default=False)
    use_potfile = db.Column(db.Boolean, nullable=False, default=False)
    _extra_options = db.Column(db.Text, nullable=True)
    start_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    end_date = db.Column(db.DateTime, nullable=True)
    end_mode = db.Column(db.Text, nullable=True)
    duration = db.Column(db.Integer, nullable=False, default=3)
    email_end_job_sent = db.Column(db.Boolean, nullable=False, default=False)

    cracks = relationship("Crack", back_populates="request")
    user = relationship("User", back_populates="cracks_requests")

    # GETTERS : DYNAMIC PROPERTIES
    @property
    def hashes_type_code(self):
        """
        return _hashes_type_code hybrid property (set as hybrid because it require a setter to check its validity)
        :return: <int>
        """
        return self._hashes_type_code

    @property
    def hashes_type_label(self):
        """
        property to get hash type label from hashes_type_code.
        The method search in ref HASH_LIST for the label
        :return: <str>
        """
        for h in HASHS_LIST:
            if int(h["code"]) == int(self.hashes_type_code):
                return h["name"]
        return ""

    @property
    def request_working_folder(self):
        """
        Method return request working folder
        working folder : output folder from user_id + request_id
        :return:
        """
        return os.path.join(
            app.config["DIR_LOCATIONS"]["hashcat_outputs"],
            "u_" + str(self.user_id),
            "req_" + str(self.id)
        )

    @property
    def outfile_path(self):
        """
        return output file path, output file is on request_working folder root)
        :return: <str> output file path
        """
        return os.path.join(self.request_working_folder, "output.txt")

    @property
    def potfile_path(self):
        """
        Retur potfile path (if request uses potfile)
        potfile is in request_working_folder root path
        :return:
        """
        if self.use_potfile:
            potfile_path = os.path.join(self.request_working_folder, "request.pot")
            FilesHelper.file_exists(potfile_path, create=True)
            app.logger.debug("get potfile_path :: potfile_path")
            return potfile_path
        app.logger.debug("get potfile_path :: request does not use potfile")
        return None

    @property
    def hashes(self):
        """
        :return: list of remaining hashes to crack (= content of request hashes file)
        """
        return FilesHelper.get_file_content(self.hashes_path)

    @property
    def dictionary_paths(self):
        """
        generator returning list of request dictionaries (keywords + dicts)
        :return:
        """
        if self._dictionary_paths:
            for d in self._dictionary_paths.split(','):
                d_folder, d_filename = FilesHelper.split_path(d, return_file_ext=False)
                yield d_filename

    @property
    def keywords(self):
        """
        return content of keyword file.
        Parse all request dictionnaries from self._dictionary_paths.
            * Return value if path not in the config dict folder
        :return: <str> / None
        """
        for d in self._dictionary_paths.split(','):
            if not d.startswith(app.config["DIR_LOCATIONS"]["wordlists"]):
                return FilesHelper.get_file_content(d)
        return None

    @property
    def has_mask(self):
        """
        Check if request has a mask
        :return: <bool>
        """
        if self.mask_path and FilesHelper.file_exists(self.mask_path):
            return True
        return False

    @property
    def mask(self):
        """
        :return: content of mask file
        """
        if self.has_mask:
            return FilesHelper.get_file_content(self.mask_path)
        return None

    @property
    def has_rules(self):
        """
        Check if rules_path property is not empty
        :return:
        """
        return True if self.rules_path else False

    @property
    def rules(self):
        """
        Generator to yield each rule file path
        :return:
        """
        if self.has_rules:
            for d in self.rules_path.split(','):
                yield d

    @property
    def extra_options(self):
        """
        :return: return content of request options as a list of dict (loaded from json in db)
        """
        if self._extra_options:
            app.logger.debug("extra options: "+str(self._extra_options))
            return json.loads(self._extra_options)

        return []

    @property
    def nb_password_found(self):
        """
        function to check nb of passwords found
            * from potfile (if potfile in use)
            * from output file if all cracks are finished
            * parsing all cracks outputs if cracks are running
        :return: <int>
        """
        if self.use_potfile:
            return FilesHelper.nb_lines_in_file(self.potfile_path)

        if self.is_finished:
            return FilesHelper.nb_lines_in_file(self.outfile_path)
        else:
            nb_passwords = 0
            for c in self.cracks:
                nb_passwords += c.nb_password_found
            return nb_passwords

    @property
    def status(self):
        """
        return current request status as string
        :return: <str>
        """
        if self.is_archived:
            return "archived"

        if not self.is_finished:
            return "running"

        if self.end_mode:
            return REQUESTS_CLOSE_MODES[self.end_mode]

        return "waiting"

    @property
    def cracks_progress(self):
        """
        get % of cracks finished (nb of finished crack / nb total of cracks)
        :return: <float>
        """
        if not self.cracks:
            return 0

        nb_finished_cracks = 0
        for c in self.cracks:
            if c.is_finished:
                nb_finished_cracks += 1

        return round((float(nb_finished_cracks) / len(self.cracks)) * 100, 2)

    @property
    def password_progress(self):
        """
        get % of password found (nb password found / nb total of passwords to find)
        :return: <float>
        """
        if not self.nb_password_to_find:
            return 0

        return round((float(self.nb_password_found) / self.nb_password_to_find)*100, 2)

    @property
    def is_finished(self):
        """
        check if request is finished (all cracks have en end_date)
        :return:
        """
        for c in self.cracks:
            if not c.is_finished:
                return False

        self.end_mode = "ALL_PERFORMED"
        db.session.commit()

        return True

    @property
    def is_expired(self):
        """
        check if request is expired (duration from start_date is expired)
        :return: <bool>
        """
        return (self.start_date + timedelta(days=self.duration)) <= datetime.now()

    @property
    def is_archived(self):
        """
        Check if request is archived.

        Archived means that cracks folders were removed from request_working_folder

        :return: <bool>
        """
        app.logger.debug("Nb folders in directory {} : {}".format(
                             str(self.request_working_folder),
                             str(FilesHelper.count_folders_in_dir(self.request_working_folder))
                        )
        )
        return True if not FilesHelper.count_folders_in_dir(self.request_working_folder) else False

    # SETTERS
    @hashes_type_code.setter
    def hashes_type_code(self, code):
        """
        setter of _hashes_type_code hybrid property.
        Checks that hashes type code exists in reference HASH_LIST
        """
        for h in HASHS_LIST:
            if int(h["code"]) == int(code):
                self._hashes_type_code = int(code)

    @hashes.setter
    def hashes(self, hashes):
        """
        Set request hashes:
            - write hashes in a hashes.txt file on root of request working folder
                * this file will be decremented when hashes are found
            - write hashes in a hashes_original.txt
                * to keep a backup of original hashes

        init value of nb_password_to_find with count of lines in hashes_original.txt file

        :param hashes: <str>
        """
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

    @keywords.setter
    def keywords(self, keywords):
        """
        From user provided keywords:
            - create a keywords.txt file on working folder root
            - add keywords.txt file to list of request dictionaries

        :param keywords: <str>
        """
        keyword_file_path = FilesHelper.create_new_file(
            file_path=self.request_working_folder,
            file_name="keywords.txt",
            content=keywords
        )

        self.add_dictionary_paths(os.path.join(self.request_working_folder, keyword_file_path))

    @mask.setter
    def mask(self, mask):
        """
        Set content of user provided mask in a mask.hcmask file on root of request working folder
        :param mask : <str>
        """
        self.mask_path = FilesHelper.create_new_file(
            file_path=self.request_working_folder,
            file_name="mask.hcmask",
            content=mask
        )

    # METHODS
    def init_request_folder(self):
        """
        method used to create the request folder (folder where intput and output file will be stored)
        :return:
        """
        self.session_id = str(uuid.uuid4())
        if not FilesHelper.dir_exists(self.request_working_folder):
            app.logger.debug("create directory "+str(self.request_working_folder))
            os.makedirs(self.request_working_folder)
        FilesHelper.file_exists(self.outfile_path, create=True)

    def add_dictionary_paths(self, dict_paths):
        """
        Method to add a dictionnary path.
            * for keywords (=custom wordlist): wordlist path is relative to working folder
            * for standard wordlists : wordlist path is relative to config wordlist folder

        note: list of dict in db (_dictionary_paths) is a comma separated list of wordlists absolute path

        :param list_of_wordlists: <str> (path of wordlist) or <list> (list of wordlists path)
        :param ref: <bool> wordlist is in the wordlist folder from config
        :return:
        """
        if not isinstance(dict_paths, list):
            dict_paths = [dict_paths]

        # split current list of dictionnary in db by ","
        current_dict_path_list = self._dictionary_paths.split(',') if self._dictionary_paths else []

        # add each wordlist absolute path to current list of wordlist
        for d in dict_paths:
            dict_path = d.full_filepath if isinstance(d, Wordlist) else d
            if dict_path not in current_dict_path_list:
                current_dict_path_list.append(dict_path)

        # set dictionary path in db to list of wordlists (comma separated)
        self._dictionary_paths = ','.join(current_dict_path_list)

    def add_rules(self, rule_objects):
        """
        From rule files path provided, update options to add --rules-file options with each rule file provided
        :param rule_objects: <path> or <list of path>
        """
        current_options = self.extra_options
        for r in rule_objects:
            current_options.append({
                "option": "--rules-file",
                "value": r.full_filepath
            })

        self._extra_options = json.dumps(current_options, indent=4)


    def prepare_cracks(self):
        """
        Create a Crack instance for each hashcat instance to launch + build hashcat command to launch
            - cracks for each dictionary
            - crack for keywords
            - crack for mask
            - crack for bruteforce

        Note: this method only create cracks instances in db (but does not run them)

        :return:
        """
        # create a crack for each worlist in _dictionary_paths
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

        # create mask crack if mask is defined
        if self.has_mask:
            app.logger.debug("Mask path is "+str(self.mask_path)+": create a mask attack")
            new_mask_crack = Crack(name="Mask crack")
            db.session.add(new_mask_crack)
            db.session.commit()

            self.cracks.append(new_mask_crack)
            new_mask_crack.build_crack_cmd(
                attack_mode=3,
                attack_file=os.path.join(self.request_working_folder, "mask.hcmask"),
            )

        # create bruteforce attack if required
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

    def run_cracks(self):
        """
        Method to run all request cracks.

        Method stops to launch cracks :
            - when all hashes were found
            - when crack duration is expired

        :return:
        """
        for c in self.cracks:
            if not c.run():
                break

            if FilesHelper.nb_lines_in_file(self.hashes_path) == 0:
                self.close_crack_request("ALL_FOUND")
                break

            if self.is_expired:
                self.close_crack_request("EXPIRED")
                break

        self.close_crack_request("ALL_PERFORMED")
        return True

    def close_crack_request(self, mode):
        """
        method to soft close crack requests:
            * set an end_mode
            * set an end_date

        :param mode: <str> close mode code (from REQUESTS_CLOSE_MODES)
        :return:
        """
        app.logger.debug("close request with code "+str(mode))
        if mode not in REQUESTS_CLOSE_MODES:
            mode = "UNDEFINED"

        self.end_mode = mode
        self.end_date = datetime.now()
        db.session.commit()

    def force_close(self):
        """
        Method to force close a request:
            1 - kill celery task
            2 - force_close all cracks
            3 - call request soft close

        :return:
        """
        # close celery task
        celery.control.revoke(self.celery_request_id)

        # force close all tasks
        for crack in self.cracks:
            crack.force_close()

        self.close_crack_request(mode="MANUAL")
