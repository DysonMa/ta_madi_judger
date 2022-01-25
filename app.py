from flask import Flask, send_from_directory
from flask_restful import Api, Resource, reqparse
from flask_cors import CORS

from api.RunCodeHandler import RunCodeHandler
from api.DiffHandler import DiffHandler


# https://towardsdatascience.com/build-deploy-a-react-flask-app-47a89a5d17d9

app = Flask(__name__, static_url_path='', static_folder='frontend/build')
CORS(app)
api = Api(app)

@app.route("/")
def serve():
    return send_from_directory(app.static_folder, "index.html")


api.add_resource(RunCodeHandler, "/run")
api.add_resource(DiffHandler, "/diff")
    

if __name__=="__main__":
    app.run(debug=True)