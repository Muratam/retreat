
class YuniProxyModule {
  constructor(env, hostname, port) {
    this._hostname = hostname
  }
}

if (require.main === module) {
} else {
  module.exports.py = {
    prelude: {
      print(x) { console.log(x) }
    }
  }
}
