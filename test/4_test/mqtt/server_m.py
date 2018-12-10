import paho.mqtt.client as mqtt
import time

# This is the Subscriber

global n
n = 0

def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    client.subscribe("topic/incoming")

def on_message(client, userdata, msg):
    global n
    n += 1
    message = msg.payload.decode()
    print('received: '+message)
    time.sleep(4)
    client.publish("topic/out", message)
    if n == 3:
        time.sleep(8)
        n = 0
        client.disconnect()


def start_mqtt():
    time.sleep(3)
    client = mqtt.Client()
    client.connect('10.0.0.246', 1883, 60)
    client.on_connect = on_connect
    client.on_message = on_message
    client.loop_forever()
    
start_mqtt()
