#ifndef FLUTTER_PLUGIN_FLUTTER_WIREGUARD_PLUGIN_H_
#define FLUTTER_PLUGIN_FLUTTER_WIREGUARD_PLUGIN_H_

#include <flutter/method_channel.h>
#include <flutter/plugin_registrar_windows.h>
#include <flutter/standard_method_codec.h>

#include <memory>

namespace flutter_wireguard_plugin {

class FlutterWireguardPlugin : public flutter::Plugin {
 public:
  static void RegisterWithRegistrar(flutter::PluginRegistrarWindows *registrar);

  FlutterWireguardPlugin();

  virtual ~FlutterWireguardPlugin();

  // Disallow copy and assign.
  FlutterWireguardPlugin(const FlutterWireguardPlugin&) = delete;
  FlutterWireguardPlugin& operator=(const FlutterWireguardPlugin&) = delete;

 private:
  // Called when a method is called on plugin channel.
  void HandleMethodCall(
      const flutter::MethodCall<flutter::EncodableValue>& call,
      std::unique_ptr<flutter::MethodResult<flutter::EncodableValue>> result);
};

}  // namespace flutter_wireguard_plugin

#endif  // FLUTTER_PLUGIN_FLUTTER_WIREGUARD_PLUGIN_H_
