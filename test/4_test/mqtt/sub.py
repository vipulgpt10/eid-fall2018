import paho.mqtt.client as mqtt

# This is the Subscriber

def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    client.subscribe("topic/incoming")

def on_message(client, userdata, msg):
    print('received: '+msg.payload.decode())
    client.publish("topic/out", msg.payload.decode())
    client.disconnect()

client = mqtt.Client()
client.connect('10.0.0.39',1883,60)

client.on_connect = on_connect
client.on_message = on_message

client.loop_forever()
