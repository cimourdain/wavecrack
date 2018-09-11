from shutil import copyfile, rmtree
import os
import uuid

from server import app

class FilesHelper(object):
    @staticmethod
    def parse_dict_folders(folder):
        for dirpath, dirs, files in os.walk(folder):
            current_folder = os.path.basename(os.path.normpath(dirpath))
            if files:
                yield dirpath[len(folder):], current_folder, files

    @staticmethod
    def get_available_files(folder):
        available_files = []
        for dirpath, current_folder, files in FilesHelper.parse_dict_folders(folder):
            for f in files:
                file_relative_path = os.path.join(dirpath, f)
                available_files.append(file_relative_path)

        return available_files

    @staticmethod
    def file_exists(file_path, folder=None, create=True):
        if folder:
            file_path = os.path.join(folder, file_path)

        if not os.path.isfile(file_path):
            if create:
                file_folders = os.path.dirname(os.path.abspath(file_path))
                try:
                    # create folders if required
                    if not os.path.exists(file_folders):
                        os.makedirs(file_folders)
                    # create file
                    open(file_path, 'a').close()
                except Exception as _:
                    return False
            else:
                return False

        return True

    @staticmethod
    def dir_exists(dir_path):
        return os.path.isdir(dir_path)

    @staticmethod
    def create_new_file(file_path, file_name, content):
        new_file_name = os.path.join(file_path, file_name)

        f = open(new_file_name, "w+")
        f.write(content)
        f.close()
        os.chmod(new_file_name, 0o777)
        return new_file_name

    @staticmethod
    def get_file_content(file_path):
        if FilesHelper.file_exists(file_path, create=False):
            for line in open(file_path):
                yield line

    @staticmethod
    def move_file_content(source_path, target_path):
        source = open(source_path, "r+")
        target = open(target_path, "a+")

        target.write(source.read())
        source.close()
        target.close()

    @staticmethod
    def remove_found_hashes_from_hashes_file(hashes_file, found_hashes_file):
        print("remove_found_hashes_from_hashes_file")
        # duplicate hashes file
        tmp_dir_path = os.path.join(app.config["DIR_LOCATIONS"]["tmp"], str(uuid.uuid4()))
        os.mkdir(tmp_dir_path)
        tmp_file_path = os.path.join(tmp_dir_path, "output_copy.txt")
        copyfile(hashes_file, tmp_file_path)

        with open(hashes_file, "w") as final_hash:
            with open(tmp_file_path, "r") as current_hashes:
                with open(found_hashes_file, "r") as found_hash:
                    for hash_to_find in current_hashes:
                        hash_to_find = hash_to_find.strip()
                        print("check if "+str(hash_to_find)+" was found")
                        found = False
                        for hash_found in found_hash:
                            print("check if "+str(hash_to_find)+" == "+str(hash_found.split(":")[0]))
                            if hash_found.split(":")[0] == hash_to_find:
                                print("yes!")
                                found = True
                        if not found:
                            final_hash.write(hash_to_find+"\n")

        final_hash.close()
        current_hashes.close()
        found_hash.close()

        # rmtree(os.path.dirname(tmp_dir_path))
