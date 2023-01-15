import json
from enum import Enum, auto
import builtins
import socket
import sys
import os

class YuniObjectType(Enum):
    Primitive = auto()
    Array = auto()
    Table = auto()
    Exception = auto()
    Object = auto()

    def to_string(type):
        for pair in _yuni_object_type_pair:
            if pair[0] == type:
                return pair[1]
        return ""

    def from_string(str):
        for pair in _yuni_object_type_pair:
            if pair[1] == str:
                return pair[0]
        return YuniObjectType.Undefined

_yuni_object_type_pair = [
    (YuniObjectType.Primitive, "primitive"),
    (YuniObjectType.Array, "array"),
    (YuniObjectType.Table, "table"),
    (YuniObjectType.Exception, "exception"),
    (YuniObjectType.Object, "object"),
]

class YuniObject:
    def _pack(type, value):
        return {
            "type": YuniObjectType.to_string(type),
            "value": value
        }

    def from_primitive(primitive):
        return YuniObject._pack(YuniObjectType.Primitive, primitive)

    def from_array(array, env):
        yuni_array = [YuniObject.from_python_object(x, env) for x in array]
        return YuniObject._pack(YuniObjectType.Array, yuni_array)

    def from_table(table, env):
        yuni_table = {}
        for k, v in table.items():
            yuni_table[k] = YuniObject.from_python_object(v, env)
        return YuniObject._pack(YuniObjectType.Table, yuni_table)

    def from_exception(exception):
        return YuniObject._pack(YuniObjectType.Exception, str(exception))

    def from_object(object, env):
        return YuniObject._pack(YuniObjectType.Object, env.register_object(object))

    def from_python_object(object, env):
        type_object = type(object)
        if (type_object == int) or (
            type_object == float) or (
            type_object == str) or (
            type_object == bool) or (
            object is None):
            return YuniObject.from_primitive(object)
        if type_object == list:
            return YuniObject.from_array(object, env)
        elif type_object == dict:
            return YuniObject.from_table(object, env)
        elif isinstance(object, Exception):
            return YuniObject.from_exception(object)
        return YuniObject.from_object(object, env)

    def interpret(yuni_object, env, raise_exception=False):
        try:
            object_type = YuniObjectType.from_string(yuni_object["type"])
            value = yuni_object["value"]
            if object_type == YuniObjectType.Primitive:
                return value
            elif object_type == YuniObjectType.Array:
                return [YuniObject.interpret(x, env, raise_exception) for x in value]
            elif object_type == YuniObjectType.Table:
                result = {}
                for k, v in value.items():
                    result[k] = YuniObject.interpret(v, env, raise_exception)
                return result
            elif object_type == YuniObjectType.Object:
                return env.get_object(value["obj_id"], value["env_id"])
            elif object_type == YuniObjectType.Exception:
                exception = Exception(value)
                if raise_exception: raise exception
                else: return exception
        except Exception as exception:
            if raise_exception: raise exception
            else: return exception
        return None

class YuniExprType(Enum):
    GetEnvId = auto()
    Object = auto()
    Invoke = auto()
    GetAttr = auto()
    Import = auto()

    def to_string(type):
        for pair in _packet_root_type_pair:
            if pair[0] == type:
                return pair[1]
        return ""

    def from_string(str):
        for pair in _packet_root_type_pair:
            if pair[1] == str:
                return pair[0]
        return YuniExprType.Undefined

_packet_root_type_pair = [
    (YuniExprType.GetEnvId, "get_env_id"),
    (YuniExprType.Object, "object"),
    (YuniExprType.Import, "import"),
    (YuniExprType.GetAttr, "get_attr"),
    (YuniExprType.Invoke, "invoke"),
]

_optional_attr_table = {
    "@ dir": "__dir__",
    "@ str": "__str__",
    "@ []": "__getitem__",
    "@ []=": "__setitem__",
    "@ in": "__contains__",
    "@ +": "__add__",
    "@ -": "__sub__",
    "@ *": "__mul__",
    "@ @": "__matmul__",
    "@ /": "__truediv__",
    "@ %": "__mod__",
    "@ **": "__pow__",
    "@ <<": "__lshift__",
    "@ >>": "__rshift__",
    "@ &": "__and__",
    "@ ^": "__xor__",
    "@ |": "__or__",
    "@ <": "__lt__",
    "@ <=": "__le__",
    "@ ==": "__eq__",
    "@ !=": "__ne__",
    "@ >=": "__ge__",
    "@ >": "__gt__",
    "@ !": "__not__",
    "@ ~": "__inv__",
    "@ 0+": "__pos__",
    "@ 0-": "__neg__",
    "@ +=": "__iadd__",
    "@ -=": "__isub__",
    "@ *=": "__imul__",
    "@ @=": "__imatmul__",
    "@ /=": "__itruediv__",
    "@ %=": "__imod__",
    "@ **=": "__ipow__",
    "@ <<=": "__ilshift__",
    "@ >>=": "__irshift__",
    "@ &=": "__iand__",
    "@ ^=": "__ixor__",
    "@ |=": "__ior__",
}
_rev_optional_attr_table = {}
for k, v in _optional_attr_table.items(): _rev_optional_attr_table[v] = k

