import random, time, json, requests, csv, datetime, threading
import paho.mqtt.client as mqtt_client
from contextlib import closing

broker = 'localhost'
port = 1883
topic = "uimanager/influxdb"
topic2 = "send/test"
headers = {'Authorization': 'Token token1'}

def query(host,req):
    headers['Accept']='application/csv'
    headers['Content-type']='application/vnd.flux'
    params = (
        ('bucket', req['bucket']),
        ('org', req['org']),
        ('precision', 'ns'),
    )
    data = f'from(bucket:"drive")\n|> range(start:{req["start"]})\n|> sort(columns: ["_value"])\n|> limit(n: 4)'
    res=[]
    with closing(requests.post(url=host, headers=headers, params=params, data=data,stream=True)) as r:
        f = (line.decode('utf-8') for line in r.iter_lines())
        reader=csv.DictReader(f)
        for row in reader:
            res.append(row)
    return res

def write(host,req):
    params = (
        ('org', 'abb'),
        ('bucket', 'drive'),
        ('precision', 's'),
    )
    time=datetime.datetime.strptime( req['data']['timestamp'], "%Y-%m-%dT%H:%M:%S.%fZ" )
    data = f"{req['serial']},paramId={req['data']['paramId']},unit={req['data']['unit']} value={req['data']['status']['value']} {int(datetime.datetime.timestamp(time))}"
    requests.post(url=host, headers=headers, params=params, data=data)
    return "successful"

def buckets(host,req):
    if req['task']=='list':
        r = requests.get(url=host, headers=headers)
        return json.loads(r.content)['buckets']
    elif req['task']=='create':
        payload = {
            "orgID": req['o'],
            "name": req['n'],
            'description':req['d'],
            "retentionRules":[
                {
                "type": "expire",
                "everySeconds": req['r'],
                }
            ]
        }
        r=requests.post(url=host, headers=headers,json=payload)
        return json.loads(r.content)
    elif req['task']=='delete':
        id=req['i']
        requests.delete(url=host+id, headers=headers)
        return "successfully deleted"
    elif req['task']=='update':
        id=req['i']
        if 'd' in req.keys():
            payload = { "description":req['d']}
        elif 'n' in req.keys():
            payload = { "name":req['n']}
        elif 'r' in req.keys():
            payload = { "retentionRules": { "everySeconds":req['r'] }}
        r = requests.patch(url=host+id, headers=headers,json=payload)
        return json.loads(r.content)

def orgs(host,req):
    if req['task']=='list':
        r = requests.get(url=host, headers=headers)
        return json.loads(r.content)['orgs']
    elif req['task']=='create':
        payload = {
            "name": req['n'],
            'description':req['d'],
        }
        r=requests.post(url=host, headers=headers,json=payload)
        return json.loads(r.content)
    elif req['task']=='delete':
        id=req['i']
        requests.delete(url = host+id, headers=headers)
        return "successfully deleted"
    elif req['task']=='update':
        orgID=req['i']
        if 'description' in req.keys():
            payload = { "description":req['description']}
        elif 'name' in req.keys():
            payload = { "name":req['name']}
        r = requests.patch(url = host+orgID, headers=headers,json=payload)
        return json.loads(r.content)

def member(host,req):
    if req['task']=='list':
        return [
            {
                "id": "07b23f9eea10e000",
                "name": "mashu",
                "status": "active"
            }
        ]
    elif req['task']=='create':
        return "successfully created"
    elif req['task']=='delete':
        return "successfully deleted"
    elif req['task']=='update':
        return "successfully updated"

def user(host,req):
    if req['task']=='list':
        return [
            {
                "id": "07b23f9eea10e000",
                "name": "mashu",
                "status": "active"
            }
        ]
    elif req['task']=='create':
        return "successfully created"
    elif req['task']=='delete':
        return "successfully deleted"
    elif req['task']=='update':
        return "successfully updated"

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected to MQTT Broker!")
        client.subscribe(topic)
        client.subscribe(topic2)
    else:
        print("Failed to connect, return code %d", rc)

def run(stop,repeat):
    while stop():
        print('query result...',repeat)
        time.sleep(repeat)

stop_threads = None
t1 = None

def newThread(repeat):
    global stop_threads
    return threading.Thread(target = run, args =(lambda : stop_threads,repeat))

def on_message(client, userdata, msg):
    req=json.loads(msg.payload.decode())
    print(f"Received `{req}` from `{msg.topic}` topic")
    host = 'http://'+broker+':8086/api/v2/'
    switcher = {
        'query': lambda: query(host+'query', req['query']),
        'write': lambda: write(host+'write', req['write']['message']),
        'buckets': lambda: buckets(host+'buckets', req['buckets']),
        'orgs': lambda: orgs(host+'orgs', req['orgs']),
        'member': lambda: member(host, req['member']),
        'user': lambda: user(host, req['user']),
    }
    if msg.topic==topic:
        for key in req.keys():
            res= switcher.get(key, lambda: "Empty Assignment.")()
            client.publish(f"response/{msg.topic}",json.dumps(res))
    elif msg.topic==topic2:
        if 'query' in req.keys():
            global stop_threads
            if req['query']['task']=='start':
                stop_threads = True
                global t1
                t1 = newThread(req['query']['num'])
                t1.start()
            elif req['query']['task']=='stop':
                print('query stopped')
                stop_threads = False
                t1.join()
        elif 'write' in req.keys():
            print('write')
            # write(host+'write', req['write']['message'])

if __name__ == '__main__':
    # generate client ID with pub prefix randomly
    client_id = f'python-mqtt-{random.randint(0, 100)}'
    # username = 'emqx'
    # password = 'public'
    client = mqtt_client.Client(client_id)
    # client.username_pw_set(username, password)
    client.on_connect = on_connect
    client.connect(broker, port)
    client.subscribe(topic)
    client.on_message = on_message
    client.loop_forever()
