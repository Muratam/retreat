import json
from enum import Enum, auto
from types import ModuleType
import importlib
import builtins

class PacketType(Enum):
    Primitive = auto()
    Object = auto()
    Call = auto()
    Import = auto()
    StdOut = auto()
    Undefined = auto()
    def to_string(self):
        for pair in _packet_type_pair:
            if pair[0] == self:
                return pair[1]
        return ""
    def from_string(str):
        for pair in _packet_type_pair:
            if pair[1] == str:
                return pair[0]
        return PacketType.Undefined
_packet_type_pair = [
    (PacketType.Primitive, "primitive"),
    (PacketType.Object, "object"),
    (PacketType.Call, "call"),
    (PacketType.Import, "import"),
    (PacketType.StdOut, "stdout"),
]

class Packet:
    def _to_packet_str(packet_type, value):
        return json.dumps({
            "packet_type": packet_type.to_string(),
            "value": value
        })
    def by_primitive(primitive):
        return Packet._to_packet_str(PacketType.Primitive, primitive)

    def by_import_statement(import_name):
        # hoge.fuga.piyo のように指定
        # 返却されるものは module だったり primitive だったり何でもありうる
        return Packet._to_packet_str(PacketType.Import, import_name)

    def by_object(object):
        return Packet._to_packet_str(PacketType.Object, object)

    def by_python_object(object, env):
        type_object = type(object)
        if (type_object is int) or (
            type_object is float) or (
            type_object is str) or (
            type_object is bool) or (
            type_object == None):
            return Packet.by_primitive(object)
        # TODO: array / object
        if isinstance(object, ModuleType):
            return Packet.by_primitive(f"imported {object.__name__}")
        print(object, "not found")
        return Packet.by_primitive(None)


class Environment:
    def __init__(self):
        self.imports = {
            "prelude": builtins,
        }

    # -> Python Object
    def parse(self, packet_str):
        packet = json.loads(packet_str)
        packet_type = PacketType.from_string(packet["packet_type"])
        value = packet["value"]
        if packet_type == PacketType.Primitive:
            return value
        elif packet_type == PacketType.Import:
            assert(type(value) is str)
            if value in self.imports:
                return self.imports[value]
            # if importlib.util.find_spec(value) is not None:
            self.imports[value] =  __import__(value)
            return self.imports[value]
        return value