class YuniExpr:
    def _pack(type, value):
        return {
            "type": YuniExprType.to_string(type),
            "value": value
        }
    def from_get_env_id_expr():
        return YuniExpr._pack(YuniExprType.GetEnvId, None)

    def from_object_expr(object, env):
        yuni_object = YuniObject.from_python_object(object, env)
        return YuniExpr._pack(YuniExprType.Object, yuni_object)

    def from_import_expr(import_name):
        return YuniExpr._pack(YuniExprType.Import, import_name)

    def from_get_attr_expr(object, attr_name, env):
        return YuniExpr._pack(YuniExprType.GetAttr, {
            "object": YuniObject.from_python_object(object, env),
            "attr_name": attr_name,
        })

    def from_invoke_expr(object, args, kwds, env):
        yuni_args = []
        for arg in args:
            yuni_args.append(YuniObject.from_python_object(arg, env))
        yuni_kwds = {}
        for k, v in kwds.items():
            yuni_kwds[k] = YuniObject.from_python_object(v, env)
        return YuniExpr._pack(YuniExprType.Invoke, {
            "object": YuniObject.from_python_object(object, env),
            "args": yuni_args,
            "kwds": yuni_kwds,
        })

    def interpret(yuni_expr, env, raise_exception=False):
        try:
            expr_type = YuniExprType.from_string(yuni_expr["type"])
            value = yuni_expr["value"]
            if expr_type == YuniExprType.GetEnvId:
                return env._id
            elif expr_type == YuniExprType.Object:
                return YuniObject.interpret(value, env, raise_exception)
            elif expr_type == YuniExprType.Import:
                return env.do_import(value)
            elif expr_type == YuniExprType.GetAttr:
                object = YuniObject.interpret(value["object"], env, raise_exception)
                attr_name = value["attr_name"]
                if attr_name in _optional_attr_table:
                    attr_name = _optional_attr_table[attr_name]
                return object.__getattribute__(attr_name)
            elif expr_type == YuniExprType.Invoke:
                object = YuniObject.interpret(value["object"], env, raise_exception)
                args = []
                for arg in value["args"]:
                    args.append(YuniObject.interpret(arg, env, raise_exception))
                kwds = {}
                for k, v in value["kwds"].items():
                    kwds[k] = YuniObject.interpret(v, env, raise_exception)
                return object.__call__(*args, **kwds)
        except Exception as exception:
            if raise_exception: raise exception
            else: return exception
        return value

class LocalResolver:
    def __init__(self, env):
        self._env = env

    def call_get_attr(self, object_proxy, name):
        object = self._env.get_object(object_proxy._obj_id, object_proxy._env_id)
        return object.__getattr__(name)

    def call_invoke(self, object_proxy, args, kwds):
        object = self._env.get_object(object_proxy._obj_id, object_proxy._env_id)
        return object.__call__(*args, **kwds)

class Environment:
    def __init__(self, id):
        self._imports = {
            "prelude": builtins,
        }
        self._objects = {}
        self._last_obj_id = 0
        self._id = id
        self._resolver_by_env_id = {
            id: LocalResolver(self)
        }

    def register_object(self, object):
        if isinstance(object, ObjectProxy):
            return {
                "obj_id": object._obj_id,
                "env_id": object._env_id
            }
        # FIXME: [A , A] のようになったときに、二重登録してしまうので治す
        # FIXME: object の 削除もできればしておきたい
        self._last_obj_id += 1
        self._objects[self._last_obj_id] = object
        return {
            "obj_id": self._last_obj_id,
            "env_id": self._id
        }

    def get_object(self, obj_id, env_id):
        if self._id == env_id:
            return self._objects[obj_id]
        return ObjectProxy(obj_id, env_id, self)

    def do_import(self, name):
        if name in self._imports:
            return self._imports[name]
        # if importlib.util.find_spec(name) is not None:
        self._imports[name] =  __import__(name)
        return self._imports[name]

    def from_packet(self, packet, raise_exception):
        yuni_expr = json.loads(packet)
        return YuniExpr.interpret(yuni_expr, self, raise_exception)

    def to_packet(self, python_object):
        yuni_expr = YuniExpr.from_object_expr(python_object, self)
        return json.dumps(yuni_expr)

    def __str__(self):
        return f"{22}"

    def __repr__(self):
        return f"{11}"

