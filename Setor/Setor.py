import json
import threading
from time import sleep
import uuid
import requests
import paho.mqtt.client as mqtt
from decouple import config as env


class Setor:
    def __init__(self):
        self.lista_lixeiras = []
        self.client = mqtt.Client()
        self.host = env('HOST')
        self.api_url = env('API_URL')
        self.uuid = str(uuid.uuid4())

    def main(self):
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message
        self.client.connect("mqtt.eclipseprojects.io", 1883, 60)
        thread2 = threading.Thread(target=self.realizar_trajeto)
        thread2.daemon = True
        thread2.start()
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


if __name__ == "__main__":
    setor = Setor()
    setor.main()
