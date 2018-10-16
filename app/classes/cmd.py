# coding: utf-8
import os
import subprocess
import shlex
from datetime import datetime

from server import app
from app.helpers.files import FilesHelper


class Cmd(object):
    """
    Class used to interact with the linux system (run linux commands)
    """
    def __init__(self, cmd, out_file=None, err_file=None):
        self.cmd = cmd
        self.pid = None
        self.return_code = None
        self.output = None
        self.errors = None
        self.start_date = None
        self.end_date = None
        self.process = None

        self.stdout = self.set_std_param(out_file, subprocess.PIPE)
        self.stderr = self.set_std_param(err_file, subprocess.STDOUT)

    def set_std_param(self, file_path, default):
        """
        Method used to define out and error path

        :param file_path: <str> path
        :param default: subprocess.PIPE or subprocess.STDOUT
        :return: <file>
        """
        if not file_path:
            return default

        FilesHelper.file_exists(file_path=file_path, create=True)

        return open(file_path, 'w')

    def run(self):
        """
        Run command
            * set start_date
            * launch linux command

        :return: <int> command process id
        """
        self.start_date = datetime.now()
        self.process = subprocess.Popen(shlex.split(self.cmd), stdout=self.stdout, stderr=self.stderr, shell=False)
        app.logger.info("Cmd :: run :: executed commandline is %s" % self.cmd)
        self.pid = self.process.pid

        return self.pid

    def is_running(self):
        """
        Check if command is running

        :return: <bool> is command currently running on system?
        """
        if self.process:
            app.logger.debug("Cmd :: is_running :: poll: "+str(self.process.poll()))
            if self.process.poll() is None:
                app.logger.info("Cmd :: is_running :: process ("+str(self.pid)+") is still running")
                return True

        app.logger.info("Cmd :: is_running :: process not running")
        return False

    def status_code(self):
        """
        get current process status code
        :return: <str>
        """
        if not self.is_running():
            return self.process.returncode
        return None

    @staticmethod
    def get_process_pids(prgm_name):
        """
        Get all process id from a program

        This method is used on the admin server page to get all running hashcat instances.

        :param prgm_name: <str>
        :return: <list> list of program ids
        """
        try:
            return subprocess.check_output(["pgrep", prgm_name], stderr=subprocess.STDOUT)
        except Exception as e:
            app.logger.warn("Cmd :: command '{}' return with error (code {}): {}".format(e.cmd, e.returncode, e.output))
            return []

    @staticmethod
    def kill(pid):
        """
        Kill process.
        :param pid: <int> process_id
        :return:
        """
        app.logger.info("Cmd :: kill :: kill process "+str(pid))
        os.system('kill -9 %s' % pid)

    @staticmethod
    def check_status(pid, expected_process_name=None):
        """
        Check process status (check if process is still running)

        used on crack entity reconstructor.

        :param pid: <int> process_id
        :param expected_process_name: <str>
        :return:
        """
        try:
            out = subprocess.check_output(["ps", "-p", str(pid), "-o", "comm="])
        except Exception as _:
            return False

        app.logger.debug("Cmd :: check_status :: out "+str(out))
        if out and \
                (not expected_process_name
                 or (expected_process_name and out.lower().find(expected_process_name.lower()) != -1)
                ):
            app.logger.debug("Cmd :: check_status :: process is running")
            return True
        app.logger.debug("Cmd :: check_status :: process is not running")
        return False
