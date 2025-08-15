#include "include/flutter_wireguard_plugin/flutter_wireguard_plugin_c_api.h"

#include <flutter/plugin_registrar_windows.h>

#include "flutter_wireguard_plugin.h"

void FlutterWireguardPluginCApiRegisterWithRegistrar(
    FlutterDesktopPluginRegistrarRef registrar) {
  flutter_wireguard_plugin::FlutterWireguardPlugin::RegisterWithRegistrar(
      flutter::PluginRegistrarManager::GetInstance()
          ->GetRegistrar<flutter::PluginRegistrarWindows>(registrar));
}
