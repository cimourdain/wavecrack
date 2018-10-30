# standard imports
import os
import time
from datetime import datetime

# third party imports
from sqlalchemy.orm import relationship, reconstructor

# local imports
from server import app
from app import db
from app.classes.crackCmdBuilder import CrackCmdBuilder
from app.classes.cmd import Cmd
from app.helpers.files import FilesHelper
from app.ref.attack_modes import ATTACK_MODES


class Crack(db.Model):
    """
    Class defining a crack.
    A crack is created (and belongs to a request)

    """
    __tablename__ = 'cracks'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255), nullable=False, default="Unnamed crack")
    crack_request_id = db.Column(db.Integer, db.ForeignKey('cracks_requests.id'))
    _attack_mode_code = db.Column(db.Integer, nullable=False)
    _attack_file = db.Column(db.Text, nullable=True)
    options = db.Column(db.Text, nullable=True)
    cmd = db.Column(db.Text, nullable=True)
    process_id = db.Column(db.Integer, nullable=True)
    start_date = db.Column(db.DateTime, nullable=True)
    end_date = db.Column(db.DateTime, nullable=True)
    end_mode = db.Column(db.String(255), nullable=True)
    _nb_password_found = db.Column(db.Integer, nullable=False, default=0)

    request = relationship("CrackRequest", back_populates="cracks")

    def __init__(self, name, attack_mode, attack_file):
        """
        On init a crack request must be created with a name
        :param name: <str>
        """
        self.name = name
        self.attack_mode = attack_mode if attack_mode else 0
        self.attack_file = attack_file if attack_file else None

    # PROPERTIES
    @property
    def crack_folder(self):
        """
        Crack folder
            * is a subfolder in the parent request working folder
            * is named with the crack id

        :return: <str> crack folder path
        """
        return os.path.join(self.request.request_working_folder, "crack_"+str(self.id))

    @property
    def output_file_path(self):
        """
        Path of the crack output file.
            * define the output file path in the crack folder
            * create it if does not exists (file must exits on hashcat command launch)

        :return: <str> output file path
        """
        output_path = os.path.join(self.crack_folder, "output.txt")
        FilesHelper.file_exists(file_path=output_path, create=True)
        return output_path

    @property
    def running(self):
        """
        Check if crack is currently running
        :return: <bool<
        """
        if self.start_date and not self.end_date:
            return True
        return False

    @property
    def is_finished(self):
        """
        Check if crack is finished (= an end date is set)
        :return: <bool>
        """
        if self.end_date:
            return True
        return False

    @property
    def nb_password_found(self):
        return FilesHelper.nb_lines_in_file(self.output_file_path)

    @property
    def attack_mode(self):
        for am in ATTACK_MODES:
            if self._attack_mode_code == am["code"]:
                return am

        return "Undefined"

    @property
    def attack_file(self):
        return os.path.split(self._attack_file)[-1]

    @property
    def has_rules(self):
        return self.request.has_rules

    @property
    def rules(self):
        return self.request.rules

    @attack_mode.setter
    def attack_mode(self, attack_mode):
        for am in ATTACK_MODES:
            if attack_mode == am["code"] or attack_mode == am["description"]:
                self._attack_mode_code = am["code"]

    @attack_file.setter
    def attack_file(self, attack_file):
        app.logger.debug("Check if attack file exists : "+str(attack_file))
        if attack_file and FilesHelper.file_exists(attack_file):
            self._attack_file = attack_file
        elif attack_file and not FilesHelper.file_exists(attack_file):
            app.logger.warn("Invalid attack file on crack "+str(attack_file))

    # RECONSTUCTOR (called on every object load)
    @reconstructor
    def check_status(self):
        """
        If crack is running, then check that hashcat command is still running
        :return:
        """
        if self.running:
            process_is_running = Cmd.check_status(self.process_id)
            if not process_is_running:
                self.set_as_ended()

    # OTHER METHODS
    def build_crack_cmd(self, crack_options=None):
        """
        From crack and request, build and set the hashcat command to launch.

        Note: This method use the crackCmdBuilder object to build the command.

        :param crack_options: <dict>
        :return:
        """

        # build options from concatenation of argument options + parent request options
        options = []
        if self.request.extra_options:
            options.extend(self.request.extra_options)

        if crack_options:
            options.extend(crack_options)
        app.logger.debug("Create new CrackClass instance with options "+str(options))

        # init a CrackCmdBuilder instance
        new_crack_class = CrackCmdBuilder(
            source_crack=self,
            attack_mode_code=self.attack_mode,
            attack_files=self.attack_file,
            options=options
        )

        # build and set hashcat command
        self.cmd = new_crack_class.build_run_cmd()

    def run(self):
        """
        Method to run crack (=run hashcat command)

        This method uses the Cmd class to run commands in a linux env.

        :return: <bool> return true if command was launched successfully
        """
        # exit if current crack hashcat cmd is not defined
        if not self.cmd:
            return False

        # set start date
        app.logger.debug("Crack Entity :: run :: run new crack ("+str(self.id)+")")
        self.start_date = datetime.now()
        db.session.commit()

        # launch linux command
        cmd = Cmd(
            cmd=self.cmd,
            out_file=os.path.join(self.crack_folder, "cmd_output.txt"),
            err_file=os.path.join(self.crack_folder, "cmd_err.txt"),
        )
        self.process_id = cmd.run()
        db.session.commit()

        # wait command to finish
        app.logger.debug("Crack Entity :: run :: wait for process to finish")
        while cmd.is_running():
            app.logger.debug("Crack Entity :: run :: process is running")
            time.sleep(30)

        # set crack as ended with success
        self.set_as_ended(end_status_mode="CMD_FINISHED")

        return True

    def set_as_ended(self, end_status_mode="UNDEFINED"):
        """
        Set crack as finished.
            - if crack is currently running:
                * move cracked hashes from crack output file to request outputfile
                * remove cracked hashes from the request hashes (=> no other attempt to crack them again)
            - set end_date and end_mode

        :param end_status_mode: <str>
        :return:
        """
        # if crack is currently running, move output content to request output
        if self.running:
            app.logger.debug("move cracked hashes from {} to request main output {}".format(
                self.output_file_path,
                self.request.outfile_path
            ))
            FilesHelper.move_file_content(
                source_path=self.output_file_path,
                target_path=self.request.outfile_path
            )

            app.logger.debug("remove cracked hashes from {} to {}".format(
                self.request.hashes_path,
                self.output_file_path
            ))
            FilesHelper.remove_found_hashes_from_hashes_file(
                hashes_file=self.request.hashes_path,
                found_hashes_file=self.output_file_path
            )

        self.end_date = datetime.now()
        self.end_mode = end_status_mode
        db.session.commit()

    def force_close(self):
        """
        method to force close a crack:
            * kill hashcat command
            * call crack soft close command

        :return:
        """
        app.logger.debug("Force close crack "+self.name)
        if self.process_id:
            Cmd.kill(self.process_id)
            self.set_as_ended(end_status_mode="MANUAL")

    def get_crack_file(self, filename):
        app.logger.debug("Crack :: Check if "+str(filename)+" is "+str(self.attack_file))
        if filename == self.attack_file:
            return self._attack_file

        app.logger.debug("Crack :: Check if " + str(filename) + " is in " + str(self.crack_folder))
        for f in FilesHelper.get_available_files(self.crack_folder):
            if f == filename:
                return os.path.join(self.crack_folder, f)

        return self.request.get_file(filename)
