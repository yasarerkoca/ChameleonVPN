import Flutter
import UIKit
import NetworkExtension

public class FlutterWireguardPlugin: NSObject, FlutterPlugin, FlutterStreamHandler {
  private var isConnected = false
  private var manager: NETunnelProviderManager?
  private var eventSink: FlutterEventSink?

  public static func register(with registrar: FlutterPluginRegistrar) {
    let channel = FlutterMethodChannel(name: "flutter_wireguard_plugin", binaryMessenger: registrar.messenger())
    let eventChannel = FlutterEventChannel(name: "flutter_wireguard_plugin/status", binaryMessenger: registrar.messenger())
    let instance = FlutterWireguardPlugin()
    registrar.addMethodCallDelegate(instance, channel: channel)
    eventChannel.setStreamHandler(instance)
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
      if success { eventSink?("connected") }
      result(success)

    case "disconnect":
      let success = disconnectWireGuard()
      if success { eventSink?("disconnected") }
      result(success)

    default:
      result(FlutterMethodNotImplemented)
    }
  }

  public func onListen(withArguments arguments: Any?, eventSink: @escaping FlutterEventSink) -> FlutterError? {
    self.eventSink = eventSink
    eventSink(isConnected ? "connected" : "disconnected")
    return nil
  }

  public func onCancel(withArguments arguments: Any?) -> FlutterError? {
    eventSink = nil
    return nil
  }

  private func connectWireGuard(config: String) -> Bool {
    var success = false
    let semaphore = DispatchSemaphore(value: 0)
    let mgr = NETunnelProviderManager()
    mgr.loadFromPreferences { error in
      if let error = error {
        NSLog("Error loading preferences: \(error)")
        semaphore.signal()
        return
      }

      let proto = NETunnelProviderProtocol()
      proto.providerBundleIdentifier = "com.example.wireguard.extension"
      proto.providerConfiguration = ["config": config]
      proto.serverAddress = "WireGuard"
      mgr.protocolConfiguration = proto
      mgr.localizedDescription = "WireGuard"
      mgr.isEnabled = true
      mgr.saveToPreferences { error in
        if let error = error {
          NSLog("Error saving preferences: \(error)")
          semaphore.signal()
          return
        }
        do {
          try mgr.connection.startVPNTunnel()
          self.manager = mgr
          self.isConnected = true
          success = true
        } catch {
          NSLog("Failed to start tunnel: \(error)")
        }
        semaphore.signal()
      }
    }
    _ = semaphore.wait(timeout: .now() + 10)
    return success
  }

  private func disconnectWireGuard() -> Bool {
    if let mgr = manager {
      mgr.connection.stopVPNTunnel()
      manager = nil
      isConnected = false
      return true
    }
    return false
  }
}
