from Mqtt import Mqtt


class AdministradorController(Mqtt):
    def __init__(self):
        super().__init__()

    def get_all_lixeiras(self, topicos: list):
        lixeirasTopicos: list = []
        for topico in topicos:
            lixera = self.client.subscribe(topico, 1)
            lixeirasTopicos.append(lixera)
        # Falta ordenar as lixeiras
        return lixeirasTopicos
