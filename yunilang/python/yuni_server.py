import sys
import asyncio
import urllib.parse
import websockets
from yuni_parser import Packet, Environment

async def server_echo(websocket):
    env = Environment()
    while True:
        try:
            async for in_packet in websocket:
                output = env.parse(in_packet)
                out_packet = Packet.by_python_object(output, env)
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
        async with websockets.serve(server_echo, netloc.hostname, netloc.port):
            await asyncio.Future()
    asyncio.run(serve())

if __name__ == "__main__":
    main()
