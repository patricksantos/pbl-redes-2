import json
import uuid
import requests
import paho.mqtt.client as mqtt
from decouple import config as env


class Setor():
    def __init__(self):
        self.lista_lixeiras = []
        self.client = mqtt.Client()
        self.host = env('HOST')
        self.api_url = env('API_URL')
        self.uuid = str(uuid.uuid4())
        self.carlos_url = env('CARLOS_URL')
        self.patrick_url = env('PATRICK_URL')

    def main(self):
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message
        self.client.connect("mqtt.eclipseprojects.io", 1883, 60)
        self.client.loop_forever()

    def on_connect(self, client, userdata, flags, rc):
        if rc == 0:
            client.subscribe(f"{self.host}/setor")
        else:
            print("Não foi possivel se conectar ao broker. Codigo de erro: ", rc)

    def on_message(self, client, userdata, msg):
        mensagem = str(msg.payload.decode("utf-8"))
        dados_lixeira = json.loads(mensagem)
        self.cadastrar_lixeira(dados_lixeira)

    def cadastrar_lixeira(self, dados_lixeira):
        print(len(self.lista_lixeiras))
        if len(self.lista_lixeiras) > 0:
            for lixeira in self.lista_lixeiras:
                if lixeira.get("uuid") == dados_lixeira.get("uuid") and lixeira.get("quantidade_lixo") == 0.0:
                    lixeira.update(
                        {"quantidade_lixo": dados_lixeira.get("quantidade_lixo")})
                    uuid = lixeira.get("uuid")
                    requests.patch(f'{self.api_url}/lixeira/' + str(uuid),
                                   json={"quantidade_lixo": lixeira.get("quantidade_lixo")})
                    return
                elif lixeira.get("uuid") == dados_lixeira.get("uuid") and lixeira.get("quantidade_lixo") != 0.0:
                    return
            payload = {
                "quantidade_lixo": dados_lixeira.get("quantidade_lixo"),
                "uuid": dados_lixeira.get("uuid"),
                "latitude": dados_lixeira.get("latitude"),
                "longitude": dados_lixeira.get("longitude"),
                "setor": dados_lixeira.get("setor"),
                "capacidade": dados_lixeira.get("capacidade")
            }
            requests.post(f"{self.api_url}/lixeira", json=payload)
            self.lista_lixeiras.append(dados_lixeira)
            self.ordenar_lixeiras()
        else:
            payload = {
                "quantidade_lixo": dados_lixeira.get("quantidade_lixo"),
                "uuid": dados_lixeira.get("uuid"),
                "latitude": dados_lixeira.get("latitude"),
                "longitude": dados_lixeira.get("longitude"),
                "setor": dados_lixeira.get("setor"),
                "capacidade": dados_lixeira.get("capacidade")
            }
            requests.post(f"{self.api_url}/lixeira", json=payload)
            self.lista_lixeiras.append(dados_lixeira)

    def ordenar_lixeiras(self):
        if len(self.lista_lixeiras) > 1:
            self.lista_lixeiras = sorted(
                self.lista_lixeiras, key=lambda i: i['quantidade_lixo'], reverse=True)

    def publicar(self, topico):
        self.client.publish(topico, "esvaziar lixeira", 0)

    def updateLixeira(self, uuid, quantidade_lixo):
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
                self.publicar("lixeira/"+str(uuid))
                return json.dumps(updatedLixeira)

        return json.dumps({"message": "Não há lixeira com o ID informado, cadastradas."})

    def requisitar_lixeiras(self):
        lixeiras_outro_setor = []
        if env('HOST')+":6000" == self.carlos_url.split('/')[2]:
            response = requests.get(f'{self.patrick_url}/lixeiras')
            if response.status_code == 308:
                return []
            else:
                lixeiras_outro_setor = response.json()
        else:
            response = requests.get(f'{self.carlos_url}/lixeiras')
            if response.status_code == 308:
                return []
            else:
                lixeiras_outro_setor = response.json()        
        retorno = self.lista_lixeiras + lixeiras_outro_setor
        return retorno
    
    def getLixeiras(self):
        return self.lista_lixeiras


if __name__ == "__main__":
    setor = Setor()
    setor.main()
