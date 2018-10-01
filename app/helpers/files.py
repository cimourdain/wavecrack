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
    def copy_file(source, target):
        copyfile(source, target)

    @staticmethod
    def remove_found_hashes_from_hashes_file(hashes_file, found_hashes_file):
        tmp_folder = app.config["DIR_LOCATIONS"]["tmp"]
        # duplicate hashes file
        tmp_dir_path = os.path.join(tmp_folder, str(uuid.uuid4()))
        os.mkdir(tmp_dir_path)
        tmp_file_path = os.path.join(tmp_dir_path, "output_copy.txt")
        FilesHelper.copy_file(hashes_file, tmp_file_path)

        current_hashes = []
        with open(tmp_file_path, "r") as hashes_file_content:
            for h in hashes_file_content:
                current_hashes.append(h.strip())
        hashes_file_content.close()

        found_hashes = []
        with open(found_hashes_file, "r") as found_hashes_file_content:
            for h in found_hashes_file_content:
                found_hashes.append(h.split(":")[0].strip())

        found_hashes_file_content.close()

        with open(hashes_file, "w") as final_hash:
            for ch in current_hashes:
                if ch not in found_hashes:
                    final_hash.write(ch + "\n")

        final_hash.close()

        rmtree(tmp_dir_path)

    @staticmethod
    def nb_lines_in_file(file_path):
        return sum(1 for line in open(file_path))

    @staticmethod
    def remove_ext_from_filename(filename):
        return os.path.splitext(filename)[0]

    @staticmethod
    def split_path(path, return_file_ext=True):
        if return_file_ext:
            return os.path.split(path)
        else:
            path_dir, path_file = os.path.split(path)
            return path_dir, FilesHelper.remove_ext_from_filename(path_file)
