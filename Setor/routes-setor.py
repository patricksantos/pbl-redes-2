
from re import I
from flask import Flask, request
import Setor.Setor as Setor

app = Flask(__name__)
apiController = Setor.setor

@app.route('/lixeira/all/', methods=['GET'])
def getAllLixeiras():
    data = apiController.lista_lixeiras
    return data

@app.route('/lixeira/<uuid>', methods=['PATCH'])
def updateLixeira(uuid):
    data = apiController.updateLixeira(uuid, 0)
    return data

app.run()
