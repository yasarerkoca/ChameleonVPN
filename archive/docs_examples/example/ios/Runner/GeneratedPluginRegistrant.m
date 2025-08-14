//
//  Generated file. Do not edit.
//

// clang-format off

#import "GeneratedPluginRegistrant.h"

#if __has_include(<integration_test/IntegrationTestPlugin.h>)
#import <integration_test/IntegrationTestPlugin.h>
#else
@import integration_test;
#endif

#if __has_include(<yasarerkoca/YasarerkocaPlugin.h>)
#import <yasarerkoca/YasarerkocaPlugin.h>
#else
@import yasarerkoca;
#endif

@implementation GeneratedPluginRegistrant

+ (void)registerWithRegistry:(NSObject<FlutterPluginRegistry>*)registry {
  [IntegrationTestPlugin registerWithRegistrar:[registry registrarForPlugin:@"IntegrationTestPlugin"]];
  [YasarerkocaPlugin registerWithRegistrar:[registry registrarForPlugin:@"YasarerkocaPlugin"]];
}

@end
