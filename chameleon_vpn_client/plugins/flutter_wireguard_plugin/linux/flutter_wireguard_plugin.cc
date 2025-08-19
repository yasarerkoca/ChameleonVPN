#include "include/flutter_wireguard_plugin/flutter_wireguard_plugin.h"

#include <flutter_linux/flutter_linux.h>
#include <gtk/gtk.h>
#include <sys/utsname.h>
#include <unistd.h>
#include <cstdio>
#include <cstdlib>
#include <cstring>

#include "flutter_wireguard_plugin_private.h"

#define FLUTTER_WIREGUARD_PLUGIN(obj) \
  (G_TYPE_CHECK_INSTANCE_CAST((obj), flutter_wireguard_plugin_get_type(), \
                              FlutterWireguardPlugin))

struct _FlutterWireguardPlugin {
  GObject parent_instance;
};

static gchar* last_config_path = NULL;
static bool is_connected = false;
static FlEventSink* status_sink = NULL;

G_DEFINE_TYPE(FlutterWireguardPlugin, flutter_wireguard_plugin, g_object_get_type())

// Forward declaration
static FlMethodResponse* get_platform_version();
static FlMethodResponse* handle_connect(FlutterWireguardPlugin* self, FlMethodCall* method_call);
static FlMethodResponse* handle_disconnect(FlutterWireguardPlugin* self);
static void send_status();

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

// send current status to stream
static void send_status() {
  if (status_sink != NULL) {
    FlValue* status = fl_value_new_string(is_connected ? "connected" : "disconnected");
    fl_event_sink_send(status_sink, status, NULL);
  }
}

// connect method implementation

FlMethodResponse* handle_connect(FlutterWireguardPlugin* self, FlMethodCall* method_call) {
  g_autoptr(FlValue) args = fl_method_call_get_args(method_call);
  const gchar* config = nullptr;
  if (args != nullptr && fl_value_get_type(args) == FL_VALUE_TYPE_MAP) {
    FlValue* config_value = fl_value_lookup_string(args, "config");
    if (config_value != nullptr && fl_value_get_type(config_value) == FL_VALUE_TYPE_STRING) {
      config = fl_value_get_string(config_value);
    }
  }
  if (config == nullptr) {
    FlValue* result = fl_value_new_bool(FALSE);
    return FL_METHOD_RESPONSE(fl_method_success_response_new(result));
  }

  gchar template_path[] = "/tmp/wgXXXXXX.conf";
  int fd = mkstemps(template_path, 5);
  if (fd == -1) {
    FlValue* result = fl_value_new_bool(FALSE);
    return FL_METHOD_RESPONSE(fl_method_success_response_new(result));
  }
  write(fd, config, strlen(config));
  close(fd);

  gchar* command = g_strdup_printf("wg-quick up %s", template_path);
  int ret = system(command);
  g_free(command);
  if (ret == 0) {
    last_config_path = g_strdup(template_path);
    is_connected = true;
    send_status();
    FlValue* result = fl_value_new_bool(TRUE);
    return FL_METHOD_RESPONSE(fl_method_success_response_new(result));
  }
  unlink(template_path);
  FlValue* result = fl_value_new_bool(FALSE);

  return FL_METHOD_RESPONSE(fl_method_success_response_new(result));
}

// disconnect method implementation
FlMethodResponse* handle_disconnect(FlutterWireguardPlugin* self) {
  if (last_config_path == NULL) {
    FlValue* result = fl_value_new_bool(FALSE);
    return FL_METHOD_RESPONSE(fl_method_success_response_new(result));
  }
  gchar* command = g_strdup_printf("wg-quick down %s", last_config_path);
  int ret = system(command);
  g_free(command);
  unlink(last_config_path);
  g_free(last_config_path);
  last_config_path = NULL;
  if (ret == 0) {
    is_connected = false;
    send_status();
    FlValue* result = fl_value_new_bool(TRUE);
    return FL_METHOD_RESPONSE(fl_method_success_response_new(result));
  }
  FlValue* result = fl_value_new_bool(FALSE);
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

  g_autoptr(FlEventChannel) event_channel =
      fl_event_channel_new(fl_plugin_registrar_get_messenger(registrar),
                           "flutter_wireguard_plugin/status",
                           FL_METHOD_CODEC(codec));
  fl_event_channel_set_stream_handlers(event_channel,
                                       [](FlEventChannel* channel, FlValue* args, gpointer user_data, FlEventSink* sink) {
                                         status_sink = sink;
                                         send_status();
                                         return NULL;
                                       },
                                       [](FlEventChannel* channel, gpointer user_data) {
                                         status_sink = NULL;
                                         return NULL;
                                       },
                                       NULL, NULL);
  g_object_unref(plugin);
}
