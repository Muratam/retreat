import json
# Object
# import <module-name>
#

def to_packet(content):
    packet_type = "primitive"
    value = content
    packet = {"packet_type": packet_type, "value": value}
    return json.dumps(packet)


def call_packet(packet_json):
    packet = json.loads(packet_json)
    packet_type = packet["packet_type"]
    value = packet["value"]
    if packet_type == "primitive":
        return value
    return value
