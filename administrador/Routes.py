from flask import Flask, request
import Controllers.AdministradorController as controller

app = Flask(__name__)
administradorController = controller.AdministradorController()


# Exemplo body = {"topicos": ["/setor/lixeira/1", "/setor/lixeira/2"]}
@app.route('/lixeira', methods=['GET'])
def get_all_lixeiras():
    json = request.get_json()
    topicos: list = json['topicos']
    data = administradorController.get_all_lixeiras(topicos)
    return {
        "code": 200,
        "status": "OK",
        "lixeiras": data
    }


app.run()
