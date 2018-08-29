import os
from server import app
from app.ref.languages_list import ALL_LANGUAGES


class WordsHelper(object):
    @staticmethod
    def get_available_languages():
        available_languages = []
        for dirpath, dirs, files in os.walk(app.config["APP_LOCATIONS"]["wordlists"]):
            language_folder = os.path.basename(os.path.normpath(dirpath))
            print language_folder
            if files and language_folder.lower() in ALL_LANGUAGES:
                available_languages.append({
                    "language_iso_code": language_folder.lower(),
                    "language": ALL_LANGUAGES[language_folder.lower()]
                })

        return available_languages
