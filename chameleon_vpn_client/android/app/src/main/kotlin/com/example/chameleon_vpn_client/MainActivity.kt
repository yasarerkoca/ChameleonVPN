package com.example.chameleon_vpn_client

import io.flutter.embedding.android.FlutterActivity
import io.flutter.embedding.engine.FlutterEngine

class MainActivity : FlutterActivity() {
    override fun configureFlutterEngine(flutterEngine: FlutterEngine) {
        super.configureFlutterEngine(flutterEngine)
        WireguardChannel(this, flutterEngine.dartExecutor.binaryMessenger)
    }
}
