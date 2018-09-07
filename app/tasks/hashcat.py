# standard imports
import os
import uuid

# local imports
from server import app, celery, db


@celery.task
def launch_new_crack(hashes, hashes_type_code, hashed_file_contains_usernames, duration, wordlist_files=None,
                     keywords=None, mask=None, rules=None, bruteforce=None):

    # create session id for cracks
    crack_id = uuid.uuid4()





