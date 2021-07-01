from paho.mqtt import client as mqtt_client

broker = 'localhost'
port = 1883
# generate client ID with pub prefix randomly
client_id = f'python-mqtt-{random.randint(0, 1000)}'
client = mqtt_client.Client(client_id)
client.connect(broker, port)


def publish(msg,topic):
    return client.publish(topic, msg)