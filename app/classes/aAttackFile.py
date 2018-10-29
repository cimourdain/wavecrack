# coding: utf8
import os

from app.helpers.files import FilesHelper


class AbstractAttackFile(object):
    config = None
    base_folder = None

    def __init__(self, filepath=None, config=None, source_folder=None):
        self.source_folder = source_folder if source_folder else type(self).base_folder
        self.filepath = None
        self.name = None
        self.active = False

        if filepath:
            self.set_from_filepath(filepath)
        elif config:
            self.set_from_config(config)

    def set_from_filepath(self, filepath):
        self.filepath = filepath
        self.set_name()

    def set_from_config(self, config):
        self.filepath = config["file"]
        self.set_name(name=config["name"] if "name" in config else None)
        self.set_active(active=config["active"] if "active" in config else None)

    def set_name(self, name=None):

        self.name = name if name else FilesHelper.remove_ext_from_filename(self.filepath)
        print("set name to "+self.name)

    def set_active(self, active=False):
        if isinstance(active, bool):
            self.active = active

    @property
    def full_filepath(self):
        return os.path.join(self.source_folder, self.filepath)

    @classmethod
    def is_valid(cls, filename, folder=None):
        if not folder:
            folder = cls.base_folder
        for f in FilesHelper.get_available_files(folder):
            if f == filename:
                return True
        return False

    @classmethod
    def get_all_from_config_and_ref_folder_as_instances(cls):

        files_defined_in_config = []
        for cf in cls.config:
            if "file" in cf and cf["file"] not in files_defined_in_config:
                files_defined_in_config.append(cf["file"])
                yield cls(config=cf)

        for f in FilesHelper.get_available_files(cls.base_folder):
            if f not in files_defined_in_config:
                yield cls(filepath=f)

    @classmethod
    def get_all_from_config_and_ref_folder_as_filename(cls):
        files_defined_in_config = []
        for cf in cls.config:
            if "file" in cf and cf["file"] not in files_defined_in_config:
                files_defined_in_config.append(cf["file"])
                yield cf["file"]

        for f in FilesHelper.get_available_files(cls.base_folder):
            if f not in files_defined_in_config:
                yield f
