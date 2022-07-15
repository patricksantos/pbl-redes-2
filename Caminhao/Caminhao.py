import json
import threading
from time import sleep
import requests
from decouple import config as env


class Caminhao():

    def __init__(self):
        self.lista_lixeiras = []
        self.api_url = env('API_URL')

    def main(self):
        thread1 = threading.Thread(target=self.requisitar_trajeto)
        thread1.daemon = True
        thread1.start()
        thread2 = threading.Thread(target=self.realizar_trajeto)
        thread2.daemon = True
        thread2.start()

    def requisitar_trajeto(self):
        response = requests.get(f'{self.api_url}/lixeira/all')
        self.lista_lixeiras = response.json()

    def esvaziar_lixeira(self):
        if len(self.lista_lixeiras) > 0:
            lixeira = self.lista_lixeiras.pop(0)
            lixeira.update({"quantidade_lixo": 0.0})
            self.lista_lixeiras.append(lixeira)
            uuid = lixeira.get("uuid")
            requests.patch(f'{self.api_url}/lixeira/' + str(uuid), json={
                           "quantidade_lixo": lixeira.get("quantidade_lixo")})

    def realizar_trajeto(self):
        while True:
            self.esvaziar_lixeira()
            self.ordenar_lixeiras()
            sleep(5)


if __name__ == "__main__":
    caminhao = Caminhao()
    caminhao.main()
