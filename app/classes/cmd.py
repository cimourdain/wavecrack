# coding: utf-8
import os
import subprocess
import shlex
from datetime import datetime

from app.helpers.files import FilesHelper


class Cmd(object):

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
        if not file_path:
            return default

        FilesHelper.file_exists(file_path=file_path, create=True)

        return open(file_path, 'w')

    def run(self):
        self.start_date = datetime.now()
        self.process = subprocess.Popen(shlex.split(self.cmd), stdout=self.stdout, stderr=self.stderr, shell=False)
        print ("executed commandline is %s" % self.cmd)
        self.pid = self.process.pid

        return self.pid

    def is_running(self):
        if self.process:
            print("poll: "+str(self.process.poll()))
            if self.process.poll() is None:
                print("cmd :: process ("+str(self.pid)+") is still running")
                return True
        print("process finished")
        return False

    def status_code(self):
        if not self.is_running():
            return self.process.returncode
        return None

    @staticmethod
    def get_process_pids(prgm_name):
        try:
            return subprocess.check_output(["pgrep", prgm_name], stderr=subprocess.STDOUT)
        except Exception as e:
            print("command '{}' return with error (code {}): {}".format(e.cmd, e.returncode, e.output))
            return []

    @staticmethod
    def kill(pid):
        print("kill process "+str(pid))
        os.system('kill -9 %s' % pid)

    @staticmethod
    def check_status(pid, expected_process_name=None):
        print("check process status for "+str(pid))
        out = subprocess.check_output(["ps", "-p", str(pid), "-o", "comm="])

        print("out "+str(out))
        if out and \
                (not expected_process_name
                 or (expected_process_name and out.lower().find(expected_process_name.lower()) != -1)
                ):
            print("process is running")
            return True
        print("process is not running")
        return False
