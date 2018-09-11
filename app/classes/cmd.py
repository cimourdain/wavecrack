# coding: utf-8
import os
import subprocess
import shlex
from datetime import datetime


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

        self.out_file = out_file if out_file else subprocess.PIPE
        print("outfile: "+self.out_file)
        self.err_file = err_file if err_file else subprocess.STDOUT
        print("errfile: "+self.err_file)

    def run(self):
        self.start_date = datetime.now()
        self.process = subprocess.Popen(shlex.split(self.cmd), stdout=open(self.out_file, 'w'), stderr=open(self.err_file, 'w'), shell=False)
        print ("executed commandline is %s" % self.cmd)
        self.pid = self.process.pid

        return self.pid

    def is_running(self):
        if self.process:
            if not self.process.poll():
                return True
        return False

    def status_code(self):
        if not self.is_running():
            return self.process.returncode
        return None

    def kill(self):
        if self.pid:
            os.system('kill -9 %s' % self.pid)
