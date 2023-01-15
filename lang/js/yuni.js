const net = require("net")
const { setTimeout } = require('timers/promises');
class Environment {
  constructor(id) {
    // TODO:
  }
  static create_instance(id) {
    Environment.instance = new Environment(id);
  }
  set_resolver(env_id, resolver) {
    // TODO:
  }
  get_background_server_address() {
    // TODO:
    return "0000";
  }
}

class Socket {
  constructor(socket) {
    this._socket = socket;
    this._recv_queue = [];
    this._socket.on("data", data => this._recv_queue.push(data));
  }
  // FIXME: no destructor(for socket.close)
  async _recv_fixed_size(size) {
    let result = ""
    while (true) {
      if (this._recv_queue.length === 0) {
        await setTimeout(1);
        continue;
      }
      for (const recv of this._recv_queue) {
        console.log(recv);
      }
      // const size_byte_8 = parseInt(Buffer.from("あ").toString("hex"), 16)
      this._recv_queue = []
      return result;
    }
  }
  async recv() {
    const size_byte_8 = await self._recv_fixed_size(8);
    const size_byte_8_view = new DataView(size_byte_8);
    const is_little_endian = false;
    const size = size_byte_8_view.getUint32(0, is_little_endian)
    const recv_buffer = await self._recv_fixed_size(size);
    return recv_buffer.toString("utf8");
  }
  send(packet) {
    const packet_byte = Buffer.from(packet, 'utf8');
    const size = packet_byte.length();
    const size_byte_8_view = new DataView(new ArrayBuffer(8));
    const is_little_endian = false;
    size_byte_8_view.setUint32(0, size, is_little_endian);
    this._socket.write(size_byte_8_view.buffer);
    this._socket.write(packet);
  }
}

class YuniProxyModule {
  constructor(hostname, port) {
    this._hostname = hostname;
    this._port = port;
    const socket = net.connect({
      port: this._port,
      host: this._hostname,
      keepAlive: true
    });
    this._socket = new Socket(socket);
    (async () => {
      const env_id = await this._socket.recv();
      Environment.instance.set_resolver(env_id, this);
      this._socket.send(Environment.instance.get_background_server_address());
    })();
  }
  static run_main_server(hostname, port) {
    // TODO:
  }
  static run_background_server(hostname) {
    // TODO:
  }
}

Environment.create_instance(`pid:${process.pid}`)
if (require.main === module) {
  // as server
  const argv = process.argv;
  if (argv.length === 2) {
    hostname, port = argv[1].split(":");
    YuniProxyModule.run_main_server(hostname, port);
  } else {
    console.log("please specify the address");
  }
} else {
  // as module
  YuniProxyModule.run_background_server("127.0.0.1");
  module.exports.py = new YuniProxyModule("127.0.0.1", 7200);
  // js go cs cpp rs
}
