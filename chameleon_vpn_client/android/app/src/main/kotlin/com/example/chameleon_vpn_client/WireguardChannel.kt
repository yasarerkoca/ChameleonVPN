package com.example.chameleon_vpn_client

import android.app.Notification
import android.app.NotificationChannel
import android.app.NotificationManager
import android.content.Context
import android.content.Intent
import android.net.VpnService
import android.os.Build
import android.os.ParcelFileDescriptor
import androidx.core.app.NotificationCompat
import io.flutter.plugin.common.BinaryMessenger
import io.flutter.plugin.common.MethodCall
import io.flutter.plugin.common.MethodChannel
import io.flutter.plugin.common.MethodChannel.MethodCallHandler
import io.flutter.plugin.common.MethodChannel.Result

class WireguardChannel(private val context: Context, messenger: BinaryMessenger) : MethodCallHandler {
    private val channel = MethodChannel(messenger, "wireguard_channel")

    init {
        channel.setMethodCallHandler(this)
    }

    override fun onMethodCall(call: MethodCall, result: Result) {
        when (call.method) {
            "openTunnel" -> {
                val prepareIntent = VpnService.prepare(context)
                if (prepareIntent != null) {
                    result.error("NOT_PREPARED", "User consent required", null)
                    context.startActivity(prepareIntent)
                    return
                }
                try {
                    context.startService(Intent(context, WireguardVpnService::class.java))
                    result.success(null)
                } catch (e: Exception) {
                    result.error("START_FAILED", e.localizedMessage, null)
                }
            }
            "closeTunnel" -> {
                context.stopService(Intent(context, WireguardVpnService::class.java))
                result.success(null)
            }
            "status" -> {
                result.success(if (WireguardVpnService.isRunning) "running" else "stopped")
            }
            else -> result.notImplemented()
        }
    }
}

class WireguardVpnService : VpnService() {
    companion object {
        @Volatile
        var isRunning: Boolean = false
            private set
    }

    private var vpnInterface: ParcelFileDescriptor? = null

    override fun onStartCommand(intent: Intent?, flags: Int, startId: Int): Int {
        val builder = Builder()
            .setSession("WireGuard")
            // Kill-switch: block traffic outside the tunnel
        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.Q) {
            builder.setBlocking(true)
        }
        builder.addAddress("10.0.0.2", 32)
        builder.addRoute("0.0.0.0", 0)
        vpnInterface = builder.establish()

        startForeground(1, createNotification())
        isRunning = true
        return START_STICKY
    }

    override fun onDestroy() {
        vpnInterface?.close()
        isRunning = false
        super.onDestroy()
    }

    private fun createNotification(): Notification {
        val channelId = "wireguard_vpn"
        val manager = getSystemService(Context.NOTIFICATION_SERVICE) as NotificationManager
        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.O) {
            val channel = NotificationChannel(channelId, "WireGuard VPN", NotificationManager.IMPORTANCE_LOW)
            manager.createNotificationChannel(channel)
        }
        return NotificationCompat.Builder(this, channelId)
            .setContentTitle("Chameleon VPN")
            .setContentText("VPN is running")
            .setSmallIcon(android.R.drawable.stat_sys_vpn_lock)
            .build()
    }
}
