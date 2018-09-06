import os


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
                try:
                    open(file_path, 'a').close()
                except Exception as _:
                    return False
            else:
                return False

        return True

    @staticmethod
    def dir_exists(dir_path):
        return os.path.isdir(dir_path)
