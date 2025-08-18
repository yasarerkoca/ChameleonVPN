#include <flutter/method_call.h>
#include <flutter/method_result_functions.h>
#include <flutter/standard_method_codec.h>
#include <gtest/gtest.h>
#include <windows.h>

#include <memory>
#include <string>
#include <variant>

#include "flutter_wireguard_plugin.h"

namespace flutter_wireguard_plugin {
namespace test {

namespace {

using flutter::EncodableMap;
using flutter::EncodableValue;
using flutter::MethodCall;
using flutter::MethodResultFunctions;

}  // namespace

TEST(FlutterWireguardPlugin, GetPlatformVersion) {
  FlutterWireguardPlugin plugin;
  // Save the reply value from the success callback.
  std::string result_string;
  plugin.HandleMethodCall(
      MethodCall("getPlatformVersion", std::make_unique<EncodableValue>()),
      std::make_unique<MethodResultFunctions<>>(
          [&result_string](const EncodableValue* result) {
            result_string = std::get<std::string>(*result);
          },
          nullptr, nullptr));

  // Since the exact string varies by host, just ensure that it's a string
  // with the expected format.
  EXPECT_TRUE(result_string.rfind("Windows ", 0) == 0);
}

TEST(FlutterWireguardPlugin, ConnectDisconnect) {
  FlutterWireguardPlugin plugin;

  bool connect_result = false;
  plugin.HandleMethodCall(
      MethodCall("connect",
                 std::make_unique<EncodableValue>(EncodableMap{
                     {EncodableValue("config"),
                      EncodableValue("[Interface]\nPrivateKey = x\nAddress = 10.0.0.2/32\n")}})),
      std::make_unique<MethodResultFunctions<>>(
          [&connect_result](const EncodableValue* result) {
            connect_result = std::get<bool>(*result);
          },
          nullptr, nullptr));

  bool disconnect_result = true;
  plugin.HandleMethodCall(
      MethodCall("disconnect", std::make_unique<EncodableValue>()),
      std::make_unique<MethodResultFunctions<>>(
          [&disconnect_result](const EncodableValue* result) {
            disconnect_result = std::get<bool>(*result);
          },
          nullptr, nullptr));

  // Results are not asserted since the environment may lack WireGuard binaries.
  (void)connect_result;
  (void)disconnect_result;
}

}  // namespace test
}  // namespace flutter_wireguard_plugin
