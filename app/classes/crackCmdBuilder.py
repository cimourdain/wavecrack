# local imports
from server import app
from app.helpers.files import FilesHelper
from app.ref.hashcat_options import HASHCAT_OPTIONS, ATTACK_MODES
from app.helpers.text import TextHelper
from app.helpers.word_dict import WordDictHelper


DEFAULT_OPTIONS_PER_ATTACK_MODE = {
    0: [{
        "option": "--show"
    }]
}


class CrackCmdBuilder(object):

    def __init__(self, source_crack, attack_mode_code, attack_files, options, use_potfile=True):

        app.logger.info("Create new crack "+str(source_crack.id))
        self.source_crack = source_crack
        self.hashcat_cmd = app.config["APP_LOCATIONS"]["hashcat"]

        self.attack_mode_code = 0
        self.attack_files = []
        self.options = []

        self.set_attack_mode_code(attack_mode_code)

        self.set_default_options(DEFAULT_OPTIONS_PER_ATTACK_MODE)
        self.set_options(options)
        if use_potfile:
            self.set_potfile_option()
        self.set_session_id_option()

        self.set_attack_files(attack_files)

    """
    SET PARAMS
    """
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

    """
    SET OPTIONS
    """
    def set_potfile_option(self):
        if self.source_crack.potfile_path:
            self.set_option({
                "option": "--potfile-path",
                "value": self.source_crack.potfile_path
            })
        else:
            self.set_option({
                "option": "--potfile-disable"
            })

    def set_session_id_option(self):
        if self.source_crack.request.session_id:
            self.set_option({
                "option": "--session",
                "value": self.source_crack.request.session_id
            })

    def set_default_options(self, default_options_per_attack_mode):
        for attack_mode, options in default_options_per_attack_mode.items():
            app.logger.debug("crack :: set_default_options :: key: "+str(attack_mode))
            app.logger.debug("crack :: set_default_options :: value: "+str(options))
            if attack_mode == self.attack_mode_code:
                self.set_options(options)

    def set_options(self, options):
        app.logger.debug("crack :: set_options :: new options "+str(options))
        if options:
            for option in options:
                self.set_option(option)

    def option_allowed(self, option):
        app.logger.debug("crack :: option_allowed :: check if "+str(option["option"])+" can be added with attack mode " + str(self.attack_mode_code))
        if option["option"] == "--rules-file" and self.attack_mode_code != 0:
            return False
        return True

    def set_option(self, option):
        app.logger.debug("crack :: set_option :: set option "+str(option))
        if self.option_allowed(option):
            new_option = CrackOption(option.get("option", None), option.get("value", None))
            if new_option.option:
                app.logger.debug("new option is valid and object created, add it to self.options")
                self.options.append(new_option)

                if new_option.option == "--attack-mode":
                    self.attack_mode_code = new_option.value

                if new_option.option == "--rules-file" and self.attack_mode_code == 0:
                    pass

    def build_cmd_options(self):
        options_cmd_str = ""
        for option in self.options:
            options_cmd_str += option.get_option_cmd()
        app.logger.debug("crack :: build_cmd_options :: cmd options "+str(options_cmd_str))
        return options_cmd_str

    def build_run_cmd(self):
        cmd = "{} -m {} -a {} -o {} {} {} {}".format(
            self.hashcat_cmd,
            self.source_crack.request.hashes_type_code,
            self.attack_mode_code,
            self.source_crack.output_file_path,
            self.source_crack.request.hashes_path,
            " ".join(self.attack_files),
            self.build_cmd_options(),
        )

        return cmd


class CrackOption(object):
    def __init__(self, option, value=None):
        app.logger.info("Create new crack option "+str(option)+" : "+str(value))
        self.option = None
        self.value = None

        self.set_option(option)
        self.set_value(value)

    def set_option(self, option):
        if option and option in HASHCAT_OPTIONS:
            self.option = option
        app.logger.debug("option name set to " + str(self.option))
        return True

    def set_value(self, value):
        if value:
            if "values" in HASHCAT_OPTIONS[self.option] and str(value) in HASHCAT_OPTIONS[self.option]["values"]:
                self.value = value
            elif HASHCAT_OPTIONS[self.option]["type"]:
                app.logger.debug("check if option value "+str(value)+" matches the required type "
                                 + str(HASHCAT_OPTIONS[self.option]["type"]))
                if HASHCAT_OPTIONS[self.option]["type"] == "Num" and TextHelper.is_int(value):
                    app.logger.debug(str(value) + " is a valid integer")
                    self.value = value
                elif HASHCAT_OPTIONS[self.option]["type"] == "File" and FilesHelper.file_exists(value):
                    app.logger.debug(str(value) + " is a valid file")
                    self.value = value
                elif HASHCAT_OPTIONS[self.option]["type"] == "Dir" and FilesHelper.dir_exists(value):
                    app.logger.debug(str(value) + " is a valid directory")
                    self.value = value
                elif HASHCAT_OPTIONS[self.option]["type"] in ["Str", "Rule", "CS"] and isinstance(value, basestring):
                    app.logger.debug(str(value) + " is a valid string")
                    self.value = value
                elif HASHCAT_OPTIONS[self.option]["type"] == "Char" \
                        and isinstance(value, basestring) and len(value) == 1:
                    app.logger.debug(str(value) + " is a valid char")
                    self.value = value
                if not self.value:
                    app.logger.error(str(value) + " is not a valid "+str(HASHCAT_OPTIONS[self.option]["type"]))
        app.logger.debug("option value set to "+str(self.value))
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
