# local imports
from server import app
from app.helpers.files import FilesHelper
from app.ref.hashcat_options import HASHCAT_OPTIONS, ATTACK_MODES
from app.helpers.text import TextHelper
from app.helpers.word_dict import WordDictHelper

# list of detault options to set per attack mode
DEFAULT_OPTIONS_PER_ATTACK_MODE = {
    # 0: [{
    #     "option": "--show"
    # }]
}


class CrackCmdBuilder(object):
    """
    Class used to build the hashcat command for a crack.
    """

    def __init__(self, source_crack, attack_mode_code, attack_files, options):
        """
        init crack command.

        :param source_crack: <Crack> object
        :param attack_mode_code: <int> hashcat attack mode (-a option)
        :param attack_files: [<str>] or <str> (dict, wordlists, masks) to apply on hashcat command (absolute paths)
        :param options: [<dict>] list of dict containing options.

        Note: options dict must have the following form:
            {
                "option": "option_name",
                "value": "option_value" # optional
            }

        Note: hash_type_code, attack_mode and output file are not handled as options but as parameter
        (see build_run_cmd())
            * hash_type_code: is inherited from the source crack parent request
            * attack_mode: is set as a parameter
            * output file: is inherited from the source crack
        """
        app.logger.info("Create new crack "+str(source_crack.id))
        self.source_crack = source_crack
        self.hashcat_cmd = app.config["APP_LOCATIONS"]["hashcat"]

        self.hash_type_code = self.source_crack.request.hashes_type_code
        self.attack_mode_code = 0
        self.output_file_path = self.source_crack.output_file_path
        self.attack_files = []
        self.options = []

        self.set_attack_mode_code(attack_mode_code)

        self.set_default_options(DEFAULT_OPTIONS_PER_ATTACK_MODE)
        self.set_options(options)
        self.set_potfile_option(use_potfile=self.source_crack.request.use_potfile)
        self.set_session_id_option()

        self.set_attack_files(attack_files)

    """
    SET PARAMS
    """
    def set_attack_mode_code(self, attack_mode_code):
        """
        Set hashcat attack mode code. Used to define the -a option in hashcat command.

        :param attack_mode_code: <int>
        :return:
        """
        if str(attack_mode_code) in ATTACK_MODES:
            self.attack_mode_code = int(attack_mode_code)

    def set_attack_files(self, files_list):
        """
        call the set_attack_file:
            * for each file in list if files_list is a list
            * for the string if files_list is a string

        :param files_list: <str> or [<str>]
        :return:
        """
        if isinstance(files_list, basestring):
            self.set_attack_file(files_list)
        elif isinstance(files_list, list):
            for f in files_list:
                self.set_attack_file(f)

    def set_attack_file(self, f):
        """
        check if file exists either in list of wordlists or in crack folder
        :param f: file absolute path
        """
        if WordDictHelper.is_valid_wordlist_file(f):
            self.attack_files.append(f)
        elif FilesHelper.file_exists(file_path=f):
            self.attack_files.append(f)

    """
    SET OPTIONS
    """
    def set_potfile_option(self, use_potfile=False):
        """
        Method to define usage of potfile option.
        if use_potfile arg is True and potfile path is defined on request level, the set optfile path option
        else, set option to disable potfile.

        Note: force disable potfile because defaulf use the hashcat potfile

        :param use_potfile: <bool>
        :return:
        """
        if use_potfile and self.source_crack.request.potfile_path:
            self.set_option({
                "option": "--potfile-path",
                "value": self.source_crack.request.potfile_path
            })
        else:
            self.set_option({
                "option": "--potfile-disable"
            })

    def set_session_id_option(self):
        """
        Method to set session_id

        :return:
        """
        if self.source_crack.request.session_id:
            self.set_option({
                "option": "--session",
                "value": self.source_crack.request.session_id
            })

    def set_default_options(self, default_options_per_attack_mode):
        """
        method to set default options (not used)

        :param default_options_per_attack_mode: <dict> (see above DEFAULT_OPTIONS_PER_ATTACK_MODE)
        :return:
        """
        for attack_mode, options in default_options_per_attack_mode.items():
            app.logger.debug("crack :: set_default_options :: key: "+str(attack_mode))
            app.logger.debug("crack :: set_default_options :: value: "+str(options))
            if attack_mode == self.attack_mode_code:
                self.set_options(options)

    def set_options(self, options):
        """
        method to launch the set_option for each individual option
        :param options: [<dict>] of options (see __init__ doc for format)
        :return:
        """
        app.logger.debug("crack :: set_options :: new options "+str(options))
        if options:
            for option in options:
                self.set_option(option)

    def option_allowed(self, option):
        """
        Method to check if an option is allowed

        -> prevent use of --rule-file option with attack mode != 0
        -> set attack_mode_code, hash_type_code or output_file_path if attempt to set them as options

        :param option: <dict>
        :return:
        """
        app.logger.debug("crack :: option_allowed :: check if "+str(option["option"])+" can be added with attack mode " + str(self.attack_mode_code))
        if option["option"] == "--rules-file" and self.attack_mode_code != 0:
            return False
        elif option["option"] in ["--attack-mode", "-a"] and TextHelper.is_int(option["value"]):
            self.attack_mode_code = int(option["value"])
            return False
        elif option["option"] in ["--hash-type", "-m"] and TextHelper.is_int(option["value"]):
            self.hash_type_code = int(option["value"])
            return False
        elif option["option"] in ["--outfile", "-o"] and FilesHelper.file_exists(option["value"]):
            self.output_file_path = int(option["value"])
            return False
        return True

    def set_option(self, option):
        """
        Method to set option.
            * check if option is allowed
            * create new CrackOption instance
            * add CrackOption to self.options

        :param option: <dict>(see __init__ doc for format)
        :return:
        """
        app.logger.debug("crack :: set_option :: set option "+str(option))
        if self.option_allowed(option):
            new_option = CrackOption(option.get("option", None), option.get("value", None))
            if new_option.option:
                app.logger.debug("new option is valid and object created, add it to self.options")
                self.options.append(new_option)

    def build_cmd_options(self):
        """
        Method to build command list of options (from list of self.options)

        :return: <str>
        """
        options_cmd_str = ""
        for option in self.options:
            options_cmd_str += option.get_option_cmd()
        app.logger.debug("crack :: build_cmd_options :: cmd options "+str(options_cmd_str))
        return options_cmd_str

    def build_run_cmd(self):
        """
        Method to build complete hashcat command

        :return: <str>
        """
        cmd = "{} -m {} -a {} -o {} {} {} {}".format(
            self.hashcat_cmd,
            self.hash_type_code,
            self.attack_mode_code,
            self.output_file_path,
            self.source_crack.request.hashes_path,
            " ".join(self.attack_files),
            self.build_cmd_options(),
        )

        return cmd


class CrackOption(object):
    """
    Class of an hashcat comand option
    """
    def __init__(self, option, value=None):
        """
        Init new option with an option name and value

        :param option: <str>
        :param value: <str>
        """
        app.logger.info("Create new crack option "+str(option)+" : "+str(value))
        self.option = None
        self.value = None

        self.set_option(option)
        self.set_value(value)

    def set_option(self, option):
        """
        Option setter, check that option name is in HASHCAT_OPTIONS ref list

        :param option: <str>
        :return: <bool>
        """
        if option and option in HASHCAT_OPTIONS:
            self.option = option
        app.logger.debug("option name set to " + str(self.option))
        return True

    def set_value(self, value):
        """
        Set option value.

        This method check that the value provided matches the required type (from HASHCAT_OPTIONS)
        :param value:
        :return:
        """
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
        """
        Method to build the hashcat option command
        :return: <str>
        """
        if HASHCAT_OPTIONS[self.option]["type"]:
            if self.value:
                if HASHCAT_OPTIONS[self.option]["type"] == "Char":
                    return "{}='{}' ".format(self.option, self.value)
                else:
                    return "{}={} ".format(self.option, self.value)
            return ""
        return self.option + " "
