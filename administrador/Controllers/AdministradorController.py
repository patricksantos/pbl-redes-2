from Mqtt import Mqtt

class AdministradorController(Mqtt):
    def __init__(self):
        super().__init__()

    def iniciar(self):
        return 'Oii'