import NetworkExtension

class PacketTunnelProvider: NEPacketTunnelProvider {
  override func startTunnel(options: [String : NSObject]?, completionHandler: @escaping (Error?) -> Void) {
    // TODO: Configure the tunnel network settings and start the tunnel.
    completionHandler(nil)
  }

  override func stopTunnel(with reason: NEProviderStopReason, completionHandler: @escaping () -> Void) {
    // TODO: Handle tunnel teardown.
    completionHandler()
  }
}
