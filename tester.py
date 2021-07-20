# python3.6
import random, time, json, requests, csv
from paho.mqtt import client as mqtt_client
from contextlib import closing

broker = 'localhost'
port = 1883
topic = "uimanager/influxdb"
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
        req=json.loads(msg.payload.decode())
        print(f"Received `{req}` from `{msg.topic}` topic")
        headers = {'Authorization': 'Token token1'}
        if 'query' in req.keys():
            host = 'http://localhost:8086/api/v2/query'
            headers['Accept']='application/csv'
            headers['Content-type']='application/vnd.flux'
            params = (
                ('bucket', 'drive'),
                ('org', 'abb'),
                ('precision', 'ns'),
            )
            start=req['query']['start']
            data = f'from(bucket:"drive")\n|> range(start:{start})\n|> sort(columns: ["_value"])\n|> limit(n: 4)'
            res=[]
            with closing(requests.post(url=host, headers=headers, params=params, data=data,stream=True)) as r:
                f = (line.decode('utf-8') for line in r.iter_lines())
                reader=csv.DictReader(f)
                for row in reader:
                    res.append(row)
        elif 'bucket' in req.keys():
            host = 'http://localhost:8086/api/v2/buckets/'
            if req['bucket']['task']=='list':
                r = requests.get(url=host, headers=headers)
                res=json.loads(r.content)['buckets']
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
                r=requests.post(url=host, headers=headers,json=payload)
                res=json.loads(r.content)
            elif req['bucket']['task']=='delete':
                id=req['bucket']['i']
                requests.delete(url=host+id, headers=headers)
                res="successfully deleted"
            elif req['bucket']['task']=='update':
                id=req['bucket']['i']
                if 'd' in req['bucket'].keys():
                    payload = { "description":req['bucket']['d']}
                elif 'n' in req['bucket'].keys():
                    payload = { "name":req['bucket']['n']}
                elif 'r' in req['bucket'].keys():
                    payload = { "retentionRules": { "everySeconds":req['bucket']['r'] }}
                r = requests.patch(url=host+id, headers=headers,json=payload)
                res=json.loads(r.content)
        elif 'org' in req.keys():
            host='http://localhost:8086/api/v2/orgs/'
            if req['org']['task']=='list':
                r = requests.get(url=host, headers=headers)
                res=json.loads(r.content)['orgs']
            elif req['org']['task']=='create':
                payload = {
                    "name": req['org']['n'],
                    'description':req['org']['d'],
                }
                r=requests.post(url=host, headers=headers,json=payload)
                res=json.loads(r.content)
            elif req['org']['task']=='delete':
                id=req['org']['i']
                requests.delete(url = host+id, headers=headers)
                res="successfully deleted"
            elif req['org']['task']=='update':
                orgID=req['org']['i']
                if 'description' in req['org'].keys():
                    payload = { "description":req['org']['description']}
                elif 'name' in req['org'].keys():
                    payload = { "name":req['org']['name']}
                r = requests.patch(url = host+orgID, headers=headers,json=payload)
                res=json.loads(r.content)
        elif 'member' in req.keys():
            if req['member']['task']=='list':
                res=[
                    {
                        "id": "07b23f9eea10e000",
                        "name": "mashu",
                        "status": "active"
                    }
                ]
            elif req['member']['task']=='create':
                res="successfully created"
            elif req['member']['task']=='delete':
                res="successfully deleted"
            elif req['member']['task']=='update':
                res="successfully updated"
        elif 'user' in req.keys():
            if req['user']['task']=='list':
                res=[
                    {
                        "id": "07b23f9eea10e000",
                        "name": "mashu",
                        "status": "active"
                    }
                ]
            elif req['user']['task']=='create':
                res="successfully created"
            elif req['user']['task']=='delete':
                res="successfully deleted"
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
