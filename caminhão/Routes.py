from flask import Flask, request
import Controllers.CaminhaoController as controller

app = Flask(__name__)
caminhaoController = controller.CaminhaoController()


# Exemplo body = {"topicos": ["/setor/lixeira/1", "/setor/lixeira/2"]}
@app.route('/lixeira', methods=['GET'])
def get_all_lixeiras():
    json = request.get_json()
    topicos: list = json['topicos']
    data = caminhaoController.get_all_lixeiras(topicos)
    return {
        "code": 200,
        "status": "OK",
        "lixeiras": data
    }


# Exemplo body = {"topico": "/setor/lixeira/1", "id": 1}
@app.route('/empty/lixeira', methods=['POST'])
def empty_lixeira():
    json = request.get_json()
    topico: str = json['topico_lixeira']
    id_lixeira: int = json['id']
    caminhaoController.empty_lixeira(topico, id_lixeira)
    return {
        "code": 201,
        "status": "OK",
    }


app.run()
