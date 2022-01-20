from flask import Flask, send_from_directory
from flask_restful import Api, Resource, reqparse
from api.RunCodeHandler import RunCodeHandler

# https://towardsdatascience.com/build-deploy-a-react-flask-app-47a89a5d17d9

app = Flask(__name__, static_url_path='', static_folder='frontend/build')
api = Api(app)

@app.route("/")
def serve():
    return send_from_directory(app.static_folder, "index.html")

# if __name__=="__main__":
api.add_resource(RunCodeHandler, "/run")
    # app.run()