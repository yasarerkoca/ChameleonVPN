#include "flutter_wireguard_plugin.h"

#include <flutter/method_channel.h>
#include <flutter/plugin_registrar_windows.h>
#include <flutter/standard_method_codec.h>
#include <flutter/event_channel.h>
#include <flutter/stream_handler_functions.h>
#include <windows.h>
#include <fstream>
#include <string>

namespace flutter_wireguard_plugin {

FlutterWireguardPlugin::FlutterWireguardPlugin() {}

FlutterWireguardPlugin::~FlutterWireguardPlugin() {}

void FlutterWireguardPlugin::RegisterWithRegistrar(
    flutter::PluginRegistrarWindows* registrar) {
  auto channel =
      std::make_unique<flutter::MethodChannel<flutter::EncodableValue>>(
          registrar->messenger(), "flutter_wireguard_plugin",
          &flutter::StandardMethodCodec::GetInstance());
  auto event_channel =
      std::make_unique<flutter::EventChannel<flutter::EncodableValue>>(
          registrar->messenger(), "flutter_wireguard_plugin/status",
          &flutter::StandardMethodCodec::GetInstance());

  auto plugin = std::make_unique<FlutterWireguardPlugin>();

  channel->SetMethodCallHandler(
      [plugin_pointer = plugin.get()](const auto& call, auto result) {
        plugin_pointer->HandleMethodCall(call, std::move(result));
      });
  event_channel->SetStreamHandler(
      std::make_unique<flutter::StreamHandlerFunctions<flutter::EncodableValue>>(
          [plugin_pointer = plugin.get()](const flutter::EncodableValue* args,
                                         std::unique_ptr<flutter::EventSink<flutter::EncodableValue>>&& events) {
            plugin_pointer->status_sink_ = std::move(events);
            plugin_pointer->SendStatus();
            return nullptr;
          },
          [plugin_pointer = plugin.get()](const flutter::EncodableValue* args) {
            plugin_pointer->status_sink_.reset();
            return nullptr;
          }));


  registrar->AddPlugin(std::move(plugin));
}

void FlutterWireguardPlugin::HandleMethodCall(
    const flutter::MethodCall<flutter::EncodableValue>& call,
    std::unique_ptr<flutter::MethodResult<flutter::EncodableValue>> result) {

  if (call.method_name().compare("getPlatformVersion") == 0) {
    result->Success(flutter::EncodableValue("Windows 10+"));
  }
  else if (call.method_name().compare("connect") == 0) {
    if (call.arguments() && call.arguments()->IsMap()) {
      auto args = std::get<flutter::EncodableMap>(*call.arguments());
      auto it = args.find(flutter::EncodableValue("config"));
      if (it != args.end()) {
        const auto& config_value = it->second;
        if (std::holds_alternative<std::string>(config_value)) {
          std::string config = std::get<std::string>(config_value);
          wchar_t temp_path[MAX_PATH];
          GetTempPathW(MAX_PATH, temp_path);
          wchar_t temp_file[MAX_PATH];
          GetTempFileNameW(temp_path, L"wg", 0, temp_file);
          std::ofstream out(temp_file);
          out << config;
          out.close();

          std::wstring command = L"wireguard.exe /installtunnelservice \"" +
                                 std::wstring(temp_file) + L"\"";
          STARTUPINFOW si{};
          si.cb = sizeof(si);
          PROCESS_INFORMATION pi{};
          bool created = CreateProcessW(nullptr, command.data(), nullptr, nullptr,
                                        FALSE, CREATE_NO_WINDOW, nullptr, nullptr,
                                        &si, &pi);
          if (created) {
            WaitForSingleObject(pi.hProcess, INFINITE);
            DWORD exit_code;
            GetExitCodeProcess(pi.hProcess, &exit_code);
            CloseHandle(pi.hProcess);
            CloseHandle(pi.hThread);
            if (exit_code == 0) {
              last_config_path_ = std::wstring(temp_file);
              is_connected_ = true;
              SendStatus();
              result->Success(flutter::EncodableValue(true));
              return;
            }
          }
          result->Success(flutter::EncodableValue(false));
          return;
        }
      }
    }
    result->Error("Bad Arguments", "Config string is missing or invalid");
  }
  else if (call.method_name().compare("disconnect") == 0) {
    if (last_config_path_.empty()) {
      result->Success(flutter::EncodableValue(false));
      return;
    }
    std::wstring command = L"wireguard.exe /uninstalltunnelservice \"" +
                           last_config_path_ + L"\"";
    STARTUPINFOW si{};
    si.cb = sizeof(si);
    PROCESS_INFORMATION pi{};
    bool created = CreateProcessW(nullptr, command.data(), nullptr, nullptr, FALSE,
                                  CREATE_NO_WINDOW, nullptr, nullptr, &si, &pi);
    if (created) {
      WaitForSingleObject(pi.hProcess, INFINITE);
      DWORD exit_code;
      GetExitCodeProcess(pi.hProcess, &exit_code);
      CloseHandle(pi.hProcess);
      CloseHandle(pi.hThread);
      last_config_path_.clear();
      is_connected_ = exit_code == 0 ? false : is_connected_;
      SendStatus();
      result->Success(flutter::EncodableValue(exit_code == 0));
    } else {
      result->Success(flutter::EncodableValue(false));
    }
  }
  else {
    result->NotImplemented();
  }
}
void FlutterWireguardPlugin::SendStatus() {
  if (status_sink_) {
    status_sink_->Success(flutter::EncodableValue(is_connected_ ? "connected" : "disconnected"));
  }
}

}  // namespace flutter_wireguard_plugin
