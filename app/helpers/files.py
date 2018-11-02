from shutil import copyfile, rmtree
import os
import uuid


class FilesHelper(object):
    @staticmethod
    def parse_dict_folders(folder):
        """
        Generator to find all files in a folder

        :param folder: <str> folder absolute path
        :return:
        """
        for dirpath, dirs, files in os.walk(folder):
            current_folder = os.path.basename(os.path.normpath(dirpath))
            if files:
                yield dirpath[len(folder):], current_folder, files

    @staticmethod
    def get_available_files(folder):
        """
        method to list relative path of files in input folder
        :param folder: <str> folder absolute path
        :return:
        """
        available_files = []
        for dirpath, current_folder, files in FilesHelper.parse_dict_folders(folder):
            for f in files:
                file_relative_path = os.path.join(dirpath, f)
                available_files.append(file_relative_path)

        return available_files

    @staticmethod
    def file_exists(file_path, folder=None, create=True):
        """
        Method to check if a file exists

        :param file_path: <str> file path
        :param folder: <str> folder (if file_path is relative)
        :param create: <bool> create file if does not exists
        :return:
        """
        # if folder arg is defined, concatenate it with file path
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
        """
        Check if directory exists

        :param dir_path: <str> dir absolute path
        :return: <bool>
        """
        return os.path.isdir(dir_path)

    @staticmethod
    def replace_file_content(file_path, new_content):
        f = open(file_path, "w+")
        f.write(new_content)
        f.close()
        os.chmod(file_path, 0o777)
        return file_path

    @staticmethod
    def create_new_file(file_path, file_name, content):
        """
        Create new file with content

        :param file_path: <str> file to create folder absolute path
        :param file_name: <str> file name
        :param content: <str> file content
        :return: <str> new file absolute path
        """
        new_file_name = os.path.join(file_path, file_name)

        return FilesHelper.replace_file_content(new_file_name, content)

    @staticmethod
    def get_file_content(file_path):
        """
        generator to return each line of a file content

        :param file_path: <str> file absolute path
        :return:
        """
        if FilesHelper.file_exists(file_path, create=False):
            for line in open(file_path):
                yield line

    @staticmethod
    def move_file_content(source_path, target_path):
        """
        move file content from a file to the end of another

        :param source_path: <str> file absolute path
        :param target_path: <str> file absolute path
        :return:
        """
        source = open(source_path, "r+")
        target = open(target_path, "a+")

        target.write(source.read())
        source.close()
        target.close()

    @staticmethod
    def copy_file(source, target):
        """
        Method to duplicate files

        :param source: <str> file absolute path
        :param target: <str> file absolute path
        :return:
        """
        copyfile(source, target)

    @staticmethod
    def remove_found_hashes_from_hashes_file(hashes_file, found_hashes_file, tmp_folder):
        """
        Method used to remove found hashes in the original hash file (to prevent searching for them on the next crack)

        :param hashes_file: <str> file absolute path
        :param found_hashes_file: <str> file absolute path
        :return:
        """
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
        """
        Method to count nb lines in file

        :param file_path: <str> File absolute path
        :return: <int> nb lines in file
        """
        if not FilesHelper.file_exists(file_path=file_path, create=False):
            return 0

        return sum(1 for line in open(file_path))

    @staticmethod
    def remove_ext_from_filename(filename):
        """
        remove extension from filename
        :param filename: <str> filename
        :return: <str> filename without extension
        """
        return os.path.splitext(filename)[0]

    @staticmethod
    def split_path(path, return_file_ext=True):
        """
        Split path string directories and filename

        :param path: <str> path
        :param return_file_ext: <bool> remove file extension from returned file name
        :return: path<str>, filename<str>
        """
        if return_file_ext:
            return os.path.split(path)
        else:
            path_dir, path_file = os.path.split(path)
            return path_dir, FilesHelper.remove_ext_from_filename(path_file)

    @staticmethod
    def path_to_list(path_str):
        """
        split path to a list of directories

        (not used)

        :param path_str: <str> absolute path
        :return:<list>
        """
        path = os.path.normpath(path_str)
        return path.split(os.sep)

    @staticmethod
    def count_folders_in_dir(path_str):
        """
        method used to count nb of directories in path
        (created to check nb of dir in request folder > determine if archived)

        :param path_str: <str>
        :return: <int> (nb of dir in path)
        """
        return sum(os.path.isdir(os.path.join(path_str, i)) for i in os.listdir(path_str))

    @staticmethod
    def delete_directory(dir_path):
        """
        method to delete a directory and its content

        :param dir_path: <str> dir absolute path
        :return:
        """
        rmtree(dir_path, ignore_errors=True)
        return True
