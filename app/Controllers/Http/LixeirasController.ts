import type { HttpContextContract } from '@ioc:Adonis/Core/HttpContext'
import { connect } from "mqtt"  // import connect from mqtt

let client = connect('mqtt://test.mosquitto.org') // create a client

interface LixeiraFacade {
    id: number,
    latLang: number,
    capacidadeAtual: number,
    capacidadeMaxima: number,
    estacao: string,
}

let lixeiras: Array<String> = []

export default class LixeirasController {

    public async index(ctx: HttpContextContract) {
        client.subscribe('/caminhao/01') // subscribe to topic
        client.on('message', function (_, message) { // listen for messages
            let lixeira: LixeiraFacade = JSON.parse(message.toString());
            client.end()
            return ctx.response.status(201).json(lixeira)
        })
        return ctx.response.status(200).send(lixeiras)
    }

    public async store(ctx: HttpContextContract) {
        const lixeira: LixeiraFacade = ctx.request.only(['id', 'latLang', 'capacidadeAtual', 'capacidadeMaxima', 'estacao'])

        client.on('connect', function () { // When connected
            client.subscribe(`/lixeira/${lixeira.id}`, function (err) { // Subscribe to 'presence' channel
                if (!err) {
                    client.publish('lixeira', lixeira.toString()) // Publish message to 'presence' channel
                    return ctx.response.status(201).send(lixeira)
                }
            })
        })
        return ctx.response.status(404).send({ error: 'Não foi possível conectar ao servidor' })
    }

}

