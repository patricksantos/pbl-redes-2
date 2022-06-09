import json


class AdministradorController():
    def __init__(self):
        super().__init__()
        self.lixeirasTopicos: list = []

    def getAllLixeiras(self, count):
        i = 0
        getAllLixeiras = []
        # Falta ordenar as lixeiras
        for lixeira in self.lixeirasTopicos:
            if(i < count):
                getAllLixeiras.append(json.loads(lixeira))
                i += 1
        return json.dumps(getAllLixeiras)

    def createdLixeira(self, uuid, latitude, longitude, capacidade, quantidade_lixo, estacao):
        lixeira = {
            "uuid": uuid,
            "latitude": latitude,
            "longitude": longitude,
            "capacidade": capacidade,
            "quantidade_lixo": quantidade_lixo,
            "estacao": estacao
        }
        self.lixeirasTopicos.append(json.dumps(lixeira))
        return json.dumps(lixeira)

    def findById(self, uuid):
        for lixeira in self.lixeirasTopicos:
            data = json.loads(lixeira)
            if(str(data["uuid"]) == str(uuid)):
                return json.loads(lixeira)

        return json.dumps("Não encontrado")

    def updateLixeira(self, uuid, latitude, longitude, capacidade, quantidade_lixo, estacao):
        print(uuid)
        updatedLixeira = {
            "uuid": uuid,
            "latitude": latitude,
            "longitude": longitude,
            "capacidade": capacidade,
            "quantidade_lixo": quantidade_lixo,
            "estacao": estacao
        }
        for lixeira in self.lixeirasTopicos:
            data = json.loads(lixeira)
            if(str(data["uuid"]) == str(uuid)):
                self.lixeirasTopicos.remove(lixeira)
                self.lixeirasTopicos.append(json.dumps(updatedLixeira))
                return json.dumps(updatedLixeira)

        return json.dumps("Não encontrado")
