# python3.6
import random, time, json, requests
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
        time.sleep(1)
        req=json.loads(msg.payload.decode())
        print(f"Received `{req}` from `{msg.topic}` topic")
        if 'bucket' in req.keys():
            if req['bucket']['task']=='list':
                url = 'http://localhost:8086/api/v2/buckets'
                headers = {'Authorization': 'Token token1'}
                r = requests.get(url, headers=headers)
                res=json.loads(r.content)
                client.publish(f"response/{msg.topic}",json.dumps(res['buckets']))
            elif req['bucket']['task']=='create':
                payload = {
                    "orgID": req['bucket']['o'],
                    "name": req['bucket']['n'],
                    'description':req['bucket']['d'],
                    "retentionRules":[
                        {
                        "type": "expire",
                        "everySeconds": req['bucket']['r'],
                        }
                    ]
                }
                url = 'http://localhost:8086/api/v2/buckets'
                headers = {'Authorization': 'Token token1'}
                r=requests.post(url, headers=headers,json=payload)
                res=json.loads(r.content)
                client.publish(f"response/{msg.topic}",json.dumps(res))
            elif req['bucket']['task']=='delete':
                id=req['bucket']['i']
                url = f'http://localhost:8086/api/v2/buckets/{id}'
                headers = {'Authorization': 'Token token1'}
                requests.delete(url, headers=headers)
                res="successfully deleted"
                client.publish(f"response/{msg.topic}",json.dumps(res))
            elif req['bucket']['task']=='update':
                res="successfully updated"
                client.publish(f"response/{msg.topic}",json.dumps(res))
        elif 'org' in req.keys():
            if req['org']['task']=='list':
                res=[
                    {
                        "id": "1e99b0e2686cf662",
                        "name": "abbc",
                        "description": "",
                        "createdAt": "2021-06-17T08:05:39.975749084Z",
                        "updatedAt": "2021-06-17T08:05:39.975749166Z"
                    },
                    {
                        "id": "1e99b0e2686cf663",
                        "name": "abb",
                        "description": "",
                        "createdAt": "2021-06-17T08:05:39.975749084Z",
                        "updatedAt": "2021-06-17T08:05:39.975749166Z"
                    }
                ]
                client.publish(f"response/{msg.topic}",json.dumps(res))
            elif req['org']['task']=='create':
                res="successfully created"
                client.publish(f"response/{msg.topic}",json.dumps(res))
            elif req['org']['task']=='delete':
                res="successfully deleted"
                client.publish(f"response/{msg.topic}",json.dumps(res))
            elif req['org']['task']=='update':
                res="successfully updated"
                client.publish(f"response/{msg.topic}",json.dumps(res))
        elif 'member' in req.keys():
            if req['member']['task']=='list':
                res=[
                    {
                        "id": "07b23f9eea10e000",
                        "name": "mashu",
                        "status": "active"
                    }
                ]
                client.publish(f"response/{msg.topic}",json.dumps(res))
            elif req['member']['task']=='create':
                res="successfully created"
                client.publish(f"response/{msg.topic}",json.dumps(res))
            elif req['member']['task']=='delete':
                res="successfully deleted"
                client.publish(f"response/{msg.topic}",json.dumps(res))
            elif req['member']['task']=='update':
                res="successfully updated"
                client.publish(f"response/{msg.topic}",json.dumps(res))
        elif 'user' in req.keys():
            if req['user']['task']=='list':
                res=[
                    {
                        "id": "07b23f9eea10e000",
                        "name": "mashu",
                        "status": "active"
                    }
                ]
                client.publish(f"response/{msg.topic}",json.dumps(res))
            elif req['user']['task']=='create':
                res="successfully created"
                client.publish(f"response/{msg.topic}",json.dumps(res))
            elif req['user']['task']=='delete':
                res="successfully deleted"
                client.publish(f"response/{msg.topic}",json.dumps(res))
            elif req['user']['task']=='update':
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
