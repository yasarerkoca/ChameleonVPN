import 'dart:convert';

import 'package:flutter_secure_storage/flutter_secure_storage.dart';
import 'package:http/http.dart' as http;
import '../constants.dart';

/// Handles authentication token storage and refresh logic.
class AuthService {
  AuthService({FlutterSecureStorage? storage})
      : storage = storage ?? const FlutterSecureStorage();

  final FlutterSecureStorage storage;

  static const _accessKey = 'access';
  static const _refreshKey = 'refresh';

  /// Save access and refresh tokens securely.
  Future<void> persistTokens(String access, String refresh) async {
    await storage.write(key: _accessKey, value: access);
    await storage.write(key: _refreshKey, value: refresh);
  }

  /// Retrieve the stored access token.
  Future<String?> readAccessToken() => storage.read(key: _accessKey);

  /// Retrieve the stored refresh token.
  Future<String?> readRefreshToken() => storage.read(key: _refreshKey);

  /// Delete all stored tokens.
  Future<void> clearTokens() => storage.deleteAll();

  bool _isExpired(String token) {
    try {
      final parts = token.split('.');
      if (parts.length != 3) return true;
      final payload = utf8.decode(
        base64Url.decode(base64Url.normalize(parts[1])),
      );
      final data = jsonDecode(payload) as Map<String, dynamic>;
      final exp = data['exp'];
      if (exp is int) {
        final expiry = DateTime.fromMillisecondsSinceEpoch(exp * 1000);
        return DateTime.now().isAfter(expiry);
      }
      return true;
    } catch (_) {
      return true;
    }
  }

  /// Refresh the access token using the stored refresh token.
  Future<bool> refresh() async {
    final refreshToken = await readRefreshToken();
    if (refreshToken == null) return false;
    final response = await http.post(
      Uri.parse('$baseUrl/auth/refresh'),
      headers: {'Authorization': 'Bearer $refreshToken'},
    );
    if (response.statusCode == 200) {
      final data = jsonDecode(response.body) as Map<String, dynamic>;
      final access = data['access'] as String?;
      final refresh = data['refresh'] as String? ?? refreshToken;
      if (access != null) {
        await persistTokens(access, refresh);
        return true;
      }
    }
    return false;
  }

  /// Retrieve a valid access token, refreshing it if necessary.
  Future<String?> getValidAccessToken() async {
    final access = await readAccessToken();
    if (access == null) return null;
    if (_isExpired(access)) {
      final ok = await refresh();
      if (!ok) return null;
      return readAccessToken();
    }
    return access;
  }
}
