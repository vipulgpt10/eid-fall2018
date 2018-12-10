import sys
import threading
import _thread

import paho.mqtt.client as mqtt
import time

import datetime


import asyncio

import aiocoap.resource as resource
import aiocoap

import tornado.web
import tornado.websocket
import tornado.ioloop
import tornado.options

import tornado.httpserver
import time

from tornado.options import define, options

define("port", default=3000 , help="run on the given port", type=int)



# Start MQTT Code

global n1
n1 = 0


def on_connect(client, userdata, flags, rc):
    print("[MQTT] Connected with result code "+str(rc))
    client.subscribe("topic/incoming")

def on_message(client, userdata, msg):
    global n1
    n1 += 1
    message = msg.payload.decode()
    print('[MQTT] MSG Received: '+message)
    time.sleep(100.0/1000.0)
    client.publish("topic/out", message)
    if n1 == 20:
        time.sleep(5)
        n1 = 0

def run_mqtt():
    time.sleep(1)
    client = mqtt.Client()
    client.connect('10.0.0.246', 1883, 60)
    client.on_connect = on_connect
    client.on_message = on_message
    client.loop_forever()
    
t1 = threading.Thread(name="run_mqtt", target=run_mqtt)

# End MQTT Code


# Start COAP Code 
class BlockResource(resource.Resource):
   
    def __init__(self):
        super().__init__()
    
    def set_content(self, content):
        self.content = content

    async def render_get(self, request):
        return aiocoap.Message(payload=self.content)
    
    async def render_put(self, request):
        print('[COAP] PUT payload: %s' % request.payload)
        self.set_content(request.payload)
        return aiocoap.Message(payload=self.content)


def run_coap():
    print('[COAP] coap started')
    root = resource.Site()
    root.add_resource(('.well-known', 'core'),
                      resource.WKCResource(root.get_resources_as_linkheader))
    root.add_resource(('other', 'block'), BlockResource())
    asyncio.Task(aiocoap.Context.create_server_context(root))
    asyncio.get_event_loop().run_forever()


#t2 = threading.Thread(name="run_coap", target=run_coap)

# End COAP 

# Start WebSocket

global n2
n2 = 0

class Application(tornado.web.Application):
    def __init__(self):
        handlers = [(r"/", MainHandler)]
        settings = dict(debug=True)
        tornado.web.Application.__init__(self, handlers, **settings)


class MainHandler(tornado.websocket.WebSocketHandler):
	def on_message(self, message):
		global n2
		n2 += 1
		print('[WebSocket] Message received')
		self.write_message(message)
		if n2 == 20:
			n2 = 0
			time.sleep(1)

	def check_origin(self, origin):
		return True

	def open(self):
		print("[WebSocket] A client connected.")

	def on_close(self):
		print("[WebSocket] A client disconnected")

			
def run_websocket():
	asyncio.set_event_loop(asyncio.new_event_loop())
	tornado.options.parse_command_line()
	app = Application()
	app.listen(options.port)
	print('[WebSocket] Web socket started')
	while True:
		tornado.ioloop.IOLoop.instance().start()

t3 = threading.Thread(name="run_websocket", target=run_websocket)
		
# End WebSocket
			

if __name__ == '__main__':
	
	t1.daemon = True
	t1.start()
	t3.daemon = True
	t3.start()
	run_coap()
	while True:
		i = 1
