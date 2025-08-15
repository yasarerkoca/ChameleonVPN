package com.example.flutter_wireguard_plugin

import android.content.Context
import io.flutter.embedding.engine.plugins.FlutterPlugin
import io.flutter.plugin.common.MethodCall
import io.flutter.plugin.common.MethodChannel
import io.flutter.plugin.common.MethodChannel.MethodCallHandler
import io.flutter.plugin.common.MethodChannel.Result

class FlutterWireguardPlugin: FlutterPlugin, MethodCallHandler {
  private lateinit var channel : MethodChannel
  private lateinit var context: Context

  override fun onAttachedToEngine(flutterPluginBinding: FlutterPlugin.FlutterPluginBinding) {
    context = flutterPluginBinding.applicationContext
    channel = MethodChannel(flutterPluginBinding.binaryMessenger, "flutter_wireguard_plugin")
    channel.setMethodCallHandler(this)
  }

  override fun onMethodCall(call: MethodCall, result: Result) {
    when (call.method) {
      "getPlatformVersion" -> {
        result.success("Android ${android.os.Build.VERSION.RELEASE}")
      }
      "connect" -> {
        val config = call.argument<String>("config")
        if (config == null) {
          result.error("INVALID_ARGUMENT", "Config param is null", null)
          return
        }
        val success = connectWireGuard(config)
        result.success(success)
      }
      "disconnect" -> {
        val success = disconnectWireGuard()
        result.success(success)
      }
      else -> {
        result.notImplemented()
      }
    }
  }

  override fun onDetachedFromEngine(binding: FlutterPlugin.FlutterPluginBinding) {
    channel.setMethodCallHandler(null)
  }

  // TODO: WireGuard bağlantısını başlatmak için native kod burada olacak
  private fun connectWireGuard(config: String): Boolean {
    // Burada WireGuard bağlantısını başlatan Android API'sini kullan
    // Şimdilik dummy olarak true döndürüyoruz
    // Gerçek implementasyonu WireGuard SDK ya da Komut satırı çağrısı ile yapmalısın
    return true
  }

  // TODO: WireGuard bağlantısını kesmek için native kod burada olacak
  private fun disconnectWireGuard(): Boolean {
    // Bağlantıyı kesmek için gerçek kod burada olacak
    return true
  }
}
