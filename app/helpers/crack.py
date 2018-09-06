from datetime import datetime
import string
import random


class CrackHelper(object):

    @staticmethod
    def get_output_file_name():
        # Determination of current crack output file
        output_file_name_prefix = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        output_file_name_suffix = ''.join(
            random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(6)
        )
        return output_file_name_prefix + output_file_name_suffix

    @staticmethod
    def crack(options):
        pass