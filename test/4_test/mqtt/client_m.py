#Publisher

import paho.mqtt.client as mqtt
import socket
import time

class MQTTClient(object):
    def __init__(self):
        self.response = None
        self.ms = 0
        self.client = mqtt.Client()
        self.client.connect('10.0.0.246', 1883, 60)
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message

    def on_connect(self, client, userdata, flags, rc):
        self.client.subscribe("topic/out")

    def on_message(self, client, userdate, msg):
        self.ms = int(round(time.time()*1000))-self.ms
        msg = msg.payload.decode().split(',')
        length = len(msg)
        self.response = [self.ms, length]
        self.client.disconnect()
        

    def publish(self, topic, msg):
        self.response = None
        self.ms = int(round(time.time()*1000))
        self.client.publish(topic, msg)
        while self.response == None:
            self.client.loop_forever()
        self.client.reconnect()
        return self.response

    def disconnect(self):
        self.client.disconnect()
        
        
mqtt_instance = MQTTClient()

msg = 'msg'

for x in range(0, 3):
	print('[mqtt] Publishing for the '+str(x+1)+'th time')
	rc = mqtt_instance.publish("topic/incoming", msg)
	print('[mqtt] Received')
	print(rc[0])
	print(rc[1])


