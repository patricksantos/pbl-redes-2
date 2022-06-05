import type { HttpContextContract } from '@ioc:Adonis/Core/HttpContext'
import { connect } from "mqtt"  // import connect from mqtt
let client = connect('mqtt://test.mosquitto.org') // create a client

let estacaos: Array<String> = []

export default class EstacaosController {
    public async index(ctx: HttpContextContract) {

        client.subscribe('/estacao/01') // subscribe to topic
        client.on('estacoes', function (topic, message) { // listen for messages
            let estacao = message.toString();
            console.log(estacao)
            estacaos.push(estacao)
            client.end()
        })

        return ctx.response.send(estacaos);
    }
}
