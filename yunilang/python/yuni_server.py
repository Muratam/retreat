import sys
import asyncio
import urllib.parse
import websockets
import uuid
from yuni_parser import Environment

async def server(websocket):
    env = Environment(str(uuid.uuid4()))
    while True:
        try:
            async for in_packet in websocket:
                output = env.from_packet(in_packet, raise_exception=False)
                out_packet = env.to_packet(output)
                await websocket.send(out_packet)
        except Exception as e:
            print(e)
            return

def main():
    if len(sys.argv) <= 1:
        print("please specify address")
        return
    netloc = urllib.parse.urlsplit(f"//{sys.argv[1]}")
    if not netloc.hostname or not netloc.port:
        print("please specify valid address")
        return
    async def serve():
        async with websockets.serve(server, netloc.hostname, netloc.port):
            await asyncio.Future()
    asyncio.run(serve())

if __name__ == "__main__":
    main()
