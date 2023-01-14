import asyncio
import websockets
import yuni_converter

class YuniProxyObject:
    def __init__():
        pass

class YuniProxy:
    def __init__(self, port, hostname):
        self.port = port
        self.hostname = hostname
        # asyncio.run(self.websocket_loop())

    # async def websocket_loop(self):
    #     pass
    #     # async with websockets.connect(f"ws://{self.hostname}:{self.port}") as ws:
    #     #     await ws.send(yuni_converter.to_packet("Hello World"))
    #     #     await ws.recv()
    #     #     print(10)

    async def call(self, content):
        async with websockets.connect(f"ws://{self.hostname}:{self.port}") as ws:
            in_packet = yuni_converter.to_packet(content)
            await ws.send(in_packet)
            out_packet = await ws.recv()
            return yuni_converter.call_packet(out_packet)

    def __getattr__(self, name):
        result = asyncio.run(self.call(name))
        print(result)
        return result

# async def hello():
#     async with websockets.connect("ws://localhost:7200") as websocket:
#         await websocket.recv()
#         print(10)
#     #     packet = yuni_converter.to_packet("Hello World!")
#     #     await websocket.send(packet)
#     #     result = await websocket.recv()
#     #     print(result)
# asyncio.run(hello())

# python
py = YuniProxy(7200, "127.0.0.1")
# js
js = YuniProxy(7201, "127.0.0.1")
