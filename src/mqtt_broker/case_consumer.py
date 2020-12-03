import paho.mqtt.client as mqtt
import time
import collections
import json
import csv


# data_json = open('data.csv', 'w')
writer_csv = csv.writer(open('data.csv', 'w'), delimiter=';', lineterminator='\n')
header = ['time', 'topic', 'message']
# writer_csv.writerow(header)


def crete_tag_time():
    s = time.localtime(time.time())

    year = str(s[0])
    month = s[1]
    if month < 10:
        month = "0" + str(month)
    day = s[2]
    if day < 10:
        day = "0" + str(day)
    hours = s[3]
    if hours < 10:
        hours = "0" + str(hours)
    m = s[4]
    if m < 10:
        m = "0" + str(m)
    sec = s[5]
    if sec < 10:
        sec = "0" + str(sec)

    ltime = str(year) + "-" + str(month) + "-" + str(day) + "_" + str(hours)
    ltime = ltime + ":" + str(m) + ":" + str(sec)
    # print("time", ltime)

    return ltime


# The callback for when the client receives a CONNACK response from the server.
def on_connect(consumer, userdata, flags, rc):
    print("Connected with result code " + str(rc))
    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.

    if rc == 0:
        consumer.connected_bad = True
        consumer.bad_connected = False
        consumer.subscribe("/data")
        # consumer.subscribe("/aircrafts")
    else:
        consumer.bad_connection_flag = True
        consumer.bad_count += 1
        consumer.connected_flag = False


# The callback for when a PUBLISH message is received from the server.
def on_message(consumer, userdata, msg):
    topic = msg.topic
    m_decode = str(msg.payload.decode('utf-8', 'ignore'))
    # print('Message received', topic)
    # print('Message:', m_decode)

    message_handler(consumer, m_decode, topic)


def message_handler(consumer, msg, topic):
    tag_time = crete_tag_time()

    data = collections.OrderedDict()
    data["time"] = tag_time
    data["topic"] = topic
    data["message"] = msg

    rows = zip([data[col] for col in header])
    for row in rows:
        writer_csv.writerow(row)

    print('save data in', tag_time)


if __name__ == "__main__":
    broker = '95.31.7.170'
    port = 1883

    consumer = mqtt.Client()
    consumer.connect(broker, port, keepalive=60)

    consumer.on_connect = on_connect
    consumer.on_message = on_message

    consumer.loop_forever()
