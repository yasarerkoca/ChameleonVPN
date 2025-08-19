import Cocoa
import FlutterMacOS

public class FlutterWireguardPlugin: NSObject, FlutterPlugin, FlutterStreamHandler {
  private var channel: FlutterMethodChannel?
  private var eventChannel: FlutterEventChannel?
  private var statusSink: FlutterEventSink?
  private var configPath: String?
  private var isConnected = false

  public static func register(with registrar: FlutterPluginRegistrar) {
    let channel = FlutterMethodChannel(name: "flutter_wireguard_plugin", binaryMessenger: registrar.messenger)
    let eventChannel = FlutterEventChannel(name: "flutter_wireguard_plugin/status", binaryMessenger: registrar.messenger)
    let instance = FlutterWireguardPlugin()
    instance.channel = channel
    instance.eventChannel = eventChannel
    registrar.addMethodCallDelegate(instance, channel: channel)
    eventChannel.setStreamHandler(instance)
  }

  public func handle(_ call: FlutterMethodCall, result: @escaping FlutterResult) {
    switch call.method {
    case "getPlatformVersion":
      result("macOS " + ProcessInfo.processInfo.operatingSystemVersionString)
      
    case "connect":
      if let args = call.arguments as? [String: Any],
         let config = args["config"] as? String {
        let success = connectWireGuard(config: config)
        if success { statusSink?("connected") }
        result(success)
      } else {
        result(FlutterError(code: "BAD_ARGS", message: "Config param missing", details: nil))
      }
      
    case "disconnect":
      let success = disconnectWireGuard()
      if success { statusSink?("disconnected") }
      result(success)
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
      isConnected = true
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
    isConnected = false
    return process.terminationStatus == 0
  }
  public func onListen(withArguments arguments: Any?, eventSink: @escaping FlutterEventSink) -> FlutterError? {
    statusSink = eventSink
    eventSink(isConnected ? "connected" : "disconnected")
    return nil
  }

  public func onCancel(withArguments arguments: Any?) -> FlutterError? {
    statusSink = nil
    return nil
  }
}
