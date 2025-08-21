import NetworkExtension

class PacketTunnelProvider: NEPacketTunnelProvider {
  private var isTunnelStarted = false

  override func startTunnel(options: [String : NSObject]?, completionHandler: @escaping (Error?) -> Void) {
    let settings = NEPacketTunnelNetworkSettings(tunnelRemoteAddress: "192.0.2.1")
    let ipv4Settings = NEIPv4Settings(addresses: ["192.0.2.2"], subnetMasks: ["255.255.255.0"])
    ipv4Settings.includedRoutes = [NEIPv4Route.default()]
    settings.ipv4Settings = ipv4Settings
    settings.dnsSettings = NEDNSSettings(servers: ["8.8.8.8"])

    setTunnelNetworkSettings(settings) { [weak self] error in
      if let error = error {
        completionHandler(error)
        return
      }

      self?.isTunnelStarted = true
      self?.readPackets()
      completionHandler(nil)
    }
  }

  private func readPackets() {
    guard isTunnelStarted else { return }
    packetFlow.readPackets { [weak self] _, _ in
      self?.readPackets()
    }

  }

  override func stopTunnel(with reason: NEProviderStopReason, completionHandler: @escaping () -> Void) {
    isTunnelStarted = false
    completionHandler()
  }
}
