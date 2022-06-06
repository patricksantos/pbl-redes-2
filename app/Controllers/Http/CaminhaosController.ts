import type { HttpContextContract } from '@ioc:Adonis/Core/HttpContext'
import { connect } from "mqtt"  // import connect from mqtt

let client = connect('mqtt://test.mosquitto.org') // create a client

interface CaminhaoFacade {
    id: number,
    latLang: number,
    capacidadeAtual: number,
    capacidadeMaxima: number,
}

export default class CaminhaosController {
    public async index(ctx: HttpContextContract) {
        client.subscribe('/caminhao') // subscribe to topic
        client.on('message', function (_, message) { // listen for messages
            let caminhao: CaminhaoFacade = JSON.parse(message.toString());
            client.end()
            return ctx.response.status(201).json(caminhao)
        })
        return ctx.response.status(404).send({ error: 'Não foi possível conectar ao servidor' })
    }

    public async store(ctx: HttpContextContract) {
        const caminhao: CaminhaoFacade = ctx.request.only(['id', 'latLang', 'capacidadeAtual', 'capacidadeMaxima'])

        client.on('connect', function () { // When connected
            client.subscribe(`/caminhao/${caminhao.id}`, function (err) { // Subscribe to 'presence' channel
                if (!err) {
                    client.publish('caminhao', caminhao.toString()) // Publish message to 'presence' channel
                    return ctx.response.status(201).send(caminhao)
                }
            })
        })
        return ctx.response.status(404).send({ error: 'Não foi possível conectar ao servidor' })
    }
}
