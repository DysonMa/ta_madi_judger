from flask import request, jsonify
from flask_restful import Resource
import os
from api.util import Utilities
from typing import Dict, List

class RunCodeHandler(Resource):
    def __init__(self) -> None:
        super().__init__()
        self.root_dir = os.path.abspath(os.path.join(__file__, "../../"))
        self.storage_path = Utilities.get_abs_path(path=self.root_dir, fileName="data")
        self.input_num = 0
        self.groups = ["CODE", "INPUT", "ANSWER"]
        self.files = {}

    def __save_uploading_files(self) -> None:
        for key, file in self.files.items():
            group = key.split("_")[0] if  "_" in key else key
            if group in self.groups:
                file_extention = "py" if group=="CODE" else "txt"
                file_path = Utilities.get_abs_path(path=self.storage_path, fileName=f"{file.name}.{file_extention}")
                file.save(file_path)
            if group=="INPUT":
                self.input_num += 1

    # read input files and execute `CODE.py`` to generate output files
    def __run_code(self) -> None:
        for group, file in self.files.items():
            if group.startswith("INPUT"):
                inputFile = Utilities.get_abs_path(path=self.storage_path, fileName=f"{file.name}.txt")
                number = file.name.split("_")[1]
                codeFile = Utilities.get_abs_path(path=self.storage_path, fileName="CODE.py")
                outputFile = Utilities.get_abs_path(path=self.storage_path, fileName=f"OUTPUT_{number}.txt")
                os.system(f'type {inputFile} | python {codeFile} > {outputFile}')

    # get all output files info 
    def __get_output_files_info(self) -> Dict:
        output_filenames, output_contents  = [], []
        for i in range(1, self.input_num+1):
            filepath = Utilities.get_abs_path(path=self.storage_path, fileName=f"OUTPUT_{i}.txt")
            output_filenames.append({
                "name": f"OUTPUT_{i}.txt"
            })
            content = ""
            with open(filepath) as f:
                content += f.read()
                output_contents.append(content)

        return {
            "filename": output_filenames,
            "content": output_contents
        }

    def get(self):
        return "Only POST method is allowed to generate output files"

    def post(self):
        self.files = request.files
        if len(self.files)==0: 
            return "No file selected"  # TODO: Error status code
        
        # read CODE, INPUT*N, OUTPUT*N files
        Utilities.create_folder_if_not_exists()
        self.__save_uploading_files()

        # read input files and execute `CODE.py`` to generate output files
        self.__run_code()
        
        # get output files info including fileName and content
        return jsonify(self.__get_output_files_info())