class ObjectProxy:
    # FIXME: 標準出力を見やすいようにOptionalで設定する
    def __init__(self, obj_id, env_id, env):
        self._obj_id = obj_id
        self._env_id = env_id
        self._env = env

    def __del__(self):
        # FIXME:
        pass

    # util
    def __get_resolver(self):
        if self._env_id in self._env._resolver_by_env_id:
            return self._env._resolver_by_env_id[self._env_id]
        raise Exception(f"Env({self._env_id}) is not found. Cannot resolve.")

    # eq
    def __eq__(self, __o):
        if not isinstance(__o, ObjectProxy):
            return False
        # FIXME: Struct的なものを比較できない
        return self._obj_id == __o._obj_id and self._env_id == __o._env_id
    def __ne__(self, __o):
        return not self.__eq__(__o)

    # attr
    def __getattr__(self, __name):
        return self.__get_resolver().call_get_attr(self, __name)
    def __call__(self, *args, **kwds):
        return self.__get_resolver().call_invoke(self, args, kwds)

    # optional methods
    def __call_attr(self, attr_name, *args):
        attr = self.__get_resolver().call_get_attr(self, attr_name)
        if isinstance(attr, ObjectProxy):
            return attr.__get_resolver().call_invoke(attr, args, {})
        else:
            raise Exception(f"Cannot Call {attr_name}")
    def __repr__(self):
        return self.__str__()
    # NOTE: __set_attr__ で上書きするとoperator override が無視されるので愚直に書く
    def __add__(self, *args): return self.__call_attr(_rev_optional_attr_table["__add__"], *args)
    def __dir__(self, *args): return self.__call_attr(_rev_optional_attr_table["__dir__"], *args)
    def __str__(self, *args): return self.__call_attr(_rev_optional_attr_table["__str__"], *args)
    def __getitem__(self, *args): return self.__call_attr(_rev_optional_attr_table["__getitem__"], *args)
    def __setitem__(self, *args): return self.__call_attr(_rev_optional_attr_table["__setitem__"], *args)
    def __contains__(self, *args): return self.__call_attr(_rev_optional_attr_table["__contains__"], *args)
    def __add__(self, *args): return self.__call_attr(_rev_optional_attr_table["__add__"], *args)
    def __sub__(self, *args): return self.__call_attr(_rev_optional_attr_table["__sub__"], *args)
    def __mul__(self, *args): return self.__call_attr(_rev_optional_attr_table["__mul__"], *args)
    def __matmul__(self, *args): return self.__call_attr(_rev_optional_attr_table["__matmul__"], *args)
    def __truediv__(self, *args): return self.__call_attr(_rev_optional_attr_table["__truediv__"], *args)
    def __mod__(self, *args): return self.__call_attr(_rev_optional_attr_table["__mod__"], *args)
    def __pow__(self, *args): return self.__call_attr(_rev_optional_attr_table["__pow__"], *args)
    def __lshift__(self, *args): return self.__call_attr(_rev_optional_attr_table["__lshift__"], *args)
    def __rshift__(self, *args): return self.__call_attr(_rev_optional_attr_table["__rshift__"], *args)
    def __and__(self, *args): return self.__call_attr(_rev_optional_attr_table["__and__"], *args)
    def __xor__(self, *args): return self.__call_attr(_rev_optional_attr_table["__xor__"], *args)
    def __or__(self, *args): return self.__call_attr(_rev_optional_attr_table["__or__"], *args)
    def __lt__(self, *args): return self.__call_attr(_rev_optional_attr_table["__lt__"], *args)
    def __le__(self, *args): return self.__call_attr(_rev_optional_attr_table["__le__"], *args)
    def __eq__(self, *args): return self.__call_attr(_rev_optional_attr_table["__eq__"], *args)
    def __ne__(self, *args): return self.__call_attr(_rev_optional_attr_table["__ne__"], *args)
    def __ge__(self, *args): return self.__call_attr(_rev_optional_attr_table["__ge__"], *args)
    def __gt__(self, *args): return self.__call_attr(_rev_optional_attr_table["__gt__"], *args)
    def __not__(self, *args): return self.__call_attr(_rev_optional_attr_table["__not__"], *args)
    def __inv__(self, *args): return self.__call_attr(_rev_optional_attr_table["__inv__"], *args)
    def __pos__(self, *args): return self.__call_attr(_rev_optional_attr_table["__pos__"], *args)
    def __neg__(self, *args): return self.__call_attr(_rev_optional_attr_table["__neg__"], *args)
    def __iadd__(self, *args): return self.__call_attr(_rev_optional_attr_table["__iadd__"], *args)
    def __isub__(self, *args): return self.__call_attr(_rev_optional_attr_table["__isub__"], *args)
    def __imul__(self, *args): return self.__call_attr(_rev_optional_attr_table["__imul__"], *args)
    def __imatmul__(self, *args): return self.__call_attr(_rev_optional_attr_table["__imatmul__"], *args)
    def __itruediv__(self, *args): return self.__call_attr(_rev_optional_attr_table["__itruediv__"], *args)
    def __imod__(self, *args): return self.__call_attr(_rev_optional_attr_table["__imod__"], *args)
    def __ipow__(self, *args): return self.__call_attr(_rev_optional_attr_table["__ipow__"], *args)
    def __ilshift__(self, *args): return self.__call_attr(_rev_optional_attr_table["__ilshift__"], *args)
    def __irshift__(self, *args): return self.__call_attr(_rev_optional_attr_table["__irshift__"], *args)
    def __iand__(self, *args): return self.__call_attr(_rev_optional_attr_table["__iand__"], *args)
    def __ixor__(self, *args): return self.__call_attr(_rev_optional_attr_table["__ixor__"], *args)
    def __ior__(self, *args): return self.__call_attr(_rev_optional_attr_table["__ior__"], *args)

