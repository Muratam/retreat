import asyncio
import websockets
from yuni_parser import Packet, Environment

class YuniProxyObject:
    def __init__(self, module):
        pass

class YuniProxyModule:
    def __init__(self, port, hostname):
        self._port = port
        self._hostname = hostname
        self._ws_loop = self._websocket_loop()

    async def _websocket_loop(self):
        async with websockets.connect(f"ws://{self._hostname}:{self._port}") as ws:
            while True:
                await ws.send((yield))
                yield await ws.recv()

    async def _call_async(self, in_packet):
        await self._ws_loop.__anext__()
        out_packet = await self._ws_loop.asend(in_packet)
        return Environment().parse(out_packet)

    def _call(self, in_packet):
        return asyncio.get_event_loop().run_until_complete(self._call_async(in_packet))

    def _call_import(self, import_name):
        in_packet = Packet.by_import_statement(import_name)
        return self._call(in_packet)

    def __getattr__(self, name):
        return self._call_import(name)

# modules
py = YuniProxyModule(7200, "127.0.0.1")
js = YuniProxyModule(7201, "127.0.0.1")
# go = YuniProxyModule(7202, "127.0.0.1")
# cs = YuniProxyModule(7203, "127.0.0.1")
# cpp = YuniProxyModule(7204, "127.0.0.1")
# rs = YuniProxyModule(7205, "127.0.0.1")
