import Flutter
import UIKit

public class FlutterWireguardPlugin: NSObject, FlutterPlugin {
  private var isConnected = false

  public static func register(with registrar: FlutterPluginRegistrar) {
    let channel = FlutterMethodChannel(name: "flutter_wireguard_plugin", binaryMessenger: registrar.messenger())
    let instance = FlutterWireguardPlugin()
    registrar.addMethodCallDelegate(instance, channel: channel)
  }

  public func handle(_ call: FlutterMethodCall, result: @escaping FlutterResult) {
    switch call.method {
    case "getPlatformVersion":
      result("iOS " + UIDevice.current.systemVersion)

    case "connect":
      guard let args = call.arguments as? [String: Any],
            let config = args["config"] as? String else {
        result(FlutterError(code: "INVALID_ARGUMENT", message: "Config parameter missing", details: nil))
        return
      }
      let success = connectWireGuard(config: config)
      result(success)

    case "disconnect":
      let success = disconnectWireGuard()
      result(success)

    default:
      result(FlutterMethodNotImplemented)
    }
  }

  // TODO: Gerçek WireGuard bağlantısını başlatmak için native iOS kodunu buraya yaz
  private func connectWireGuard(config: String) -> Bool {
    // Şimdilik sadece dummy olarak true döndürüyoruz
    // Burada WireGuard SDK veya sistem çağrısı ile bağlantıyı başlatabilirsin
    isConnected = true
    return true
  }

  // TODO: WireGuard bağlantısını kesmek için native iOS kodunu buraya yaz
  private func disconnectWireGuard() -> Bool {
    // Bağlantıyı kesmek için gerçek kod burada olacak
    isConnected = false
    return true
  }
}
