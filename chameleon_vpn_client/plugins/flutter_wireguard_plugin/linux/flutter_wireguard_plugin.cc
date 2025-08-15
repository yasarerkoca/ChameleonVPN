#include "include/flutter_wireguard_plugin/flutter_wireguard_plugin.h"

#include <flutter_linux/flutter_linux.h>
#include <gtk/gtk.h>
#include <sys/utsname.h>

#include <cstring>

#include "flutter_wireguard_plugin_private.h"

#define FLUTTER_WIREGUARD_PLUGIN(obj) \
  (G_TYPE_CHECK_INSTANCE_CAST((obj), flutter_wireguard_plugin_get_type(), \
                              FlutterWireguardPlugin))

struct _FlutterWireguardPlugin {
  GObject parent_instance;
};

G_DEFINE_TYPE(FlutterWireguardPlugin, flutter_wireguard_plugin, g_object_get_type())

// Forward declaration
static FlMethodResponse* get_platform_version();
static FlMethodResponse* handle_connect(FlutterWireguardPlugin* self, FlMethodCall* method_call);
static FlMethodResponse* handle_disconnect(FlutterWireguardPlugin* self);

// Called when a method call is received from Flutter.
static void flutter_wireguard_plugin_handle_method_call(
    FlutterWireguardPlugin* self,
    FlMethodCall* method_call) {
  g_autoptr(FlMethodResponse) response = nullptr;

  const gchar* method = fl_method_call_get_name(method_call);

  if (strcmp(method, "getPlatformVersion") == 0) {
    response = get_platform_version();
  } else if (strcmp(method, "connect") == 0) {
    response = handle_connect(self, method_call);
  } else if (strcmp(method, "disconnect") == 0) {
    response = handle_disconnect(self);
  } else {
    response = FL_METHOD_RESPONSE(fl_method_not_implemented_response_new());
  }

  fl_method_call_respond(method_call, response, nullptr);
}

// getPlatformVersion method implementation
FlMethodResponse* get_platform_version() {
  struct utsname uname_data = {};
  uname(&uname_data);
  g_autofree gchar *version = g_strdup_printf("Linux %s", uname_data.version);
  g_autoptr(FlValue) result = fl_value_new_string(version);
  return FL_METHOD_RESPONSE(fl_method_success_response_new(result));
}

// connect method implementation - örnek placeholder
FlMethodResponse* handle_connect(FlutterWireguardPlugin* self, FlMethodCall* method_call) {
  // Parametreleri al (config string)
  g_autoptr(FlValue) args = fl_method_call_get_args(method_call);
  const gchar* config = nullptr;

  if (args != nullptr && fl_value_get_type(args) == FL_VALUE_TYPE_MAP) {
    FlValue* config_value = fl_value_lookup_string(args, "config");
    if (config_value != nullptr && fl_value_get_type(config_value) == FL_VALUE_TYPE_STRING) {
      config = fl_value_get_string(config_value);
    }
  }

  // Burada gerçek WireGuard bağlantısı yapılmalı
  // Şimdilik sadece başarılı dönüş yapıyoruz.
  g_print("WireGuard connect called with config:\n%s\n", config ? config : "null");

  FlValue* result = fl_value_new_bool(TRUE); // Başarılı kabul
  return FL_METHOD_RESPONSE(fl_method_success_response_new(result));
}

// disconnect method implementation - örnek placeholder
FlMethodResponse* handle_disconnect(FlutterWireguardPlugin* self) {
  // Burada gerçek WireGuard bağlantısı sonlandırılmalı
  g_print("WireGuard disconnect called\n");

  FlValue* result = fl_value_new_bool(TRUE); // Başarılı kabul
  return FL_METHOD_RESPONSE(fl_method_success_response_new(result));
}

static void flutter_wireguard_plugin_dispose(GObject* object) {
  G_OBJECT_CLASS(flutter_wireguard_plugin_parent_class)->dispose(object);
}

static void flutter_wireguard_plugin_class_init(FlutterWireguardPluginClass* klass) {
  G_OBJECT_CLASS(klass)->dispose = flutter_wireguard_plugin_dispose;
}
static void flutter_wireguard_plugin_init(FlutterWireguardPlugin* self) {}

static void method_call_cb(FlMethodChannel* channel, FlMethodCall* method_call,
                           gpointer user_data) {
  FlutterWireguardPlugin* plugin = FLUTTER_WIREGUARD_PLUGIN(user_data);
  flutter_wireguard_plugin_handle_method_call(plugin, method_call);
}

void flutter_wireguard_plugin_register_with_registrar(FlPluginRegistrar* registrar) {
  FlutterWireguardPlugin* plugin = FLUTTER_WIREGUARD_PLUGIN(
      g_object_new(flutter_wireguard_plugin_get_type(), nullptr));

  g_autoptr(FlStandardMethodCodec) codec = fl_standard_method_codec_new();
  g_autoptr(FlMethodChannel) channel =
      fl_method_channel_new(fl_plugin_registrar_get_messenger(registrar),
                            "flutter_wireguard_plugin",
                            FL_METHOD_CODEC(codec));
  fl_method_channel_set_method_call_handler(channel, method_call_cb,
                                            g_object_ref(plugin),
                                            g_object_unref);

  g_object_unref(plugin);
}
