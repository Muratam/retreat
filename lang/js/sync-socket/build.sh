#!/bin/bash
# require: installed node-gyp
cd `dirname $0`
node-gyp rebuild
cd -
