import json

from flask import jsonify, make_response


class AdministradorController():
    def __init__(self):
        super().__init__()
        self.lixeirasTopicos: list = []

    def getAllLixeiras(self, count):
        i = 0
        lista_lixeiras = []
        if len(self.lixeirasTopicos) == 0:
            return make_response(jsonify({"message": "Não há lixeiras cadastradas."}), 400)
        for lixeira in self.lixeirasTopicos:
            if(i < count):
                lista_lixeiras.append(lixeira)
                i += 1
        if len(lista_lixeiras) > 1:
            lista_lixeiras = sorted(
                lista_lixeiras, key=lambda i: i['quantidade_lixo'], reverse=True)
        return make_response({"lista das lixeiras": lista_lixeiras}, 200)

    def createdLixeira(self, uuid, latitude, longitude, capacidade, quantidade_lixo, estacao):
        dados_lixeira = {
            "uuid": uuid,
            "latitude": latitude,
            "longitude": longitude,
            "capacidade": capacidade,
            "quantidade_lixo": quantidade_lixo,
            "estacao": estacao
        }
        for lixeira in self.lixeirasTopicos:
            if lixeira.get("uuid") == dados_lixeira.get("uuid"):
                return make_response(jsonify({"message": "lixeira já está cadastrada."}), 400)
        self.lixeirasTopicos.append(dados_lixeira)
        return make_response({"lixeira": self.lixeirasTopicos}, 200)

    def findById(self, uuid):
        for lixeira in self.lixeirasTopicos:
            if(lixeira.get("uuid") == str(uuid)):
                return make_response({"lixeira": lixeira}, 200)
        return make_response(jsonify({"message": "Não há lixeira com o ID informado, cadastradas."}), 400)

    def updateLixeira(self, uuid, quantidade_lixo):
        i = 0
        if len(self.lixeirasTopicos) == 0:
            return make_response(jsonify({"message": "Não há lixeiras cadastradas."}), 400)
        for lixeira in self.lixeirasTopicos:
            if(lixeira.get("uuid") == str(uuid)):
                lixeira = self.lixeirasTopicos.pop(i)
                lixeira.update({"quantidade_lixo": quantidade_lixo})
                self.lixeirasTopicos.append(lixeira)
                return make_response({"lixeira": self.lixeirasTopicos}, 200)
            i += 1
        return make_response(jsonify({"message": "Não há lixeira com o ID informado, cadastradas."}), 400)
