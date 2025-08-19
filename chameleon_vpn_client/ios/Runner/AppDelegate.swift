import Flutter
import UIKit
import NetworkExtension

@main
@objc class AppDelegate: FlutterAppDelegate {
  private var vpnChannel: FlutterMethodChannel?
  override func application(
    _ application: UIApplication,
    didFinishLaunchingWithOptions launchOptions: [UIApplication.LaunchOptionsKey: Any]?
  ) -> Bool {
    let controller: FlutterViewController = window?.rootViewController as! FlutterViewController
    vpnChannel = FlutterMethodChannel(name: "chameleon_vpn/tunnel", binaryMessenger: controller.binaryMessenger)
    vpnChannel?.setMethodCallHandler { [weak self] call, result in
      switch call.method {
      case "startTunnel":
        self?.startTunnel(result: result)
      case "stopTunnel":
        self?.stopTunnel(result: result)
      default:
        result(FlutterMethodNotImplemented)
      }
    }

    NotificationCenter.default.addObserver(self,
      selector: #selector(self.vpnStatusDidChange),
      name: NSNotification.Name.NEVPNStatusDidChange,
      object: nil)

    GeneratedPluginRegistrant.register(with: self)
    return super.application(application, didFinishLaunchingWithOptions: launchOptions)
  }

  @objc private func vpnStatusDidChange() {
    let status = NEVPNManager.shared().connection.status.rawValue
    vpnChannel?.invokeMethod("onStatusChanged", arguments: status)
  }

  private func startTunnel(result: @escaping FlutterResult) {
    NETunnelProviderManager.loadAllFromPreferences { [weak self] managers, error in
      if let error = error {
        self?.vpnChannel?.invokeMethod("onError", arguments: error.localizedDescription)
        result(FlutterError(code: "load_failed", message: error.localizedDescription, details: nil))
        return
      }
      let manager = managers?.first ?? NETunnelProviderManager()
      manager.protocolConfiguration = NETunnelProviderProtocol()
      manager.isEnabled = true
      manager.saveToPreferences { saveError in
        if let saveError = saveError {
          self?.vpnChannel?.invokeMethod("onError", arguments: saveError.localizedDescription)
          result(FlutterError(code: "save_failed", message: saveError.localizedDescription, details: nil))
          return
        }
        do {
          try manager.connection.startVPNTunnel()
          result(nil)
        } catch {
          self?.vpnChannel?.invokeMethod("onError", arguments: error.localizedDescription)
          result(FlutterError(code: "start_failed", message: error.localizedDescription, details: nil))
        }
      }
    }
  }

  private func stopTunnel(result: @escaping FlutterResult) {
    NETunnelProviderManager.loadAllFromPreferences { managers, _ in
      if let manager = managers?.first {
        manager.connection.stopVPNTunnel()
      }
      result(nil)
    }
  }
}
