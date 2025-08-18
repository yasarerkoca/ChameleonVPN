package com.example.flutter_wireguard_plugin

import android.content.Context
import io.flutter.embedding.engine.plugins.FlutterPlugin
import io.flutter.plugin.common.MethodCall
import io.flutter.plugin.common.MethodChannel
import io.flutter.plugin.common.MethodChannel.MethodCallHandler
import io.flutter.plugin.common.MethodChannel.Result
import java.io.File

class FlutterWireguardPlugin: FlutterPlugin, MethodCallHandler {
  private lateinit var channel : MethodChannel
  private lateinit var context: Context
  private var lastConfigFile: File? = null
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

  private fun connectWireGuard(config: String): Boolean {
    return try {
      val file = File.createTempFile("wg", ".conf", context.cacheDir)
      file.writeText(config)
      val process = ProcessBuilder("sh", "-c", "wg-quick up ${file.absolutePath}").start()
      val exit = process.waitFor()
      if (exit == 0) {
        lastConfigFile = file
        true
      } else {
        file.delete()
        false
      }
    } catch (e: Exception) {
      e.printStackTrace()
      false
    }
  }

  private fun disconnectWireGuard(): Boolean {
    val file = lastConfigFile ?: return false
    return try {
      val process = ProcessBuilder("sh", "-c", "wg-quick down ${file.absolutePath}").start()
      val exit = process.waitFor()
      file.delete()
      lastConfigFile = null
      exit == 0
    } catch (e: Exception) {
      e.printStackTrace()
      false
    }
  }
}
