import threading
from time import sleep
import requests
from decouple import config as env

class Caminhao():

    def __init__(self):
        self.lista_lixeiras = []
        self.api_url = env('API_URL')
        self.host= env('HOST')

    def main(self):
        self.realizar_trajeto()

    def requisitar_trajeto(self):
        response = requests.get(f'{self.api_url}/lixeira/all/5/{self.host}')
        self.lista_lixeiras = response.json()

    def esvaziar_lixeira(self):
        if len(self.lista_lixeiras) > 0:
            lixeira = self.lista_lixeiras.pop(0)
            lixeira.update({"quantidade_lixo": 0.0})
            uuid = lixeira.get("uuid")
            requests.patch(f'{self.api_url}/lixeira/' + str(uuid), json={
                           "quantidade_lixo": lixeira.get("quantidade_lixo")})

    def ordenar_lixeiras(self):
        if len(self.lista_lixeiras) > 1:
            self.lista_lixeiras = sorted(
                self.lista_lixeiras, key=lambda i: i['quantidade_lixo'], reverse=True)

    def realizar_trajeto(self):
        while True:
            if(len(self.lista_lixeiras) == 0):
                self.requisitar_trajeto()
            self.esvaziar_lixeira()
            self.ordenar_lixeiras()
            sleep(5)


if __name__ == "__main__":
    caminhao = Caminhao()
    caminhao.main()
