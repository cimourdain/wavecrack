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


DEFAULT_OPTIONS_PER_ATTACK_MODE = {
    0: [{
        "option": "--show"
    }]
}


class Crack(object):

    def __init__(self, input_hashfile, hashes_type_code, attack_mode_code, attack_files, options,
                 output_path, session_id=None):

        self.hashcat_cmd = app.config["APP_LOCATIONS"]["hashcat"]
        self.working_folder = None
        self.input_hashfile_abs_path = None
        self.hashes_type_code = 0
        self.output_abs_path = None
        self.options = []
        self.attack_mode_code = 0
        self.attack_files = []
        self.session_id = None

        self.set_attack_mode_code(attack_mode_code)
        self.set_input_hashfile(input_hashfile, output_path=output_path)
        self.set_hashes_type_code(hashes_type_code)

        self.set_default_options(DEFAULT_OPTIONS_PER_ATTACK_MODE)
        self.set_options(options)

        self.set_attack_files(attack_files)
        self.set_session_id(session_id)

    """
    SET HASHFILE
    """
    def set_input_hashfile(self, input_hashfile, output_path):
        self.working_folder = os.path.dirname(os.path.abspath(input_hashfile))

        self.input_hashfile_abs_path = input_hashfile
        FilesHelper.file_exists(output_path, create=True)
        self.output_abs_path = output_path

    def set_hashes_type_code(self, code):
        self.hashes_type_code = int(code)

    def set_attack_mode_code(self, attack_mode_code):
        if str(attack_mode_code) in ATTACK_MODES:
            self.attack_mode_code = int(attack_mode_code)
            if self.attack_mode_code == 3:
                self.set_option({
                    "option": "--show"
                })

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
    def set_default_options(self, default_options_per_attack_mode):
        for attack_mode, options in default_options_per_attack_mode.items():
            print("key: "+str(attack_mode))
            print("value: "+str(options))
            if attack_mode == self.attack_mode_code:
                self.set_options(options)

    def set_options(self, options):
        print("new options "+str(options))
        if options:
            for option in options:
                self.set_option(option)

    def option_allowed(self, option):
        print("check if "+str(option["option"])+" can be added with attacj mode "+str(self.attack_mode_code))
        if option["option"] == "--rules-file" and self.attack_mode_code != 0:
            return False
        return True

    def set_option(self, option):
        print("set option "+str(option))
        if self.option_allowed(option):
            new_option = CrackOption(option.get("option", None), option.get("value", None))
            if new_option.option:
                self.options.append(new_option)

                if new_option.option == "--attack-mode":
                    self.attack_mode_code = new_option.value

                if new_option.option == "--rules-file" and self.attack_mode_code == 0:
                    pass

    def build_cmd_options(self):
        options_cmd_str = ""
        for option in self.options:
            options_cmd_str += option.get_option_cmd()
        print("cmd options "+str(options_cmd_str))
        return options_cmd_str

    def build_run_cmd(self):
        cmd = "{} -m {} -a {} -o {} {} {} {}".format(
            self.hashcat_cmd,
            self.hashes_type_code,
            self.attack_mode_code,
            self.output_abs_path,
            self.input_hashfile_abs_path,
            " ".join(self.attack_files),
            self.build_cmd_options(),
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
        return self.option + " "
