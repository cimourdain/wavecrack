import os
from server import app


class RulesHelper(object):
    @staticmethod
    def parse_dict_folders():
        for dirpath, dirs, files in os.walk(app.config["APP_LOCATIONS"]["rules"]):
            language_folder = os.path.basename(os.path.normpath(dirpath))
            yield language_folder, files

    @staticmethod
    def get_available_wordlists():
        available_wordlists = []
        for language_folder, files in RulesHelper.parse_dict_folders():
                available_wordlists.extend(files)

        return available_wordlists
