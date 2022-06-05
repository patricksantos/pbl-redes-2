import type { HttpContextContract } from '@ioc:Adonis/Core/HttpContext'
import { connect } from "mqtt"  // import connect from mqtt
let client = connect('mqtt://test.mosquitto.org') // create a client

let lixeiras: Array<String> = []

export default class LixeirasController {

    public async index(ctx: HttpContextContract) {

        client.subscribe('/caminhao/01') // subscribe to topic
        client.on('message', function (topic, message) { // listen for messages
            let lixeira = message.toString();
            console.log(lixeira)
            lixeiras.push(lixeira)
            client.end()
        })

        return ctx.response.send(lixeiras);
    }

}

// client.on('connect', function () { // When connected
//     client.subscribe('presence', function (err) { // Subscribe to 'presence' channel
//         if (!err) { 
//             client.publish('presence', 'Hello mqtt') // Publish message to 'presence' channel
//         }
//     })
// })