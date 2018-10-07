# standard imports
import os
import json
import time
from datetime import datetime

# third party imports
from sqlalchemy.orm import relationship, reconstructor

# local imports
from app import db
from app.classes.crack import Crack as CrackClass
from app.classes.cmd import Cmd
from app.helpers.files import FilesHelper
from app.ref.close_modes import CRACKS_CLOSE_MODES

class Crack(db.Model):
    __tablename__ = 'cracks'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255), nullable=False, default="Unnamed crack")
    crack_request_id = db.Column(db.Integer, db.ForeignKey('cracks_requests.id'))
    cmd = db.Column(db.Text, nullable=True)
    process_id = db.Column(db.Integer, nullable=True)
    start_date = db.Column(db.DateTime, nullable=True)
    running = db.Column(db.Boolean, nullable=False, default=False)
    end_date = db.Column(db.DateTime, nullable=True)
    end_mode = db.Column(db.String(255), nullable=True)
    working_folder = db.Column(db.Text, nullable=False)
    nb_password_found = db.Column(db.Integer, nullable=False, default=0)

    request = relationship("CrackRequest", back_populates="cracks")

    @property
    def output_file_path(self):
        return os.path.join(self.working_folder, str(self.id), "output.txt")

    @property
    def status(self):
        if self.end_mode:
            return

    def build_crack_cmd(self, attack_mode, attack_file, crack_options=None):
        options = []
        if self.request.extra_options:
            options.extend(self.request.extra_options)
        print("Create new CrackClass instance with options " + str(options))
        if crack_options:
            options.extend(crack_options)
        print("Create new CrackClass instance with options "+str(options))

        new_crack_class = CrackClass(
            input_hashfile=self.request.hashes_path,
            hashes_type_code=self.request.hashes_type_code,
            attack_mode_code=attack_mode,
            attack_files=attack_file,
            options=options,
            output_path=self.output_file_path,
            session_id=self.request.session_id
        )
        self.cmd = new_crack_class.build_run_cmd()

    def run(self):
        print("======== crack :: run new crack ("+str(self.id)+")")
        self.start_date = datetime.now()
        db.session.commit()
        cmd = Cmd(
            cmd=self.cmd,
            out_file=os.path.join(self.working_folder,  str(self.id), "cmd_output.txt"),
            err_file=os.path.join(self.working_folder,  str(self.id), "cmd_err.txt"),
        )
        self.process_id = cmd.run()
        self.running = True
        db.session.commit()

        print("wait for process to finish")
        while cmd.is_running():
            print("process is running")
            time.sleep(30)

        self.set_as_ended(end_status_mode="CMD_FINISHED")

        return cmd

    def set_as_ended(self, end_status_mode="UNDEFINED"):
        self.running = False
        self.end_date = datetime.now()
        self.end_mode = end_status_mode
        self.nb_password_found = FilesHelper.nb_lines_in_file(self.output_file_path)
        print("nb passwords found :: " + str(self.nb_password_found))
        db.session.commit()

        FilesHelper.move_file_content(
            source_path=self.output_file_path,
            target_path=self.request.outfile_path
        )

        FilesHelper.remove_found_hashes_from_hashes_file(
            hashes_file=self.request.hashes_path,
            found_hashes_file=self.output_file_path
        )

    @reconstructor
    def check_status(self):
        if self.running:
            process_is_running = Cmd.check_status(self.process_id)
            if not process_is_running:
                self.set_as_ended()

    def force_close(self):
        print("Force close crack "+self.name)
        if self.process_id:
            Cmd.kill(self.process_id)
            self.set_as_ended(end_status_mode="MANUAL")
