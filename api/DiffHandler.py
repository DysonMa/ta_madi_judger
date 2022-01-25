from flask import request, send_file, jsonify
from flask_restful import Api, Resource
import os, sys
import difflib

FILE_KEYS = ["ANSWER", "OUTPUT"]
root_dir = os.path.abspath(os.path.join(__file__, "../../"))

class DiffHandler(Resource):
    def get(self):

        # TODO: renew data in `data` folder(delete first)
        storage_path = os.path.join(root_dir, "data")
        if not os.path.exists(storage_path):
            os.mkdir(storage_path)

        # compare the difference between the output files and the answer files
        diff_filenames = []
        diff_contents = []
        storage_path = os.path.join(root_dir, "data")
        for i in range(1,4):
            answer_file = open(os.path.abspath(os.path.join(storage_path, f"ANSWER_{i}.txt")), "r")
            output_file = open(os.path.abspath(os.path.join(storage_path, f"OUTPUT_{i}.txt")), "r")
            diff = difflib.ndiff(answer_file.readlines(), output_file.readlines())
            content = ""
            diff_file = os.path.abspath(os.path.join(storage_path, f"diff_{i}.txt"))
            with open(diff_file, "w") as f:
                for line in diff:
                    if not line.startswith("? "):
                        f.write(line)  
                        content += line 
            diff_filenames.append({
                "name":f"diff_{i}.txt"
            })
            diff_contents.append(content)
        
        return jsonify({
            "filename": diff_filenames,
            "content": diff_contents
        })

