import sys
import asyncio
import urllib.parse
import websockets
import yuni_converter

async def server_echo(websocket):
    async for in_packet in websocket:
        output = yuni_converter.call_packet(in_packet)
        out_packet = yuni_converter.to_packet(output)
        await websocket.send(out_packet)

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
