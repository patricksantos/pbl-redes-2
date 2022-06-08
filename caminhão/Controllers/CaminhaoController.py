from Mqtt import Mqtt


class CaminhaoController(Mqtt):
    def __init__(self):
        super().__init__()

    def get_all_lixeiras(self, topicos: list):
        lixeirasTopicos: list = []
        for topico in topicos:
            lixera = self.client.subscribe(topico, 1)
            lixeirasTopicos.append(lixera)
        # Falta ordenar as lixeiras
        return lixeirasTopicos

    def empty_lixeira(self, topico: str, id: int):
        payload = {
            "id": id,
            "capacidade_atual": 0,
        }
        self.client.publish(topico, payload, 1)
