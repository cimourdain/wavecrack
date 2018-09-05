# standard imports
import uuid

# local imports
from server import app
from app.classes.cmd import Cmd
from app.helpers.hashes import HashesHelper
from app.helpers.attack_modes import AttackModeHelper
from app.helpers.files import FilesHelper

# Hashcat options details :
#     Call the program through hashcat_location
#     . Option -a 0 or -a 3 : Attack-mode. 0 Straight or 3 Brute-force
#     . Option -m hashtype_selected : Hash-type
#     . Option --session "".join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(6) : Assign different name to cracks to be able to launch them concurrently
#     . Option -p separator : Define separator character between hash and password in output files. By default, it's hash:password
#     . Option -o output_file_name : Output file path
#     . Option --potfile-disable : Disable .pot file
#     . Option --status et --status-timer: Write crack status in a file regularly
#     . Option --remove et --remove-timer: Remove of hash once it is cracked in input file
#     . Option hashfile : Specify input hashes file
#     . Option wordlists_location + "wordlist.txt" :	 Specify wordlist to use


# https://github.com/hashcat/hashcat/blob/master/docs/status_codes.txt
# status codes on exit:
# =====================
#
# -2 = gpu-watchdog alarm
# -1 = error
#  0 = OK/cracked
#  1 = exhausted
#  2 = aborted
#  3 = aborted by checkpoint
#  4 = aborted by runtime


class Crack(object):

    def __init__(self, hash_type_code, attack_mode_code, outfile_path, rules_files_path=None, separator=None):
        self.hash_type_code = self.set_hash_type_code(hash_type_code)
        self.attack_mode_code = self.set_attack_mode_code(attack_mode_code)
        self.outfile_path = self.set_outfile_path(outfile_path)
        self.separator = self.set_separator(separator)
        self.session_id = self.set_session_id()
        self.rules_files_path = self.set_rules_files_path(rules_files_path)

    """
    SETTERS
    """
    def set_hash_type_code(self, hash_type_code, default_hash_type_code=0):
        if HashesHelper.validate_code(hash_type_code):
            return int(hash_type_code)

        return default_hash_type_code

    def set_attack_mode_code(self, attack_mode_code, default_attack_mode=0):

        if AttackModeHelper.validate_code(attack_mode_code):
            return int(attack_mode_code)

        return default_attack_mode

    def set_outfile_path(self, outfile_path):
        if FilesHelper.file_exists(outfile_path):
            return outfile_path

        return None

    def set_separator(self, separator, default_separator=':'):
        if isinstance(separator, basestring) and len(separator) == 1:
            return separator
        return default_separator

    def set_session_id(self):
        return uuid.uuid4()

    def set_rules_files_path(self, rules_files_path):
        rules_files = []
        for rule_file_path in rules_files_path:
            if FilesHelper.file_exists(rules_files_path, create=False):
                rules_files.append(rules_files_path)

        return rules_files


    """
    GETTERS
    """
    def get_hash_type_code(self):
        return self.hash_type_code

    def get_attack_mode_code(self):
        return self.attack_mode_code

    def get_outfile_path(self):
        return self.outfile_path

    def get_separator(self):
        return self.separator

    def get_session_id(self):
        return self.session_id

    def get_rules_files_path(self):
        return self.rules_files_path

    def run(self):
        # prepare hashcat shell cmd as string
        hashcat_shell_cmd = app.config["APP_LOCATIONS"]["hashcat"]

        # run shell cmd
        return_code, output, errors = Cmd.run_cmd(hashcat_shell_cmd)

