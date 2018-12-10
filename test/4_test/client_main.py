import paho.mqtt.client as mqtt
import socket
import time

import asyncio
from aiocoap import *


from tornado.ioloop import IOLoop, PeriodicCallback
from tornado import gen
from tornado.websocket import websocket_connect

import tornado.web
import tornado.websocket
import tornado.ioloop

import time


# MQTT
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
        
# COAP
class COAPClient(object):
    def __init__(self):
        self.ms = 0
        self.length = 0
        self.context = None
        asyncio.get_event_loop().run_until_complete(self.create_context())

    async def create_context(self):
        self.context = await Context.create_client_context()

    async def put(self, msg):
        self.ms = int(round(time.time()*1000))
        request = Message(code=PUT, payload=bytes(msg, 'utf-8'))
        request.opt.uri_host = '127.0.0.1'
        request.opt.uri_path = ("other", "block")
        response = await self.context.request(request).response
        self.ms = int(round(time.time()*1000))-self.ms
        self.length = len(response.payload.decode().split(','))
    
    def return_value(self):
        return [self.ms, self.length]

# WebSocket

class Client(object):
    def __init__(self, url, timeout):
        self.url = url
        self.timeout = timeout
        self.ioloop = IOLoop.instance()
        self.ws = None
        self.ms = 0
        self.length = 0
        
    @gen.coroutine
    def connect(self):
        print ("trying to connect")
        
        try:
            self.ws = yield websocket_connect(self.url)
        except Exception as e:
            print("connection error")
        else:
            print("connected")
            self.ms = int(round(time.time()*1000))
            self.ws.write_message("msg")
            msg = yield self.ws.read_message()
            self.ms = int(round(time.time()*1000))-self.ms
            self.length = 1
            print(msg)
            self.ioloop.stop()


    def return_value(self):
        return [self.ms, self.length]



def start_profiling():
	mqtt_instance = MQTTClient()     
	
	for x in range(0, 5):
		print('[MQTT] Publishing #'+str(x+1))
		rc = mqtt_instance.publish("topic/incoming", 'msg')
		print('[MQTT] Received')
		print(rc[0])
		print(rc[1])
		
	coap_instance = COAPClient()
	for x in range(0, 5):
		print('[COAP] PUT msg #'+str(x+1))
		asyncio.get_event_loop().run_until_complete(coap_instance.put('msg'))
		print('[COAP] Received')
		rc = coap_instance.return_value()
		print(rc[0])
		print(rc[1])
		
	client = Client("ws://localhost:3000", 5)
	for x in range(0, 5):
		print('Websocket msg#'+str(x+1))
		client.connect()
		client.ioloop.start()
		rc = client.return_value()
		print(rc[0])
		print(rc[1])
	

start_profiling()
