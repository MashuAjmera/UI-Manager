# python3.6

import random, time, json
from paho.mqtt import client as mqtt_client


broker = 'localhost'
port = 1883
topic = "uimanager/influxdb/#"
# generate client ID with pub prefix randomly
client_id = f'python-mqtt-{random.randint(0, 100)}'
# username = 'emqx'
# password = 'public'


def connect_mqtt() -> mqtt_client:
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker!")
        else:
            print("Failed to connect, return code %d\n", rc)

    client = mqtt_client.Client(client_id)
    # client.username_pw_set(username, password)
    client.on_connect = on_connect
    client.connect(broker, port)
    return client


def subscribe(client: mqtt_client):
    def on_message(client, userdata, msg):
        time.sleep(3)
        req=json.loads(msg.payload.decode())
        print(f"Received `{req}` from `{msg.topic}` topic")
        if req['bucket']['task']=='list':
            res=[
                {
                    "id": "606c9140d36f326e",
                    "orgID": "1e99b0e2686cf663",
                    "type": 0,
                    "name": "Bucket1",
                    "description": "",
                    "retentionPeriod": 345600000000000,
                    "createdAt": "2021-06-17T08:05:39.989819941Z",
                    "updatedAt": "2021-06-17T08:05:39.98982006Z"
                },
                {
                    "id": "70942f1469bc2f95",
                    "orgID": "1e99b0e2686cf663",
                    "type": 1,
                    "name": "_monitoring",
                    "description": "System bucket for monitoring logs",
                    "retentionPeriod": 604800000000000,
                    "createdAt": "2021-06-17T08:05:39.98350539Z",
                    "updatedAt": "2021-06-17T08:05:39.983505479Z"
                },
                {
                    "id": "420ba7a69b618485",
                    "orgID": "1e99b0e2686cf663",
                    "type": 1,
                    "name": "_tasks",
                    "description": "System bucket for task logs",
                    "retentionPeriod": 259200000000000,
                    "createdAt": "2021-06-17T08:05:39.978392507Z",
                    "updatedAt": "2021-06-17T08:05:39.978392587Z"
                }
            ]
            client.publish(f"response/{msg.topic}",json.dumps(res))
        elif req['bucket']['task']=='create':
            res="successfully created"
            client.publish(f"response/{msg.topic}",json.dumps(res))
        elif req['bucket']['task']=='delete':
            res="successfully deleted"
            client.publish(f"response/{msg.topic}",json.dumps(res))
        elif req['bucket']['task']=='update':
            res="successfully updated"
            client.publish(f"response/{msg.topic}",json.dumps(res))

    client.subscribe(topic)
    client.on_message = on_message


def run():
    client = connect_mqtt()
    subscribe(client)
    client.loop_forever()


if __name__ == '__main__':
    run()
