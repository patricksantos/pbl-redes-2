import threading
from time import sleep
import uuid
import paho.mqtt.client as mqtt

class Caminhao():
    def __init__(self):
        self.lista_lixeiras = []

    def main(self):
        client = mqtt.Client()
        client.on_connect = self.on_connect
        client.on_message = self.on_message
        client.connect("localhost", 1883, 60)
        # thread2 = threading.Thread(target=self.publicar)
        # thread2.daemon = True
        # thread2.start()
        client.loop_forever()

    def on_connect(self, client, userdata, flags, rc):
        if rc == 0:
            client.subscribe("estacao 1")
            client.subscribe("estacao 2")
            client.subscribe("estacao 3")
            client.subscribe("estacao 4")
            client.subscribe("estacao 5")
        else:
            print("Não foi possivel se conectar ao broker. Codigo de erro: ",rc)

    def on_message(self, client, userdata, msg):
        print(msg.topic)
        print(str(msg.payload))

    def publicar(self, client):
        while True:
            payload = {
                "latitude": self.latitude,
                "longitude": self.longitude,
                "capacidade": self.capacidade,
                "quantidade_lixo": self.quantidade_lixo,
                "uuid": self.uuid
            }
            client.publish(self.estacao, payload, 0)
            sleep(1)    

if __name__ == "__main__":
    caminhao = Caminhao()
    caminhao.main()