import subprocess


class Cmd(object):

    @staticmethod
    def run_cmd(cmd_str):

        p = subprocess.Popen(cmd_str, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True)
        output, errors = p.communicate()

        if output:
            output = output.split("\n")

        return p.returncode, output, errors
