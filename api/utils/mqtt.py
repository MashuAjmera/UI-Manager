from paho.mqtt import client as mqtt_client
import random 

broker = 'localhost'
port = 1883
# generate client ID with pub prefix randomly
client_id = f'python-mqtt-{random.randint(0, 1000)}'
client = mqtt_client.Client(client_id)

res=""

def on_message(client, userdata, msg):
    global res
    res=msg.payload.decode()
    client.disconnect()

def request(msg,topic):
    try:
        client.connect(broker, port, keepalive=10)
        client.subscribe(f"response/{topic}")
        client.on_message = on_message
        result=client.publish(topic, msg)
        status = result[0]
        if status == 0:
            client.loop_forever()
            if res=="":
                return "Server could not be contacted"
            else:
                return res
        else:
            client.disconnect()
            return f"Failed to send message to topic {topic}"
    except:
        return "Connection could not be establised with the broker."    