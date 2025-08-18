package com.example.flutter_wireguard_plugin

import io.flutter.plugin.common.MethodCall
import io.flutter.plugin.common.MethodChannel
import kotlin.test.Test
import org.mockito.Mockito

/*
 * This demonstrates a simple unit test of the Kotlin portion of this plugin's implementation.
 *
 * Once you have built the plugin's example app, you can run these tests from the command
 * line by running `./gradlew testDebugUnitTest` in the `example/android/` directory, or
 * you can run them directly from IDEs that support JUnit such as Android Studio.
 */

internal class FlutterWireguardPluginTest {
  @Test
  fun onMethodCall_getPlatformVersion_returnsExpectedValue() {
    val plugin = FlutterWireguardPlugin()

    val call = MethodCall("getPlatformVersion", null)
    val mockResult: MethodChannel.Result = Mockito.mock(MethodChannel.Result::class.java)
    plugin.onMethodCall(call, mockResult)

    Mockito.verify(mockResult).success("Android " + android.os.Build.VERSION.RELEASE)
  }
  @Test
  fun onMethodCall_connectAndDisconnect_returnsBoolean() {
    val plugin = FlutterWireguardPlugin()

    val connectCall = MethodCall("connect", mapOf("config" to "[Interface]\nPrivateKey = x\nAddress = 10.0.0.2/32"))
    val connectResult: MethodChannel.Result = Mockito.mock(MethodChannel.Result::class.java)
    plugin.onMethodCall(connectCall, connectResult)
    Mockito.verify(connectResult).success(Mockito.anyBoolean())

    val disconnectCall = MethodCall("disconnect", null)
    val disconnectResult: MethodChannel.Result = Mockito.mock(MethodChannel.Result::class.java)
    plugin.onMethodCall(disconnectCall, disconnectResult)
    Mockito.verify(disconnectResult).success(Mockito.anyBoolean())
  }
}
