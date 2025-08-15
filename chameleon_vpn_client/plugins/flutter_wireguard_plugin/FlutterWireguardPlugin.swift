import Flutter
import UIKit

public class FlutterWireguardPlugin: NSObject, FlutterPlugin {
  public static func register(with registrar: FlutterPluginRegistrar) {
    let channel = FlutterMethodChannel(name: "flutter_wireguard_plugin", binaryMessenger: registrar.messenger())
    let instance = FlutterWireguardPlugin()
    registrar.addMethodCallDelegate(instance, channel: channel)
  }

  public func handle(_ call: FlutterMethodCall, result: @escaping FlutterResult) {
    switch call.method {
    case "connect":
      if let args = call.arguments as? [String: Any], let config = args["config"] as? String {
        // TODO: WireGuard bağlantısını iOS tarafında native yap
        result("WireGuard bağlantısı başarılı (simüle)")
      } else {
        result(FlutterError(code: "INVALID_ARGUMENT", message: "Config parametresi eksik", details: nil))
      }
    default:
      result(FlutterMethodNotImplemented)
    }
  }
}
