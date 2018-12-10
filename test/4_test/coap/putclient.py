import asyncio
from aiocoap import *
import time

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
        

coap_instance = COAPClient()
for x in range(0, 3):
	print('[coap] Sending the '+str(x+1)+'th PUT message')
	asyncio.get_event_loop().run_until_complete(coap_instance.put('msg'))
	print('[coap] Received')
	rc = coap_instance.return_value()
	print(rc[0])
	print(rc[1])

