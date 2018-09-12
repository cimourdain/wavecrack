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

    def kill(self):
        if self.pid:
            os.system('kill -9 %s' % self.pid)
