class Environment {
  constructor(id) {
    // TODO:
  }
  static create_instance(id) {
    // TODO:
  }
}

class YuniProxyModule {
  constructor(env, hostname, port) {
    this._hostname = hostname
    this._port = port
    this._env = env
    // TODO:
  }
  static run_main_server(hostname, port) {
    // TODO:
  }
  static run_background_server(env, hostname) {
    // TODO:
  }
}

Environment.create_instance(`pid:${process.pid}`)
if (require.main === module) {
  // as server
  const argv = process.argv
  if (argv.length === 2) {
    hostname, port = argv[1].split(":")
    YuniProxyModule.run_main_server(hostname, port)
  } else {
    console.log("please specify the address")
  }
} else {
  // as module
  YuniProxyModule.run_background_server("127.0.0.1")
  module.exports.py = new YuniProxyModule("127.0.0.1", 7200)
  // js go cs cpp rs
}
