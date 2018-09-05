# local imports
from server import app, celery


@celery.task
def launch_new_crack(hashes, hashes_type_code, output_file_path,
                     hashed_file_contains_usernames, attack_details,
                     duration):
    print("hashes "+str(hashes))
    print("hashes_type_code " + str(hashes_type_code))
    print("contains usernames : "+str(hashed_file_contains_usernames))
    print("outfile_path : "+str(output_file_path))
    print("attack_details: "+str(attack_details)+ "("+str(type(attack_details))+")")
    print("duration : "+str(duration))

