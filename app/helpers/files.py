import os


class FilesHelper(object):
    @staticmethod
    def parse_dict_folders(folder):
        for dirpath, dirs, files in os.walk(folder):
            current_folder = os.path.basename(os.path.normpath(dirpath))
            yield current_folder, files

    @staticmethod
    def get_available_files(folder):
        available_files = []
        for current_folder, files in FilesHelper.parse_dict_folders(folder):
            available_files.extend(files)

        return available_files
