import json
from this import d
from flask import Flask
import Controllers.Setor as setor
from decouple import config as env

app = Flask(__name__)
apiController = setor.Setor()

host = env('HOST')


@app.route('/lixeira/all/', methods=['GET'])
def getAllLixeiras():
    data = apiController.requisitar_lixeiras()
    print(type(data))
    return json.dumps(data)


@app.route('/lixeiras', methods=['GET'])
def getLixeiras():
    data = apiController.getLixeiras()
    return json.dumps(data)


@app.route('/lixeira/<uuid>', methods=['PATCH'])
def updateLixeira(uuid):
    data = apiController.updateLixeira(uuid, 0)
    return json.dumps(data)


if __name__ == "__main__":
    app.run(host=host, port=6000)
