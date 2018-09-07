# standard imports
import os
import uuid

# local imports
from server import app, celery, db
from app.models.cracks.entity import Crack
from app.models.cracks.request import CrackRequest
from app.classes.crack import Crack
from app.helpers.files import FilesHelper



def create_new_crack_request(user_id, crack_folder, duration):
    new_crack_request = CrackRequest()
    new_crack_request.user_id = user_id
    new_crack_request.crack_folder = crack_folder
    new_crack_request.crack_duration = duration

    db.session.add(new_crack_request)
    db.session.commit()

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

    crack_folder = str(uuid.uuid4())
    print("crack folder full path : "+str(app.config["DIR_LOCATIONS"]["hashcat_outputs"])+str(crack_folder))
    crack_folder_full_path = os.path.join(app.config["DIR_LOCATIONS"]["hashcat_outputs"], crack_folder)
    os.mkdir(crack_folder_full_path)
    crack_output_file = os.path.join(crack_folder_full_path, "output.txt")

    # create new request
    create_new_crack_request(user_id, crack_folder, duration)

    # create hash file in crack request folder
    hash_file = FilesHelper.create_new_file(
        file_path=crack_folder_full_path,
        file_name="hashes.txt",
        content=hashes
    )

    # create keyword file if required
    keywords_file = None
    if keywords:
        keywords_file = FilesHelper.create_new_file(
            file_path=crack_folder_full_path,
            file_name="keywords.txt",
            content=keywords
        )

    # create mask file if required
    mask_file = None
    if mask:
        mask_file = FilesHelper.create_new_file(
            file_path=crack_folder_full_path,
            file_name="mask.hcmask",
            content=mask
        )

    if keywords:
        # launch attack with keywords strict
        crack_keyword_no_rules = Crack(
            input_hashfile=hash_file,
            attack_mode_code=0,
            hashes_type_code=hashes_type_code,
            attack_files=keywords_file,
            options=None,
            output_file=crack_output_file,
            log=True)
        code, output, errors = crack_keyword_no_rules.run()

        if errors:
            FilesHelper.create_new_file(
                file_path=crack_folder_full_path,
                file_name="cmd_errors.txt",
                content=errors
            )
        FilesHelper.create_new_file(
            file_path=crack_folder_full_path,
            file_name="cmd_output.txt",
            content="\n".join(output)
        )

        # launch attack with keywords + rules
        pass

    if wordlist_files:
        # launch attack for each wordlist file
        # launch attack for each wordlist file + rules
        pass

    if bruteforce:
        # launch bruteforce attack
        pass






