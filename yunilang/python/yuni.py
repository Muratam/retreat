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
        self.ws_loop = self.websocket_loop()

    async def websocket_loop(self):
        async with websockets.connect(f"ws://{self.hostname}:{self.port}") as ws:
            while True:
                content = yield True
                in_packet = yuni_converter.to_packet(content)
                await ws.send(in_packet)
                out_packet = await ws.recv()
                yield yuni_converter.call_packet(out_packet)

    async def call(self, content):
        ok = await self.ws_loop.__anext__()
        if not ok:
            quit("no connection")
        return await self.ws_loop.asend(content)

    def __getattr__(self, name):
        return asyncio.get_event_loop().run_until_complete(self.call(name))

# python
py = YuniProxy(7200, "127.0.0.1")
# js
js = YuniProxy(7201, "127.0.0.1")
