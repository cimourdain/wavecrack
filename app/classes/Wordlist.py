from server import app
from app.classes.aAttackFile import AbstractAttackFile


class Wordlist(AbstractAttackFile):
    base_folder = app.config["DIR_LOCATIONS"]["wordlists"]
    config = app.config["WORDLIST_SETUP"]


