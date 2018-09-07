# coding: utf-8
import subprocess
import shlex

class Cmd(object):

    @staticmethod
    def run_cmd(cmd):
        p = subprocess.Popen(shlex.split(cmd), stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=False)
        print ("executed commandline is %s" % cmd)
        output, errors = p.communicate()

        if output:
            output = output.split("\n")
        print("return code :"+str(p.returncode))
        print("output: "+str(output))
        print("errors: "+str(errors))
        return p.returncode, output, errors
