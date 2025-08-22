import NetworkExtension
import Network

class PacketTunnelProvider: NEPacketTunnelProvider {
  private var isTunnelStarted = false
  private var connection: NWConnection?

  override func startTunnel(options: [String : NSObject]?, completionHandler: @escaping (Error?) -> Void) {
    let providerConfig = (protocolConfiguration as? NETunnelProviderProtocol)?.providerConfiguration

    let serverAddress = options?["serverAddress"] as? String ??
      providerConfig?["serverAddress"] as? String ?? "127.0.0.1"
    let serverPort = options?["serverPort"] as? Int ??
      providerConfig?["serverPort"] as? Int ?? 443
    let localAddress = options?["localAddress"] as? String ??
      providerConfig?["localAddress"] as? String ?? "0.0.0.0"
    let subnetMask = options?["subnetMask"] as? String ??
      providerConfig?["subnetMask"] as? String ?? "255.255.255.255"
    let dnsServers = options?["dnsServers"] as? [String] ??
      providerConfig?["dnsServers"] as? [String] ?? ["8.8.8.8"]

    let settings = NEPacketTunnelNetworkSettings(tunnelRemoteAddress: serverAddress)
    let ipv4Settings = NEIPv4Settings(addresses: [localAddress], subnetMasks: [subnetMask])
    ipv4Settings.includedRoutes = [NEIPv4Route.default()]
    settings.ipv4Settings = ipv4Settings
    settings.dnsSettings = NEDNSSettings(servers: dnsServers)

    setTunnelNetworkSettings(settings) { [weak self] error in
      guard let self = self else { return }
      if let error = error {
        completionHandler(error)
        return
      }

      guard let port = NWEndpoint.Port(rawValue: UInt16(serverPort)) else {
        completionHandler(NSError(domain: NEVPNErrorDomain,
                                  code: NEVPNError.configurationInvalid.rawValue,
                                  userInfo: nil))
        return
      }

      self.connection = NWConnection(host: NWEndpoint.Host(serverAddress),
                                     port: port,
                                     using: .udp)
      self.connection?.start(queue: .main)
      self.isTunnelStarted = true
      self.readPackets()
      self.receivePackets()
      completionHandler(nil)
    }
  }

  private func readPackets() {
    guard isTunnelStarted else { return }
    packetFlow.readPackets { [weak self] packets, _ in
      guard let self = self else { return }
      for packet in packets {
        self.connection?.send(content: packet, completion: .contentProcessed { _ in })
      }
      self.readPackets()
    }
  }
  private func receivePackets() {
    connection?.receive(minimumIncompleteLength: 1, maximumLength: 65536) { [weak self] data, _, _, error in
      guard let self = self else { return }
      if let data = data {
        self.packetFlow.writePackets([data], withProtocols: [AF_INET as NSNumber])
      }
      if error == nil {
        self.receivePackets()
      }
    }
  }

  override func stopTunnel(with reason: NEProviderStopReason, completionHandler: @escaping () -> Void) {
    isTunnelStarted = false
    connection?.cancel()
    connection = nil
    completionHandler()
  }
}
