import asyncio
import websockets
import uuid
import json
from yuni_parser import YuniExpr, Environment

class YuniProxyObject:
    def __init__(self, module):
        pass

class YuniProxyModule:
    def __init__(self, port, hostname):
        self._port = port
        self._hostname = hostname
        self._env = Environment(str(uuid.uuid4()))
        self._ws_loop = self._websocket_loop()
        self._call_set_ws_env_id()

    async def _websocket_loop(self):
        async with websockets.connect(f"ws://{self._hostname}:{self._port}") as ws:
            while True:
                await ws.send((yield))
                yield await ws.recv()

    async def _call_async(self, in_packet):
        await self._ws_loop.__anext__()
        out_packet = await self._ws_loop.asend(in_packet)
        return self._env.from_packet(out_packet, raise_exception=True)

    def _call(self, in_packet):
        return asyncio.get_event_loop().run_until_complete(self._call_async(in_packet))

    def _call_set_ws_env_id(self):
        in_packet = json.dumps(YuniExpr.from_get_env_id_expr())
        ws_env_id = self._call(in_packet)
        self._env.resolver_by_env_id[ws_env_id] = self

    def _call_import(self, import_name):
        in_packet = json.dumps(YuniExpr.from_import_expr(import_name))
        return self._call(in_packet)

    def call_get_attr(self, object_proxy, name):
        in_packet = json.dumps(YuniExpr.from_get_attr_expr(object_proxy, name, self._env))
        return self._call(in_packet)

        # object = self.env.get_object(object_proxy.obj_id, object_proxy.env_id)
        # return object.__get_attr__(name)
        # in_packet = json.dumps(YuniExpr.from_import_expr(import_name))
        # return self._call(in_packet)


    def __getattr__(self, name):
        return self._call_import(name)

# modules
py = YuniProxyModule(7200, "127.0.0.1")
# js = YuniProxyModule(7201, "127.0.0.1")
# go = YuniProxyModule(7202, "127.0.0.1")
# cs = YuniProxyModule(7203, "127.0.0.1")
# cpp = YuniProxyModule(7204, "127.0.0.1")
# rs = YuniProxyModule(7205, "127.0.0.1")
