#Publisher

import paho.mqtt.client as mqtt
import socket
import time

class MQTTClient(object):
    def __init__(self):
        self.response = None
        self.ms = 0
        self.client = mqtt.Client()
        self.client.connect('10.201.9.97', 1883, 60)
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message

    def on_connect(self, client, userdata, flags, rc):
        self.client.subscribe("topic/out")

    def on_message(self, client, userdate, msg):
        self.ms = int(round(time.time()*1000))-self.ms
        msg = msg.payload.decode().split(',')
        length = len(msg)
        self.client.disconnect()
        self.response = [self.ms, length]

    def publish(self, topic, msg):
        self.response = None
        self.ms = int(round(time.time()*1000))
        self.client.publish(topic, msg)
        while self.response == None:
            self.client.loop_forever()
        return self.response


a = MQTTClient()
# the return value rc is a list that contains the time it took and the length of the msg:
# rc = [time, length] eg.: rc = [44, 3] ---it took 44ms, received 3 numbers
rc = a.publish("topic/incoming", "22,23,24")
print(rc)
