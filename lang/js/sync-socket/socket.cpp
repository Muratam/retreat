#include <node.h>

namespace yuni_socket {

// need
// new Socket()
// - connect(hostname: String, port: Number)
// - send(bytes: Buffer)
// - recv(size: Number) -> Buffer
// - accept() -> [socket:Socket, addr:String]
// close()

void Add(const v8::FunctionCallbackInfo<v8::Value>& args) {
  v8::Isolate* isolate = args.GetIsolate();

  // Check the number of arguments passed.
  if (args.Length() < 2) {
    // Throw an Error that is passed back to JavaScript
    isolate->ThrowException(v8::Exception::TypeError(
        v8::String::NewFromUtf8(isolate, "Wrong number of arguments")
            .ToLocalChecked()));
    return;
  }

  // Check the argument types
  if (!args[0]->IsNumber() || !args[1]->IsNumber()) {
    isolate->ThrowException(v8::Exception::TypeError(
        v8::String::NewFromUtf8(isolate, "Wrong arguments").ToLocalChecked()));
    return;
  }

  // Perform the operation
  double value =
      args[0].As<v8::Number>()->Value() + args[1].As<v8::Number>()->Value();
  v8::Local<v8::Number> num = v8::Number::New(isolate, value);

  // Set the return value (using the passed in
  // FunctionCallbackInfo<Value>&)
  args.GetReturnValue().Set(num);
}
void CreateObject(const v8::FunctionCallbackInfo<v8::Value>& args) {
  v8::Isolate* isolate = args.GetIsolate();
  v8::Local<v8::Context> context = isolate->GetCurrentContext();

  v8::Local<v8::Object> obj = v8::Object::New(isolate);
  obj->Set(context, v8::String::NewFromUtf8(isolate, "msg").ToLocalChecked(),
           args[0]->ToString(context).ToLocalChecked())
      .FromJust();

  args.GetReturnValue().Set(obj);
}
void MyFunction(const v8::FunctionCallbackInfo<v8::Value>& args) {
  auto isolate = args.GetIsolate();
  args.GetReturnValue().Set(
      v8::String::NewFromUtf8(isolate, "hello world").ToLocalChecked());
}
void CreateFunction(const v8::FunctionCallbackInfo<v8::Value>& args) {
  auto isolate = args.GetIsolate();

  v8::Local<v8::Context> context = isolate->GetCurrentContext();
  v8::Local<v8::FunctionTemplate> tpl =
      v8::FunctionTemplate::New(isolate, MyFunction);
  v8::Local<v8::Function> fn = tpl->GetFunction(context).ToLocalChecked();

  // omit this to make it anonymous
  fn->SetName(v8::String::NewFromUtf8(isolate, "theFunction").ToLocalChecked());

  args.GetReturnValue().Set(fn);
}

void Init(v8::Local<v8::Object> exports) {
  NODE_SET_METHOD(exports, "add", Add);
  NODE_SET_METHOD(exports, "create", CreateObject);
  NODE_SET_METHOD(exports, "func", CreateFunction);
}

NODE_MODULE(NODE_GYP_MODULE_NAME, Init)

}  // namespace yuni_socket
