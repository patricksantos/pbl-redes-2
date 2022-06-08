import random
import threading
from time import sleep
from Mqtt import Mqtt

class Lixeira(Mqtt):
    def __init__(self):
        super().__init__()
        self.capacidade = 0.0
        self.quantidade_lixo = 0.0
        self.latitude = 0
        self.longitude = 0

    def main(self):
        self.latitude = random.randint(1,101)
        self.longitude = random.randint(1,101)
        if self.latitude == self.latitude:
            while self.longitude == self.latitude:
                self.longitude = random.randint(1,101)
        self.capacidade = random.randint(1,101)
        self.quantidade_lixo = random.randint(1, (self.capacidade+1))
        thread = threading.Thread(target= self.gerar_lixo)
        thread.daemon = True
        thread.start()
        self.publish_message('lixeira/capacidade', self.capacidade)
        
    def gerar_lixo(self):
        while True:
            if self.quantidade_lixo == 0:
                self.quantidade_lixo = random.randint(1, (self.capacidade+1))
            sleep(10)

if __name__ == "__main__":
    lixeira = Lixeira()
    lixeira.main()