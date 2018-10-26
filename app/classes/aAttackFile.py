import os

from app.helpers.files import FilesHelper


class AbstractAttackFile(object):
    config = None
    base_folder = None

    def __init__(self, filepath):
        self.filepath = None
        self.name = None
        self.default = False

        self.set_from_filepath(filepath)

    def set_from_filepath(self, filepath):
        if type(self).is_valid(filepath):
            self.filepath = filepath
            if type(self).config and filepath in type(self).config:
                self.set_name(config=type(self).config[filepath])
                self.set_default(config=type(self).config[filepath])
            else:
                self.name = FilesHelper.remove_ext_from_filename(self.filepath)

    def set_name(self, config=None):
        if config and "name" in config:
            self.name = config["name"]
        else:
            self.name = FilesHelper.remove_ext_from_filename(self.filepath)

    def set_default(self, config=None, value=False):
        if config and "default" in config and isinstance(config["default"], bool):
            self.default = config["default"]
        elif not config and isinstance(value, bool):
            self.default = value

    @property
    def full_filepath(self):
        return os.path.join(type(self).base_folder, self.filepath)

    @classmethod
    def is_valid(cls, filename):
        for f in FilesHelper.get_available_files(cls.base_folder):
            if f == filename:
                return True
        return False

    @classmethod
    def get_all_as_instances(cls):
        for f in FilesHelper.get_available_files(cls.base_folder):
            yield cls(filepath=f)

    @classmethod
    def get_all_filename(cls):
        return FilesHelper.get_available_files(cls.base_folder)
