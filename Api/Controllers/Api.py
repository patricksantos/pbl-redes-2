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

    def ordenar_lixeiras(self, lista):
        if len(lista) > 1:
            lista = sorted(
                lista, key=lambda i: i['quantidade_lixo'], reverse=True)
            return lista

    def getLixeiras(self, count):
        if len(self.lista_lixeiras) == 0:
            return json.dumps({"message": "Não há lixeiras cadastradas."})
        i = 0
        getAllLixeiras = []
        temp_list = []
        for lixeira in self.lista_lixeiras:
            temp_list.append(json.loads(lixeira))
        temp_list = self.ordenar_lixeiras(temp_list)
        for lixeira in temp_list:
            if(i < count):
                getAllLixeiras.append(lixeira)
                i += 1
        return json.dumps(getAllLixeiras)

    def getAllLixeiras(self, count, host):
        if len(self.lista_lixeiras) == 0:
            return json.dumps({"message": "Não há lixeiras cadastradas."})
        retorno = []
        if host == "http://"+self.carlos_url.split(':')[0]:
            response = requests.get(f'{self.carlos_url}/lixeira/all/')
            retorno = response.json()
        else: 
            response = requests.get(f'{self.patrick_url}/lixeira/all/')
            retorno = response.json()
        if len(retorno) == 0:
            return json.dumps([])
        i = 0
        getAllLixeiras = []
        retorno = self.ordenar_lixeiras(retorno)
        for lixeira in retorno:
            if(i < count):
                getAllLixeiras.append(lixeira)
                i += 1
        return json.dumps(getAllLixeiras)

    def createdLixeira(self, uuid, latitude, longitude, capacidade, quantidade_lixo, setor):
        lixeira_cadastro = {
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
                return json.dumps({"message":"Lixeira já está cadastrada"})
        self.lista_lixeiras.append(json.dumps(lixeira_cadastro))
        return json.dumps(lixeira_cadastro)

    def findById(self, uuid):
        for lixeira in self.lista_lixeiras:
            data = json.loads(lixeira)
            if(str(data["uuid"]) == str(uuid)):
                return json.loads(lixeira)

        return json.dumps({"message": "Não há lixeira com o ID informado, cadastradas."})

    def updateLixeira(self, uuid, quantidade_lixo):
        if len(self.lista_lixeiras) == 0:
            return json.dumps({"message": "Não há lixeiras cadastradas."})
        for lixeira in self.lista_lixeiras:
            data = json.loads(lixeira)
            if(str(data["uuid"]) == str(uuid)):                
                if quantidade_lixo > data["capacidade"]:
                    return json.dumps({"message": "Não se pode adicionar mais lixo que a capacidade da lixeira."})
                updatedLixeira = {
                    "uuid": uuid,
                    "latitude": data["latitude"],
                    "longitude": data["longitude"],
                    "capacidade": data["capacidade"],
                    "quantidade_lixo": quantidade_lixo,
                    "setor": data["setor"]
                }
                self.lista_lixeiras.remove(lixeira)
                self.lista_lixeiras.append(json.dumps(updatedLixeira))
                return json.dumps(updatedLixeira)

        return json.dumps({"message": "Não há lixeira com o ID informado, cadastradas."})
