import Cocoa
import FlutterMacOS

public class FlutterWireguardPlugin: NSObject, FlutterPlugin {
  private var channel: FlutterMethodChannel?

  public static func register(with registrar: FlutterPluginRegistrar) {
    let channel = FlutterMethodChannel(name: "flutter_wireguard_plugin", binaryMessenger: registrar.messenger)
    let instance = FlutterWireguardPlugin()
    instance.channel = channel
    registrar.addMethodCallDelegate(instance, channel: channel)
  }

  public func handle(_ call: FlutterMethodCall, result: @escaping FlutterResult) {
    switch call.method {
    case "getPlatformVersion":
      result("macOS " + ProcessInfo.processInfo.operatingSystemVersionString)
      
    case "connect":
      if let args = call.arguments as? [String: Any],
         let config = args["config"] as? String {
        // TODO: WireGuard bağlantısını başlatmak için native macOS kodu yazılacak
        NSLog("WireGuard connect called with config: \(config)")
        result(true)
      } else {
        result(FlutterError(code: "BAD_ARGS", message: "Config param missing", details: nil))
      }
      
    case "disconnect":
      // TODO: WireGuard bağlantısını kesmek için native macOS kodu yazılacak
      NSLog("WireGuard disconnect called")
      result(true)
      
    default:
      result(FlutterMethodNotImplemented)
    }
  }
}
