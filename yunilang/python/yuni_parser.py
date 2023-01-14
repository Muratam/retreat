import json
from enum import Enum, auto
from types import ModuleType
import importlib
import builtins

class YuniObjectType(Enum):
    Primitive = auto()
    Array = auto()
    Table = auto()
    Object = auto()
    Undefined = auto()
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

    def from_object(object, env):
        # FIXME: [A , A] のようになったときに、二重登録しそう
        id = env.register_object(object)
        return YuniObject._pack(YuniObjectType.Object, id)

    def from_python_object(object, env):
        type_object = type(object)
        if (type_object == int) or (
            type_object == float) or (
            type_object == str) or (
            type_object == bool) or (
            type_object == None):
            return YuniObject.from_primitive(object)
        if type_object == list:
            return YuniObject.from_array(object, env)
        if type_object == dict:
            return YuniObject.from_table(object, env)
        return YuniObject.from_object(object, env)

    def interpret(yuni_object, env):
        object_type = YuniObjectType.from_string(yuni_object["type"])
        value = yuni_object["value"]
        if object_type == YuniObjectType.Primitive:
            return value
        elif object_type == YuniObjectType.Array:
            return [env.interpret(x, env) for x in value]
        elif object_type == YuniObjectType.Table:
            result = {}
            for k, v in value.items():
                result[k] = env.interpret(v, env)
            return result
        elif object_type == YuniObjectType.Object:
            return env.get_object(value)
        print(yuni_object, "not found")
        return None


class YuniExprType(Enum):
    Object = auto()
    Invoke = auto()
    Import = auto()
    # StdOut = auto() # エラーを見やすいようにOptionalで設定する
    Undefined = auto()
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
    (YuniExprType.Object, "object"),
    (YuniExprType.Invoke, "invoke"),
    (YuniExprType.Import, "import"),
    # (PacketType.StdOut, "stdout"),
]

class YuniExpr:
    def _pack(type, value):
        return {
            "type": YuniExprType.to_string(type),
            "value": value
        }

    def from_object_expr(object, env):
        yuni_object = YuniObject.from_python_object(object, env)
        return YuniExpr._pack(YuniExprType.Object, yuni_object)

    def from_invoke_expr(function_invoke):
        # TODO:
        # TODO: object の delete も忘れないようにする
        return YuniExpr._pack(YuniExprType.Invoke, function_invoke)

    def from_import_expr(import_name: str):
        return YuniExpr._pack(YuniExprType.Import, import_name)

    def interpret(yuni_expr, env):
        expr_type = YuniExprType.from_string(yuni_expr["type"])
        value = yuni_expr["value"]
        if expr_type == YuniExprType.Object:
            return YuniObject.interpret(value, env)
        elif expr_type == YuniExprType.Import:
            return env.do_import(value)
        elif expr_type == YuniExprType.Invoke:
            # TODO:
            pass
        return value

class Environment:
    def __init__(self, is_master):
        self._imports = {
            "prelude": builtins,
        }
        self._objects = {}
        self._last_object_id = 0
        self.is_master = is_master

    def register_object(self, object):
        self._last_object_id += 1
        self._objects[self._last_object_id] = object
        return self._last_object_id

    def get_object(self, id):
        if self.is_master:
            return self._objects[id]
        return ObjectProxy(self, id)

    def do_import(self, name):
        if name in self._imports:
            return self._imports[name]
        # if importlib.util.find_spec(name) is not None:
        self._imports[name] =  __import__(name)
        return self._imports[name]

    def from_packet(self, packet):
        yuni_expr = json.loads(packet)
        return YuniExpr.interpret(yuni_expr, self)

    def to_packet(self, python_object):
        yuni_expr = YuniExpr.from_object_expr(python_object, self)
        return json.dumps(yuni_expr)

class ObjectProxy:
    def __init__(self, env, id):
        self.env = env
        self.id = id
