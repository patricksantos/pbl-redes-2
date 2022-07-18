from flask import Flask, request
import Controllers.Api as api
from decouple import config as env

app = Flask(__name__)
apiController = api.ApiController()

# Exemplo body = {"count": 10}
host = env('HOST')


@app.route('/lixeira/all/<count>/<host>', methods=['GET'])
def getAllLixeiras(count, host):
    data = apiController.getAllLixeiras(int(count), str(host))
    return data


@app.route('/lixeira/<uuid>', methods=['GET'])
def findById(uuid):
    data = apiController.findById(uuid)
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

    data = apiController.createdLixeira(
        uuid, latitude, longitude, capacidade, quantidade_lixo, estacao)
    return data


# Exemplo params = 1 /lixeira/1 = { "latitude": 1, "longitude": 1, "capacidade": 1, "quantidade_lixo": 1, "estacao": "1" }
@app.route('/lixeira/<uuid>', methods=['PATCH'])
def updateLixeira(uuid):
    body = request.get_json()
    quantidade_lixo = body['quantidade_lixo']
    data = apiController.updateLixeira(uuid, quantidade_lixo)
    return data


if __name__ == "__main__":
    app.run(host=host, port=5000)
