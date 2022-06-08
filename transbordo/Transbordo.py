import random
import threading
from time import sleep
from Mqtt import Mqtt


class Transbordo(Mqtt):
    def __init__(self):
        super().__init__()
        self.capacidade = 0.0
        self.quantidade_lixo = 0.0
        self.latitude = 0
        self.longitude = 0

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
        payload = {
            "latitude": self.latitude,
            "longitude": self.longitude,
            "capacidade": self.capacidade,
            "quantidade_lixo": self.quantidade_lixo
        }
        self.client.publish('transbordo', payload)


if __name__ == "__main__":
    transbordo = Transbordo()
    transbordo.main()
