# standard imports
import uuid
import os

# local imports
from server import app
from app.classes.cmd import Cmd
from app.helpers.files import FilesHelper
from app.ref.hashcat_options import HASHCAT_OPTIONS, ATTACK_MODES
from app.helpers.text import TextHelper
from app.helpers.word_dict import WordDictHelper

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

DEFAULT_OPTIONS = [
    {
        "option": "--show"
    },
    {
        "option": "--remove"
    }
]

class Crack(object):

    def __init__(self, input_hashfile, hashes_type_code, attack_mode_code, attack_files, options,
                 output_file="output.txt", log=False, session_id=None):

        self.hashcat_cmd = app.config["APP_LOCATIONS"]["hashcat"]
        self.working_folder = None
        self.input_hashfile_abs_path = None
        self.hashes_type_code = 0
        self.output_abs_path = None
        self.options = []
        self.attack_mode_code = 0
        self.attack_files = []
        self.session_id = None

        self.set_input_hashfile(input_hashfile, output_filename=output_file, log=log)
        self.set_hashes_type_code(hashes_type_code)
        self.set_options(DEFAULT_OPTIONS)
        self.set_options(options)
        self.set_attack_mode_code(attack_mode_code)
        self.set_attack_files(attack_files)
        self.set_session_id(session_id)

    """
    SET HASHFILE
    """
    def set_input_hashfile(self, input_hashfile, output_filename, log):
        self.working_folder = os.path.dirname(os.path.abspath(input_hashfile))

        self.input_hashfile_abs_path = input_hashfile
        self.output_abs_path = FilesHelper.file_exists(
            file_path=os.path.join(self.working_folder, output_filename),
            create=True
        )

        if log:
            log_file = os.path.join(self.working_folder, "hashcat_log.txt")
            self.set_option({
                "option": "--debug-file",
                "value": log_file
            })

    def set_hashes_type_code(self, code):
        self.hashes_type_code = int(code)

    def set_attack_mode_code(self, attack_mode_code):
        if str(attack_mode_code) in ATTACK_MODES:
            self.attack_mode_code = int(attack_mode_code)

    def set_attack_files(self, files_list):
        if isinstance(files_list, basestring):
            self.set_attack_file(files_list)
        elif isinstance(files_list, list):
            for f in files_list:
                self.set_attack_file(f)

    def set_attack_file(self, f):
        """
        check if file exists either in list of wordlists or in crack folder
        """
        if WordDictHelper.is_valid_wordlist_file(f):
            self.attack_files.append(f)
        elif FilesHelper.file_exists(file_path=f):
            self.attack_files.append(f)

    def set_session_id(self, session_id):
        if session_id:
            self.set_option({
                "option": "--session",
                "value": session_id
            })

    """
    SET OPTIONS
    """
    def set_options(self, options):
        if options:
            for option in options:
                self.set_option(option)

    def set_option(self, option):
        new_option = CrackOption(option.get("option", None), option.get("value", None))
        if new_option.option:
            self.options.append(new_option)

            if new_option.option == "--attack-mode":
                self.attack_mode_code = new_option.value

    def build_cmd_options(self):
        options_cmd_str = ""
        for option in self.options:
            options_cmd_str += option.get_option_cmd()

        return options_cmd_str

    def build_run_cmd(self):
        cmd = "{} -m {} -a {} -o {} {} {} {}".format(
            self.hashcat_cmd,
            self.hashes_type_code,
            self.attack_mode_code,
            self.output_abs_path,
            self.build_cmd_options(),
            self.input_hashfile_abs_path,
            " ".join(self.attack_files)
        )

        return cmd


class CrackOption(object):
    def __init__(self, option, value=None):
        self.option = None
        self.value = None

        self.set_option(option)
        self.set_value(value)

    def set_option(self, option):
        if option and option in HASHCAT_OPTIONS:
            self.option = option
        return True

    def set_value(self, value):
        if value:
            if "values" in HASHCAT_OPTIONS[self.option] and str(value) in HASHCAT_OPTIONS[self.option]["values"]:
                self.value = value
            elif HASHCAT_OPTIONS[self.option]["type"]:
                if HASHCAT_OPTIONS[self.option]["type"] == "Num" and TextHelper.is_int(value):
                    self.value = value
                elif HASHCAT_OPTIONS[self.option]["type"] == "File" and FilesHelper.file_exists(value):
                    self.value = value
                elif HASHCAT_OPTIONS[self.option]["type"] == "Dir" and FilesHelper.dir_exists(value):
                    self.value = value
                elif HASHCAT_OPTIONS[self.option]["type"] in ["Str", "Rule", "CS"] and isinstance(value, basestring):
                    self.value = value
                elif HASHCAT_OPTIONS[self.option]["type"] == "Char" \
                        and isinstance(value, basestring) and len(value) == 1:
                    self.value = value
        return True

    def get_option_cmd(self):
        if HASHCAT_OPTIONS[self.option]["type"]:
            if self.value:
                if HASHCAT_OPTIONS[self.option]["type"] == "Char":
                    return "{}='{}' ".format(self.option, self.value)
                else:
                    return "{}={} ".format(self.option, self.value)
            return ""
        return self.option
