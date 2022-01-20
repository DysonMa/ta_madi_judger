from flask_restful import Api, Resource, reqparse
import os, sys

class RunCodeHandler(Resource):
    def get(self):
        os.system('type input.txt | test.py > output.txt')
        return {
            "status": 200
        }
    