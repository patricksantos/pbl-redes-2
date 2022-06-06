import type { HttpContextContract } from '@ioc:Adonis/Core/HttpContext'
import { connect } from "mqtt"  // import connect from mqtt

let client = connect('mqtt://test.mosquitto.org') // create a client

interface EstacaoFacade {
    id: number,
    latLang: number,
    capacidadeAtual: number,
    capacidadeMaxima: number,
}

export default class EstacaosController {
    public async index(ctx: HttpContextContract) {
        client.subscribe('/estacao/01') // subscribe to topic
        client.on('estacoes', function (_, message) { // listen for messages
            let estacao: EstacaoFacade = JSON.parse(message.toString());
            client.end()
            return ctx.response.status(201).json(estacao)
        })
        return ctx.response.status(404).send({ error: 'Não foi possível conectar ao servidor' })
    }

    public async store(ctx: HttpContextContract) {
        const estacao: EstacaoFacade = ctx.request.only(['id', 'latLang', 'capacidadeAtual', 'capacidadeMaxima'])

        client.on('connect', function () { // When connected
            client.subscribe(`/estacao/${estacao.id}`, function (err) { // Subscribe to 'presence' channel
                if (!err) {
                    client.publish('lixeira', estacao.toString()) // Publish message to 'presence' channel
                    return ctx.response.status(201).json(estacao)
                }
            })
        })
        return ctx.response.status(404).send({ error: 'Não foi possível conectar ao servidor' })
    }
}
