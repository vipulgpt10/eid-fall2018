import logging
import asyncio

from aiocoap import *

logging.basicConfig(level=logging.INFO)

async def main():
	
	context = await Context.create_client_context()
	await asyncio.sleep(2)
	payload = b"The quick brown fox jumps over the lazy dog.\n"
	request = Message(code=PUT, payload=payload)
	request.opt.uri_host = '127.0.0.1'
	request.opt.uri_path = ("other", "block")
	response = await context.request(request).response
	
	print('Result: %s\n%r'%(response.code, response.payload))

	
    

if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(main())
