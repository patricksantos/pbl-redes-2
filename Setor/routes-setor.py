
import json
from flask import Flask
import Setor.Setor as Setor
from decouple import config as env

app = Flask(__name__)
apiController = Setor.setor

@app.route('/lixeira/all/', methods=['GET'])
def getAllLixeiras():
    data = apiController.requisitar_lixeiras
    return json.dumps(data)

@app.route('/lixeira/<uuid>', methods=['PATCH'])
def updateLixeira(uuid):
    data = apiController.updateLixeira(uuid, 0)
    return json.dumps(data)

if __name__ == "__main__":
    app.run(host=env('HOST'), port=6000)
