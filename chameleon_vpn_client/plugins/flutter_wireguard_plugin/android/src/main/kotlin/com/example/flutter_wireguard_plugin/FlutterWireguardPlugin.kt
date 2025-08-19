package com.example.flutter_wireguard_plugin

import android.content.Context
import io.flutter.embedding.engine.plugins.FlutterPlugin
import io.flutter.plugin.common.EventChannel
import io.flutter.plugin.common.MethodCall
import io.flutter.plugin.common.MethodChannel
import io.flutter.plugin.common.MethodChannel.MethodCallHandler
import io.flutter.plugin.common.MethodChannel.Result
import java.io.File

class FlutterWireguardPlugin: FlutterPlugin, MethodCallHandler, EventChannel.StreamHandler {
  private lateinit var channel : MethodChannel
  private lateinit var statusChannel: EventChannel
  private var events: EventChannel.EventSink? = null
  private lateinit var context: Context
  private var lastConfigFile: File? = null
  private var isConnected = false

  override fun onAttachedToEngine(flutterPluginBinding: FlutterPlugin.FlutterPluginBinding) {
    context = flutterPluginBinding.applicationContext
    channel = MethodChannel(flutterPluginBinding.binaryMessenger, "flutter_wireguard_plugin")
    channel.setMethodCallHandler(this)
    statusChannel = EventChannel(flutterPluginBinding.binaryMessenger, "flutter_wireguard_plugin/status")
    statusChannel.setStreamHandler(this)
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

  override fun onListen(arguments: Any?, events: EventChannel.EventSink?) {
    this.events = events
    events?.success(if (isConnected) "connected" else "disconnected")
  }

  override fun onCancel(arguments: Any?) {
    events = null
  }

  private fun connectWireGuard(config: String): Boolean {
    return try {
      val file = File.createTempFile("wg", ".conf", context.cacheDir)
      file.writeText(config)
      val process = ProcessBuilder("sh", "-c", "wg-quick up ${file.absolutePath}").start()
      val exit = process.waitFor()
      if (exit == 0) {
        lastConfigFile = file
        isConnected = true
        events?.success("connected")
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
      val success = exit == 0
      if (success) {
        isConnected = false
        events?.success("disconnected")
      }
      success
    } catch (e: Exception) {
      e.printStackTrace()
      false
    }
  }
}
