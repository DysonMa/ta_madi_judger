import os, shutil

root_dir = os.path.abspath(os.path.join(__file__, "../../"))

class Utilities():
    @staticmethod
    def renew_storage_folder() -> None:
        storage_path = os.path.join(root_dir, "staging_area")
        # clear existed files in `staging_area` folder, BE CAREFUL!
        if os.path.exists(storage_path):
            shutil.rmtree(storage_path) 
        os.mkdir(storage_path)

    @staticmethod
    def get_abs_path(path, fileName) -> str:
        return os.path.abspath(os.path.join(path, fileName))

