import os
from random import randint
from datetime import datetime

from app.tests import app, db
from app.helpers.files import FilesHelper


def crack_run_mock(self):
    """
    Method to run crack (=run hashcat command)

    This method uses the Cmd class to run commands in a linux env.

    :return: <bool> return true if command was launched successfully
    """
    from app.tests.test_submit_request import TestSubmitNewRequestForm
    output = TestSubmitNewRequestForm.output

    # set start date
    app.logger.debug("crack_run_mock :: run new crack (" + str(self.id) + ")")
    self.start_date = datetime.now()
    self.process_id = -1
    db.session.commit()

    # create files content
    app.logger.debug("crack_run_mock :: set output file content to "+str(output))
    FilesHelper.replace_file_content(self.output_file_path, output)

    # set crack as ended with success
    self.set_as_ended(end_status_mode="CMD_FINISHED")

    return True
