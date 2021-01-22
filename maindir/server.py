import asyncio
import json

from constants import *
from helpers import key_names, redis

counter = 0


async def run_server(host, port):
    print('fuk', flush=True)
    server = await asyncio.start_server(serve_client, host, port)
    # server = await asyncio.start_server(serve_client, host)
    await server.serve_forever()


async def serve_client(reader, writer):
    global counter
    cid = counter
    counter += 1
    print(f'Client #{cid} connected', flush=True)

    request = await read_request(reader)

    if request is None:
        print(f'Client #{cid} unexpectedly disconnected', flush=True)
    else:
        response = await handle_request(request)
        print(response)
        await write_response(writer, response, cid)


async def read_request(reader, ):
    request = bytearray()
    while True:
        chunk = await reader.read(1000)
        print(chunk)
        if not chunk:
            # Клиент преждевременно отключился.
            break

        request += chunk
        return request

    return None


async def handle_request(request):
    print(request, flush=True)
    # if request == b'\n':
    response = list()
    flight_keys_for_check = key_names(days=days, flights=flights, suffix=cheapest_day_fly_redis_key)
    print('in first loop', flush=True)
    for key in flight_keys_for_check:
        print('in second loop', flush=True)
        redis_data = redis.get(key)
        if redis_data is not None and redis_data != 'empty':
            response.append(json.loads(redis_data))
        else:
            response.append('empty')

    return json.dumps(response).encode()


async def write_response(writer, response, cid):
    writer.write(response)
    await writer.drain()
    writer.close()
    print(f'Client #{cid} has been served', flush=True)


if __name__ == '__main__':
    asyncio.run(run_server(server_host, server_port))
