# Packet Tunnel Manual Testing

The Packet Tunnel extension can be verified manually on an iOS simulator or device.

1. Open `chameleon_vpn_client/ios` in Xcode.
2. Select the *PacketTunnel* extension target.
3. Build and run the host application on a simulator or device.
4. Start the VPN connection; the extension configures the interface with IP `192.0.2.2` and default routes.
5. Observe Xcode logs to confirm packets are received.
6. Stop the VPN connection and ensure the interface is removed without errors.

These steps confirm that the tunnel can start and stop cleanly.
