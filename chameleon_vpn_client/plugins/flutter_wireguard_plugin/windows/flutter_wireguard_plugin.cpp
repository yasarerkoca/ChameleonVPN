#include "flutter_wireguard_plugin.h"

#include <flutter/method_channel.h>
#include <flutter/plugin_registrar_windows.h>
#include <flutter/standard_method_codec.h>

#include <windows.h>

namespace flutter_wireguard_plugin {

FlutterWireguardPlugin::FlutterWireguardPlugin() {}

FlutterWireguardPlugin::~FlutterWireguardPlugin() {}

void FlutterWireguardPlugin::RegisterWithRegistrar(
    flutter::PluginRegistrarWindows* registrar) {
  auto channel =
      std::make_unique<flutter::MethodChannel<flutter::EncodableValue>>(
          registrar->messenger(), "flutter_wireguard_plugin",
          &flutter::StandardMethodCodec::GetInstance());

  auto plugin = std::make_unique<FlutterWireguardPlugin>();

  channel->SetMethodCallHandler(
      [plugin_pointer = plugin.get()](const auto& call, auto result) {
        plugin_pointer->HandleMethodCall(call, std::move(result));
      });

  registrar->AddPlugin(std::move(plugin));
}

void FlutterWireguardPlugin::HandleMethodCall(
    const flutter::MethodCall<flutter::EncodableValue>& call,
    std::unique_ptr<flutter::MethodResult<flutter::EncodableValue>> result) {

  if (call.method_name().compare("getPlatformVersion") == 0) {
    result->Success(flutter::EncodableValue("Windows 10+"));
  } 
  else if (call.method_name().compare("connect") == 0) {
    // Parametreleri oku
    if (call.arguments() && call.arguments()->IsMap()) {
      auto args = std::get<flutter::EncodableMap>(*call.arguments());
      auto it = args.find(flutter::EncodableValue("config"));
      if (it != args.end()) {
        const auto& config_value = it->second;
        if (std::holds_alternative<std::string>(config_value)) {
          std::string config = std::get<std::string>(config_value);
          // TODO: WireGuard bağlantısı için native Windows API çağrısı veya WireGuard SDK kullanımı yapılacak
          // Şimdilik başarılı kabul edelim
          OutputDebugStringA(("WireGuard connect called with config:\n" + config + "\n").c_str());
          result->Success(flutter::EncodableValue(true));
          return;
        }
      }
    }
    result->Error("Bad Arguments", "Config string is missing or invalid");
  } 
  else if (call.method_name().compare("disconnect") == 0) {
    // TODO: WireGuard bağlantısını kesme işlemi yapılacak
    OutputDebugStringA("WireGuard disconnect called\n");
    result->Success(flutter::EncodableValue(true));
  } 
  else {
    result->NotImplemented();
  }
}

}  // namespace flutter_wireguard_plugin
