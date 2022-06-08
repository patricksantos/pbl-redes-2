from flask import Flask
import Controllers.AdministradorController as controller 

app = Flask(__name__)
AdministradorController = controller.AdministradorController()

@app.route('/')
def base_url():
    return AdministradorController.iniciar()

app.run()
