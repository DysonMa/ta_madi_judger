import os

root_dir = os.path.abspath(os.path.join(__file__, "../../"))

class Utilities():
    @staticmethod
    def create_folder_if_not_exists():
        storage_path = os.path.join(root_dir, "data")
        if not os.path.exists(storage_path):
            os.mkdir(storage_path)

    @staticmethod
    def get_abs_path(path, fileName):
        return os.path.abspath(os.path.join(path, fileName))

