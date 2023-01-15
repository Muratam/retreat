class Environment {
  constructor(id) {
    // TODO:
  }
}

class YuniProxyModule {
  constructor(env, hostname, port) {
    this._hostname = hostname;
    this._port = port;
    this._env = env;
    // TODO:
  }
  static run_background_server(env, hostname) {
    // TODO:
  }
}

if (require.main === module) {
  // as server

} else {
  // as module
  YuniProxyModule.run_background_server(env, "127.0.0.1")
  module.exports.py = new YuniProxyModule(env, "127.0.0.1", 7200);
  // js go cs cpp rs
}
