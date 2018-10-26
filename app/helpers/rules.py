import os
from server import app
from app.helpers.files import FilesHelper


class RulesHelper(object):
    @staticmethod
    def get_rules_files():
        all_rules = []
        all_rules.extend(FilesHelper.get_available_files(app.config["DIR_LOCATIONS"]["rules"]))
        return all_rules

