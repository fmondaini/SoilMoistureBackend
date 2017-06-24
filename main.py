import os
import json
import requests
import paho.mqtt.client as mqtt


def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))
    client.subscribe("esp")


def on_message(client, userdata, msg):
    print(msg.topic + " " + str(msg.payload))
    if msg.topic == "esp":
        data = json.loads(msg.payload.decode('utf-8'))

        event, key = 'moisture_level', os.getenv('IFTTT_MAKER_KEY')
        url = "https://maker.ifttt.com/trigger/%s/with/key/%s" % (event, key)

        requests.post(url, data=data)


def get_config():
    return {
        'user': os.getenv('CLOUDMQTT_USER'),
        'password': os.getenv('CLOUDMQTT_PASSWORD'),
        'host': os.getenv('CLOUDMQTT_HOST'),
        'port': os.getenv('CLOUDMQTT_PORT')
    }


if __name__ == '__main__':
    config = get_config()
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message

    client.username_pw_set(config['user'], config['password'])
    client.connect(config['host'], int(config['port']), 60)

    client.loop_forever()
