from flask import request, send_file, jsonify
from flask_restful import Api, Resource
from werkzeug.utils import secure_filename
import os, sys
import difflib
from api.util import Utilities
from typing import Dict

class DiffHandler(Resource):
    def __init__(self) -> None:
        super().__init__()
        self.root_dir = os.path.abspath(os.path.join(__file__, "../../"))
        self.storage_path = Utilities.get_abs_path(path=self.root_dir, fileName="staging_area")
        self.diff_num = 0

    def __get_diff_files_count(self) -> int:
        answer_file_count = 0
        output_file_count = 0
        for file in os.listdir(self.storage_path):
            if file.startswith("ANSWER"):
                answer_file_count += 1
            if file.startswith("OUTPUT"):
                output_file_count += 1
        return min(answer_file_count, output_file_count)

    # compare the difference between the output files and the answer files
    def __run_diff(self) -> Dict:
        self.diff_num = self.__get_diff_files_count()
        if self.diff_num == 0:
            raise Exception("No diff files found")

        diff_filenames, diff_contents = [], []
        for i in range(1, self.diff_num+1):
            answer_file_path = Utilities.get_abs_path(path=self.storage_path, fileName=f"ANSWER_{i}.txt")
            output_file_path = Utilities.get_abs_path(path=self.storage_path, fileName=f"OUTPUT_{i}.txt")
            diff_file_path = Utilities.get_abs_path(path=self.storage_path, fileName=f"diff_{i}.txt")

            answer_file = open(answer_file_path, "r")
            output_file = open(output_file_path, "r")
            diff = difflib.ndiff(answer_file.readlines(), output_file.readlines())

            # write diff to file
            content = ""
            with open(diff_file_path, "w") as f:
                for line in diff:
                    if not line.startswith("? "):  # "?" means line not present in either input sequence
                        f.write(line)  
                        content += line
            
            diff_filenames.append({
                "name": f"diff_{i}.txt" # needs to match the format of File Object from javascript
            })
            diff_contents.append(content)

        return {
            "filename": diff_filenames,
            "content": diff_contents
        }

    def get(self):
        try:
            return jsonify(self.__run_diff())
        except Exception as e:
            return e

