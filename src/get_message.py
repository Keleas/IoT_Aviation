import random
import time

from paho.mqtt import client as mqtt_client


broker = '127.0.0.1'
port = 1883
topic = "/test_data/mqtt"
# generate client ID with pub prefix randomly
# client_id = f'python-mqtt-{random.randint(0, 1000)}'
client_id = 42


def run():
    import paho.mqtt.client as mqtt

    consumer = mqtt.Client()
    consumer.connect(broker, port, keepalive=20)

    consumer.on_connect = on_connect
    consumer.on_message = on_message

    consumer.loop_forever()


# The callback for when the client receives a CONNACK response from the server.
def on_connect(consumer, userdata, flags, rc):
    print("Connected with result code " + str(rc))
    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.

    if rc == 0:
        consumer.connected_bad = True
        consumer.bad_connected = False
        consumer.subscribe(topic)
    else:
        consumer.bad_connection_flag = True
        consumer.bad_count += 1
        consumer.connected_flag = False


# The callback for when a PUBLISH message is received from the server.
def on_message(consumer, userdata, msg):
    topic = msg.topic
    m_decode = str(msg.payload.decode('utf-8', 'ignore'))
    print('Message received', topic)
    print('Message received', m_decode)


if __name__ == '__main__':
    run()
