import type { HttpContextContract } from '@ioc:Adonis/Core/HttpContext'
import { connect } from "mqtt"  // import connect from mqtt
let client = connect('mqtt://test.mosquitto.org') // create a client

let caminhao: Array<String> = []

export default class CaminhaosController {
    public async index(ctx: HttpContextContract) {
        
        client.subscribe('/caminhao') // subscribe to topic
        client.on('message', function (topic, message) { // listen for messages
            console.log(message.toString())
            caminhao.push(message.toString())
            client.end()
        })

        return ctx.response.send(caminhao);
      }
}
