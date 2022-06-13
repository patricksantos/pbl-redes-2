
from re import I
from flask import Flask, request
import Controllers.Administrador as controller

app = Flask(__name__)
administradorController = controller.AdministradorController()

# Exemplo body = {"count": 10}


@app.route('/lixeira/all', methods=['GET'])
def getAllLixeiras():
    json = request.get_json()
    count: int = json['count']
    data = administradorController.getAllLixeiras(count)
    return data


@app.route('/lixeira/<uuid>', methods=['GET'])
def findById(uuid):
    data = administradorController.findById(uuid)
    return data


# Exemplo body = { "latitude": 1, "longitude": 1, "capacidade": 1, "quantidade_lixo": 1, "uuid": "1", "estacao": "1" }
@app.route('/lixeira', methods=['POST'])
def createdLixeira():
    body = request.get_json()
    uuid = body['uuid']
    latitude = body['latitude']
    longitude = body['longitude']
    capacidade = body['capacidade']
    quantidade_lixo = body['quantidade_lixo']
    estacao = body['estacao']

    data = administradorController.createdLixeira(
        uuid, latitude, longitude, capacidade, quantidade_lixo, estacao)
    return data


# Exemplo params = 1 /lixeira/1 = { "latitude": 1, "longitude": 1, "capacidade": 1, "quantidade_lixo": 1, "estacao": "1" }
@app.route('/lixeira/<uuid>', methods=['PATCH'])
def updateLixeira(uuid):
    body = request.get_json()
    quantidade_lixo = body['quantidade_lixo']
    data = administradorController.updateLixeira(uuid, quantidade_lixo)
    return data


app.run()
