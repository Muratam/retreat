import json
from enum import Enum, auto
import importlib
import builtins

class YuniObjectType(Enum):
    Primitive = auto()
    Array = auto()
    Table = auto()
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
        return YuniObject._pack(YuniObjectType.Object, env.register_object(object))

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
            return env.get_object(value["obj_id"], value["env_id"])
        print(yuni_object, "not found")
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

    # TODO:
    # def from_invoke_expr(object, args, options):
    #     return YuniExpr._pack(YuniExprType.Invoke, {
    #         "object": object,
    #         "args": args,
    #         "options": options,
    #     })

    def interpret(yuni_expr, env):
        expr_type = YuniExprType.from_string(yuni_expr["type"])
        value = yuni_expr["value"]
        if expr_type == YuniExprType.GetEnvId:
            return env.id
        elif expr_type == YuniExprType.Object:
            return YuniObject.interpret(value, env)
        elif expr_type == YuniExprType.Import:
            return env.do_import(value)
        elif expr_type == YuniExprType.GetAttr:
            object = YuniObject.interpret(value["object"], env)
            attr_name = value["attr_name"]
            print(object, attr_name)
            return object.__getattribute__(attr_name)
        # TODO:
        # elif expr_type == YuniExprType.Invoke:
        #     object = env.get_object()
        return value

class LocalResolver:
    def __init__(self, env):
        self.env = env

    def call_get_attr(self, object_proxy, name):
        object = self.env.get_object(object_proxy.obj_id, object_proxy.env_id)
        return object.__get_attr__(name)
    # TODO:
    # def call_invoke(self, object_proxy, name):
    #     object = self.env.get_object(object_proxy.obj_id, object_proxy.env_id)
    #     return object.__get_attr__(name)

class Environment:
    def __init__(self, id):
        self._imports = {
            "prelude": builtins,
        }
        self._objects = {}
        self._last_obj_id = 0
        self.id = id
        self.resolver_by_env_id = {
            id: LocalResolver(self)
        }

    def register_object(self, object):
        if isinstance(object, ObjectProxy):
            return {
                "obj_id": object.obj_id,
                "env_id": object.env_id
            }
        # FIXME: [A , A] のようになったときに、二重登録してしまうので治す
        # FIXME: object の 削除もできればしておきたい
        self._last_obj_id += 1
        self._objects[self._last_obj_id] = object
        return {
            "obj_id": self._last_obj_id,
            "env_id": self.id
        }

    def get_object(self, obj_id, env_id):
        if self.id == env_id:
            return self._objects[obj_id]
        return ObjectProxy(obj_id, env_id, self)

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

    def __str__(self):
        return f"{22}"

    def __repr__(self):
        return f"{11}"

class ObjectProxy:
    # TODO: エラーを見やすいようにOptionalで設定する
    def __init__(self, obj_id, env_id, env):
        self.obj_id = obj_id
        self.env_id = env_id
        self.env = env
    def __del__(self):
        # FIXME:
        pass

    # str
    def __str__(self):
        return f"Proxy Object {self.obj_id} @ {self.env_id}"
    def __repr__(self):
        return self.__str__(self)

    # eq
    def __eq__(self, __o):
        if not isinstance(__o, ObjectProxy):
            return False
        return self.obj_id == __o.obj_id and self.env_id == __o.env_id
    def __ne__(self, __o):
        return not self.__eq__(__o)

    # attr
    def __getattr__(self, __name):
        return self.env.resolver_by_env_id[self.env_id].call_get_attr(self, __name)
    # def __call__(self, *args: Any, **kwds: Any) -> Any:
    #     pass
    # def __dir__(self) -> Iterable[str]:
    #     pass
    # operators
    # container
    # __getitem__ / __setitem__ / __delitem__ / __contains__
    # numbers
    # __add__ / __sub__ / __mul__ ...
