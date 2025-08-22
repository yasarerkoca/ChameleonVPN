# Packet Tunnel Manual Testing

The Packet Tunnel extension can be verified manually on an iOS simulator or device.

1. Open `chameleon_vpn_client/ios` in Xcode.
2. Select the *PacketTunnel* extension target.
3. Configure the `NETunnelProviderProtocol` with a valid server address, port,
   local address and DNS servers. These values may be supplied by the backend or
   stored in user settings.
4. Build and run the host application on a simulator or device.
5. Start the VPN connection and verify in the Xcode logs that packets are
   forwarded to the configured VPN server.
6. Stop the VPN connection and ensure the interface and network connection are
   removed without errors.
These steps confirm that the tunnel uses dynamic configuration and forwards
traffic to the remote server while starting and stopping cleanly.