class Socket:
    def __init__(self, sock):
        self._socket = sock

    def __del__(self):
        self._socket.close()

    def recv(self):
        size_byte_8 = self._socket.recv(8)
        size = int.from_bytes(size_byte_8, "big")
        return self._socket.recv(size).decode("utf-8")

    def send(self, packet):
        packet_byte = packet.encode("utf-8")
        size = len(packet_byte)
        size_byte_8 = int(size).to_bytes(8, "big")
        self._socket.send(size_byte_8)
        self._socket.send(packet_byte)

class YuniProxyModule:
    def __init__(self, port, hostname):
        self._port = port
        self._hostname = hostname
        self._env = Environment(f"pid:{os.getpid()}") # f"uuid4:{uuid.uuid4()}
        sock = socket.socket()
        sock.connect((self._hostname, int(self._port)))
        self._socket = Socket(sock)
        # self._socket.send(self._env._id)
        self._call_set_env_id()

    def _call(self, in_packet):
        self._socket.send(in_packet)
        out_packet = self._socket.recv()
        return self._env.from_packet(out_packet, raise_exception=True)

    def _call_set_env_id(self):
        in_packet = json.dumps(YuniExpr.from_get_env_id_expr())
        env_id = self._call(in_packet)
        self._env._resolver_by_env_id[env_id] = self

    def _call_import(self, import_name):
        in_packet = json.dumps(YuniExpr.from_import_expr(import_name))
        return self._call(in_packet)

    def call_get_attr(self, object_proxy, name):
        in_packet = json.dumps(YuniExpr.from_get_attr_expr(object_proxy, name, self._env))
        return self._call(in_packet)

    def call_invoke(self, object_proxy, args, kwds):
        in_packet = json.dumps(YuniExpr.from_invoke_expr(object_proxy, args, kwds, self._env))
        return self._call(in_packet)

    def __getattr__(self, name):
        return self._call_import(name)

    def run_server(hostname, port):
        server_socket = socket.socket()
        server_socket.bind((hostname, int(port)))
        server_socket.listen()
        # シングルスレッドで処理する
        env = Environment(f"pid:{os.getpid()}") # f"uuid4:{uuid.uuid4()}
        while True:
            socket_acc_raw, addr = server_socket.accept()
            print(f"connect: {addr}")
            socket_acc = Socket(socket_acc_raw)
            while True:
                try:
                    in_packet = socket_acc.recv()
                    if not in_packet: break # killed
                    output = env.from_packet(in_packet, raise_exception=False)
                    out_packet = env.to_packet(output)
                    socket_acc.send(out_packet)
                except Exception as e:
                    print(e)
                    break

if __name__ == "__main__":
    # as Server
    if len(sys.argv) != 2:
        print("please specify the address")
        quit()
    hostname, port = sys.argv[1].split(":")
    YuniProxyModule.run_server(hostname, port)
else:
    # as Module
    py = YuniProxyModule(7200, "127.0.0.1")
    # js = YuniProxyModule(7201, "127.0.0.1")
    # go = YuniProxyModule(7202, "127.0.0.1")
    # cs = YuniProxyModule(7203, "127.0.0.1")
    # cpp = YuniProxyModule(7204, "127.0.0.1")
    # rs = YuniProxyModule(7205, "127.0.0.1")
