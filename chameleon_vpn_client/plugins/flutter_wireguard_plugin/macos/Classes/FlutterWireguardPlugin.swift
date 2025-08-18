import Cocoa
import FlutterMacOS

public class FlutterWireguardPlugin: NSObject, FlutterPlugin {
  private var channel: FlutterMethodChannel?
  private var configPath: String?

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
        result(connectWireGuard(config: config))
      } else {
        result(FlutterError(code: "BAD_ARGS", message: "Config param missing", details: nil))
      }
      
    case "disconnect":
      result(disconnectWireGuard())      
    default:
      result(FlutterMethodNotImplemented)
    }
  }
  private func connectWireGuard(config: String) -> Bool {
    let tempURL = FileManager.default.temporaryDirectory.appendingPathComponent("wg.conf")
    do {
      try config.write(to: tempURL, atomically: true, encoding: .utf8)
    } catch {
      NSLog("Failed to write config: \(error)")
      return false
    }
    let process = Process()
    process.launchPath = "/usr/local/bin/wg-quick"
    process.arguments = ["up", tempURL.path]
    process.launch()
    process.waitUntilExit()
    if process.terminationStatus == 0 {
      configPath = tempURL.path
      return true
    }
    return false
  }

  private func disconnectWireGuard() -> Bool {
    guard let path = configPath else { return false }
    let process = Process()
    process.launchPath = "/usr/local/bin/wg-quick"
    process.arguments = ["down", path]
    process.launch()
    process.waitUntilExit()
    configPath = nil
    return process.terminationStatus == 0
  }
}
