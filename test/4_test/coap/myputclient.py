import asyncio
from aiocoap import *


async def main():

    context = await Context.create_client_context()

    payload = b'1111'
    request = Message(code=PUT, payload=payload)
    request.opt.uri_host = '127.0.0.1'  # change address
    request.opt.uri_path = ("other", "block")

    response = await context.request(request).response

    print('Result: %s\n%r'%(response.payload))

if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(main())
