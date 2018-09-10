# standard imports
import os
import uuid

# local imports
from server import app, celery, db
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


@celery.task
def launch_new_crack(user_id, hashes, hashes_type_code, hashed_file_contains_usernames, duration, wordlist_files=None,
                     keywords=None, mask=None, rules=None, bruteforce=None):

    print("celery :: hashcat :: create new crack request")
    new_crack_request = CrackRequest()
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

    print(str(new_crack_request.__dict__))


    # # create new request
    # create_new_crack_request(user_id, crack_folder, duration)
    #
    # # create hash file in crack request folder
    # hash_file = FilesHelper.create_new_file(
    #     file_path=crack_folder_full_path,
    #     file_name="hashes.txt",
    #     content=hashes
    # )
    #
    # # create keyword file if required
    # keywords_file = None
    # if keywords:
    #     keywords_file = FilesHelper.create_new_file(
    #         file_path=crack_folder_full_path,
    #         file_name="keywords.txt",
    #         content=keywords
    #     )
    #
    # # create mask file if required
    # mask_file = None
    # if mask:
    #     mask_file = FilesHelper.create_new_file(
    #         file_path=crack_folder_full_path,
    #         file_name="mask.hcmask",
    #         content=mask
    #     )

    # if keywords:
    #     # launch attack with keywords strict
    #     crack_keyword_no_rules = Crack(
    #         input_hashfile=hash_file,
    #         attack_mode_code=0,
    #         hashes_type_code=hashes_type_code,
    #         attack_files=keywords_file,
    #         options=None,
    #         output_file=crack_output_file,
    #         log=True)
    #     code, output, errors = crack_keyword_no_rules.run()
    #
    #     if errors:
    #         FilesHelper.create_new_file(
    #             file_path=crack_folder_full_path,
    #             file_name="cmd_errors.txt",
    #             content=errors
    #         )
    #     FilesHelper.create_new_file(
    #         file_path=crack_folder_full_path,
    #         file_name="cmd_output.txt",
    #         content="\n".join(output)
    #     )
    #
    #     # launch attack with keywords + rules
    #     pass
    #
    # if wordlist_files:
    #     # launch attack for each wordlist file
    #     # launch attack for each wordlist file + rules
    #     pass
    #
    # if bruteforce:
    #     # launch bruteforce attack
    #     pass
    #





