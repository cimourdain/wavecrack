# local imports
from server import celery


@celery.task
def launch_new_crack(hashes, hashes_type_code, output_file_path,
                     hashed_file_contains_usernames, attack_details,
                     duration):

    if hashes_type_code == 999999:
        pass
