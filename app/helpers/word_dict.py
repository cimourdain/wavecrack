
from server import app
from app.helpers.files import FilesHelper


WORDLISTS_FOLDER = app.config["DIR_LOCATIONS"]["wordlists"]


class WordDictHelper(object):

    @staticmethod
    def get_rules_files():
        return FilesHelper.get_available_files(WORDLISTS_FOLDER)

    @staticmethod
    def is_valid_wordlist_file(file_path):
        if FilesHelper.file_exists(file_path, folder=app.config["DIR_LOCATIONS"]["wordlists"]):
            return True

        return False
