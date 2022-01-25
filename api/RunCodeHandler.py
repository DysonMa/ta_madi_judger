from flask import request, jsonify
from flask_restful import Resource
import os

FILE_KEYS = ["CODE", "INPUT", "ANSWER"]
root_dir = os.path.abspath(os.path.join(__file__, "../../"))

class RunCodeHandler(Resource):
    def get(self):
        return "Only POST method is allowed to generate output files"

    def post(self):
        print(request.files)
        if len(request.files)==0: 
            return "No file selected"  # TODO: Error status code
        
        # read CODE, INPUT*N, OUTPUT*N files

        # TODO: renew data in `data` folder(delete first)
        storage_path = os.path.join(root_dir, "data")
        if not os.path.exists(storage_path):
            os.mkdir(storage_path)

        input_num = 0
        for fileKey, file in request.files.items():
            type = fileKey.split("_")[0] if  "_" in fileKey else fileKey
            if type in FILE_KEYS:
                fileName = f"{fileKey}.py" if fileKey=="CODE" else f"{fileKey}.txt"
                file.save(os.path.join(storage_path, fileName))
                
            if type=="INPUT":
                input_num += 1

        # read input files and execute `CODE.py`` to generate output files
        for fileKey, file in request.files.items():
            if fileKey.startswith("INPUT"):
                inputFile = os.path.join(storage_path, f"{file.name}.txt")
                number = file.name.split("_")[1]
                codeFile = os.path.join(storage_path, "CODE.py")
                outputFile = os.path.join(storage_path, f"OUTPUT_{number}.txt")
                os.system(f'type {inputFile} | python {codeFile} > {outputFile}')
        
        # generate output files
        output_filenames = []
        output_contents = []
        for i in range(1, input_num+1):
            filename = f"OUTPUT_{i}"
            filepath = os.path.join(storage_path, f"{filename}.txt")
            output_filenames.append({
                "name": filename
            })
            content = ""
            with open(filepath) as f:
                content += f.read()
                output_contents.append(content)

        return jsonify({
            "filename": output_filenames,
            "content": output_contents
        })
