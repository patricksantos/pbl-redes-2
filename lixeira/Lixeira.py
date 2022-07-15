import json
import random
import threading
from time import sleep
import uuid
import paho.mqtt.client as mqtt
from decouple import config as env


class Lixeira():
    def __init__(self):
        self.capacidade = 0.0
        self.quantidade_lixo = 0.0
        self.latitude = 0
        self.longitude = 0
        self.uuid = str(uuid.uuid4())
        self.setor = f"{env('HOST')}/setor"
        self.client = mqtt.Client()

    def main(self):
        self.latitude = random.randint(1, 101)
        self.longitude = random.randint(1, 101)
        if self.latitude == self.latitude:
            while self.longitude == self.latitude:
                self.longitude = random.randint(1, 101)
        self.capacidade = random.randint(1, 101)
        self.quantidade_lixo = random.randint(1, (self.capacidade+1))
        thread = threading.Thread(target=self.gerar_lixo)
        thread.daemon = True
        thread.start()
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message
        self.client.connect("mqtt.eclipseprojects.io", 1883, 60)
        thread2 = threading.Thread(target=self.publicar)
        thread2.daemon = True
        thread2.start()
        self.client.loop_forever()

    def gerar_lixo(self):
        while True:
            if self.quantidade_lixo == 0:
                self.quantidade_lixo = random.randint(1, (self.capacidade+1))
            sleep(5)

    def on_connect(self, client, userdata, flags, rc):
        if rc == 0:
            client.subscribe("lixeira/"+str(self.uuid))
        else:
            print("Não foi possivel se conectar ao broker. Codigo de erro: ", rc)

    def on_message(self, client, userdata, msg):
        if str(msg.payload.decode("utf-8")) == "esvaziar lixeira":
            self.quantidade_lixo = 0.0
        else:
            print("Comando desconhecido: "+str(msg.payload.decode("utf-8")))

    def publicar(self):
        while True:
            payload = {
                "latitude": self.latitude,
                "longitude": self.longitude,
                "capacidade": self.capacidade,
                "quantidade_lixo": self.quantidade_lixo,
                "uuid": self.uuid,
                "setor": self.setor
            }
            self.client.publish(self.setor, str(json.dumps(payload)), 0)
            sleep(5)


if __name__ == "__main__":
    lixeira = Lixeira()
    lixeira.main()
