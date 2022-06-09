from ast import While
import json
import threading
from time import sleep
import uuid
import paho.mqtt.client as mqtt

class Caminhao():

    def __init__(self):
        self.lista_lixeiras = []
        self.client = mqtt.Client()

    def main(self):
       self.client.on_connect = self.on_connect
       self.client.on_message = self.on_message
       self.client.connect("localhost", 1883, 60)
       thread2 = threading.Thread(target=self.realizar_trajeto)
       thread2.daemon = True
       thread2.start()
       self.client.loop_forever()

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
        mensagem = str(msg.payload.decode("utf-8"))
        dados_lixeira = json.loads(mensagem)        
        self.cadastrar_lixeira(dados_lixeira)

    def publicar(self, topico):
        self.client.publish(topico, "esvaziar lixeira", 0)
        
    def cadastrar_lixeira(self, dados_lixeira):
        if len(self.lista_lixeiras) > 0:
            for lixeira in self.lista_lixeiras:
                if lixeira.get("uuid") == dados_lixeira.get("uuid") and lixeira.get("quantidade_lixo") == 0.0:
                    lixeira.update({"quantidade_lixo":dados_lixeira.get("quantidade_lixo")})                    
                    return
                elif lixeira.get("uuid") == dados_lixeira.get("uuid") and lixeira.get("quantidade_lixo") != 0.0:
                    return
            self.lista_lixeiras.append(dados_lixeira)
            self.ordenar_lixeiras()
        else:
            self.lista_lixeiras.append(dados_lixeira)

    def esvaziar_lixeira(self):
        if len(self.lista_lixeiras) > 0:
            lixeira = self.lista_lixeiras.pop(0)
            lixeira.update({"quantidade_lixo": 0.0})
            self.lista_lixeiras.append(lixeira)
            self.publicar("lixeira/"+str(lixeira.get("uuid")))

    def ordenar_lixeiras(self):
        if len(self.lista_lixeiras) > 1:
            self.lista_lixeiras = sorted(self.lista_lixeiras, key = lambda i: i['quantidade_lixo'],reverse=True)

    def realizar_trajeto(self):
        while True:
            self.esvaziar_lixeira()
            self.ordenar_lixeiras()
            sleep(5)

if __name__ == "__main__":
    caminhao = Caminhao()
    caminhao.main()