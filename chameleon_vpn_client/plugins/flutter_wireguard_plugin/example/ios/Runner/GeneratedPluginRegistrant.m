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

#if __has_include(<integration_test/IntegrationTestPlugin.h>)
#import <integration_test/IntegrationTestPlugin.h>
#else
@import integration_test;
#endif

@implementation GeneratedPluginRegistrant

+ (void)registerWithRegistry:(NSObject<FlutterPluginRegistry>*)registry {
  [FlutterWireguardPlugin registerWithRegistrar:[registry registrarForPlugin:@"FlutterWireguardPlugin"]];
  [IntegrationTestPlugin registerWithRegistrar:[registry registrarForPlugin:@"IntegrationTestPlugin"]];
}

@end
