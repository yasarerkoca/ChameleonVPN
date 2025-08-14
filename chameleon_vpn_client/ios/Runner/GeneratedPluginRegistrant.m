//
//  Generated file. Do not edit.
//

// clang-format off

#import "GeneratedPluginRegistrant.h"

#if __has_include(<flutter_wireguard_plugin/FlutterWireguardPlugin.h>)
#import <flutter_wireguard_plugin/FlutterWireguardPlugin.h>
#else
@import flutter_wireguard_plugin;
#endif

#if __has_include(<openvpn_flutter/OpenVPNFlutterPlugin.h>)
#import <openvpn_flutter/OpenVPNFlutterPlugin.h>
#else
@import openvpn_flutter;
#endif

@implementation GeneratedPluginRegistrant

+ (void)registerWithRegistry:(NSObject<FlutterPluginRegistry>*)registry {
  [FlutterWireguardPlugin registerWithRegistrar:[registry registrarForPlugin:@"FlutterWireguardPlugin"]];
  [OpenVPNFlutterPlugin registerWithRegistrar:[registry registrarForPlugin:@"OpenVPNFlutterPlugin"]];
}

@end
