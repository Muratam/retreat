#include <node.h>
#include <v8.h>

using namespace node;
using namespace v8;

void Method(const FunctionCallbackInfo<Value>& args) {
  Isolate* isolate = args.GetIsolate();
  HandleScope scope(isolate);
  Local<v8::String> result;
  MaybeLocal<v8::String> str = String::NewFromUtf8(isolate, "Hello World!");
  str.ToLocal(&result);
  args.GetReturnValue().Set(result);
}

void init(Local<Object> exports) { NODE_SET_METHOD(exports, "hello", Method); }

NODE_MODULE(NODE_GYP_MODULE_NAME, init)
