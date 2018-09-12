# standard imports
import os
import uuid

# local imports
from server import app, celery, db
from app.classes.cmd import Cmd
from app.models.cracks.entity import Crack
from app.models.cracks.request import CrackRequest
from app.classes.crack import Crack
from app.helpers.files import FilesHelper

#
# def create_new_crack_request(user_id, crack_folder, duration):
#
#
#     db.session.add(new_crack_request)
#     db.session.commit()


def write_errors(folder, errors):
    FilesHelper.create_new_file(
        file_path=folder,
        file_name="errors.txt",
        content=errors
    )
    return True


#  the bind decorator argument > access to task id
@celery.task(bind=True)
def launch_new_crack(self, name, user_id, hashes, hashes_type_code, hashed_file_contains_usernames, duration, wordlist_files=None,
                     keywords=None, mask=None, rules=None, bruteforce=None):

    print("celery :: hashcat :: create new crack request")
    new_crack_request = CrackRequest()
    new_crack_request.name = name
    new_crack_request.celery_request_id = self.request.id
    new_crack_request.user_id = user_id
    new_crack_request.duration = duration

    new_crack_request.hashes_type_code = hashes_type_code
    new_crack_request.hashed_file_contains_usernames = hashed_file_contains_usernames
    new_crack_request.hashes = hashes
    if wordlist_files:
        new_crack_request.add_dictionary_paths(wordlist_files, ref=True)

    if keywords:
        new_crack_request.keywords = keywords
    if mask:
        new_crack_request.mask = mask
    if rules:
        new_crack_request.rules = rules
    new_crack_request.bruteforce = bruteforce

    db.session.add(new_crack_request)
    db.session.commit()

    new_crack_request.prepare_cracks()

    new_crack_request.run_cracks()
