from server import app

from app.classes.aAttackFile import AbstractAttackFile


class Rule(AbstractAttackFile):
    base_folder = app.config["DIR_LOCATIONS"]["rules"]
    config = app.config["RULES_SETUP"]
