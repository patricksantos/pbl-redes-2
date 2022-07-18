import json
from urllib import response
from decouple import config as env
import requests

class ApiController():
    def __init__(self):
        super().__init__()
        self.lista_lixeiras: list = []
        self.carlos_url = env('CARLOS_URL')
        self.patrick_url = env('PATRICK_URL')

    def ordenar_lixeiras(self):
        if len(self.lista_lixeiras) > 1:
            self.lista_lixeiras = sorted(
                self.lista_lixeiras, key=lambda i: i['quantidade_lixo'], reverse=True)

    def getAllLixeiras(self, count, host):
        if len(self.lista_lixeiras) == 0:
            return json.dumps({"message": "Não há lixeiras cadastradas."})
        if host == self.carlos_url.split(':')[0]:
            response = requests.get(f'{self.carlos_url}/lixeira/all/')
            self.lista_lixeiras = response.json()
        else: 
            response = requests.get(f'{self.patrick_url}/lixeira/all/')
            self.lista_lixeiras = response.json()
        i = 0
        getAllLixeiras = []
        self.ordenar_lixeiras()
        for lixeira in self.lista_lixeiras:
            if(i < count):
                getAllLixeiras.append(json.loads(lixeira))
                i += 1
        return json.dumps(getAllLixeiras)

    def createdLixeira(self, uuid, latitude, longitude, capacidade, quantidade_lixo, setor):
        lixeira = {
            "uuid": uuid,
            "latitude": latitude,
            "longitude": longitude,
            "capacidade": capacidade,
            "quantidade_lixo": quantidade_lixo,
            "setor": setor
        }
        for lixeira in self.lista_lixeiras:
            lixeira = json.loads(lixeira)
            if lixeira.get("uuid") == uuid:
                return 
        self.lista_lixeiras.append(json.dumps(lixeira))
        return json.dumps(lixeira)

    def findById(self, uuid):
        for lixeira in self.lista_lixeiras:
            data = json.loads(lixeira)
            if(str(data["uuid"]) == str(uuid)):
                return json.loads(lixeira)

        return json.dumps({"message": "Não há lixeira com o ID informado, cadastradas."})

    def updateLixeira(self, uuid, quantidade_lixo):
        print(uuid)
        if len(self.lista_lixeiras) == 0:
            return json.dumps({"message": "Não há lixeiras cadastradas."})
        for lixeira in self.lista_lixeiras:
            data = json.loads(lixeira)
            if(str(data["uuid"]) == str(uuid)):
                updatedLixeira = {
                    "uuid": uuid,
                    "latitude": data["latitude"],
                    "longitude": data["longitude"],
                    "capacidade": data["capacidade"],
                    "quantidade_lixo": quantidade_lixo,
                    "estacao": data["estacao"]
                }
                if quantidade_lixo > data["capacidade"]:
                    return json.dumps({"message": "Não se pode adicionar mais lixo que a capacidade da lixeira."})
                self.lista_lixeiras.remove(lixeira)
                self.lista_lixeiras.append(json.dumps(updatedLixeira))
                return json.dumps(updatedLixeira)

        return json.dumps({"message": "Não há lixeira com o ID informado, cadastradas."})
