#include <node.h>

namespace yuni_socket {
// need
// new Socket()
// - connect(hostname: String, port: Number)
// - send(bytes: Buffer)
// - recv(size: Number) -> Buffer
// - accept() -> [socket:Socket, addr:String]
// close()

v8::Local<v8::String> CreateV8String(v8::Isolate* isolate, const char* str) {
  return v8::String::NewFromUtf8(isolate, str).ToLocalChecked();
}
void ThrowException(v8::Isolate* isolate, const char* str) {
  auto error_str = CreateV8String(isolate, str);
  auto error = v8::Exception::TypeError(error_str);
  isolate->ThrowException(error);
}
void Add(const v8::FunctionCallbackInfo<v8::Value>& args) {
  auto isolate = args.GetIsolate();
  if (args.Length() < 2) {
    ThrowException(isolate, "Wrong number of arguments");
    return;
  }
  if (!args[0]->IsNumber() || !args[1]->IsNumber()) {
    ThrowException(isolate, "Wrong arguments");
    return;
  }
  double value =
      args[0].As<v8::Number>()->Value() + args[1].As<v8::Number>()->Value();
  auto num = v8::Number::New(isolate, value);
  args.GetReturnValue().Set(num);
}
void CreateObject(const v8::FunctionCallbackInfo<v8::Value>& args) {
  auto isolate = args.GetIsolate();
  auto context = isolate->GetCurrentContext();
  auto obj = v8::Object::New(isolate);
  auto msg = CreateV8String(isolate, "msg");
  auto arg0 = args[0]->ToString(context).ToLocalChecked();
  obj->Set(context, msg, arg0).FromJust();
  args.GetReturnValue().Set(obj);
}
void MyFunction(const v8::FunctionCallbackInfo<v8::Value>& args) {
  auto isolate = args.GetIsolate();
  auto str = CreateV8String(isolate, "hello world");
  args.GetReturnValue().Set(str);
}
void CreateFunction(const v8::FunctionCallbackInfo<v8::Value>& args) {
  auto isolate = args.GetIsolate();
  auto context = isolate->GetCurrentContext();
  auto tpl = v8::FunctionTemplate::New(isolate, MyFunction);
  auto fn = tpl->GetFunction(context).ToLocalChecked();
  fn->SetName(CreateV8String(isolate, "theFunction"));
  args.GetReturnValue().Set(fn);
}

void Init(v8::Local<v8::Object> exports) {
  NODE_SET_METHOD(exports, "add", Add);
  NODE_SET_METHOD(exports, "create", CreateObject);
  NODE_SET_METHOD(exports, "func", CreateFunction);
}

NODE_MODULE(NODE_GYP_MODULE_NAME, Init)
}  // namespace yuni_socket
