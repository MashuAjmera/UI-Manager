from paho.mqtt import client as mqtt_client
import random 

broker = 'localhost'
port = 1883
# generate client ID with pub prefix randomly
client_id = f'python-mqtt-{random.randint(0, 1000)}'
client = mqtt_client.Client(client_id)
client.connect(broker, port)


def publish(msg,topic):
    result=client.publish(topic, msg)
    status = result[0]
    if status == 0:
        return f"Send `{msg}` to topic `{topic}`"
    else:
        return f"Failed to send message to topic {topic}"