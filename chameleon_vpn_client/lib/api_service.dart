import 'dart:convert';
import 'package:http/http.dart' as http;
import 'services/auth.dart';

import 'constants.dart';
/// Simple API client for interacting with the backend.
class ApiService {
  ApiService({required this.auth});
  final AuthService auth;
  /// Authenticate the user and store tokens on success.
  Future<bool> login(String email, String password) async {
    final response = await http.post(
      Uri.parse('$baseUrl/login'),
      body: {'email': email, 'password': password},
    );

    if (response.statusCode == 200) {
      final data = jsonDecode(response.body) as Map<String, dynamic>;
      final access = data['access'] as String?;
      final refresh = data['refresh'] as String?;
      if (access != null && refresh != null) {
        await auth.persistTokens(access, refresh);
        return true;
      }
    }
    return false;
  }

  /// Remove all stored authentication tokens.
  Future<void> logout() => auth.clearTokens();

  /// Retrieve the current subscription information for the user.
  Future<Map<String, dynamic>?> fetchSubscription() async {
    final token = await auth.getValidAccessToken();
    if (token == null) return null;
    final response = await http.get(
      Uri.parse('$baseUrl/subscription'),
      headers: {'Authorization': 'Bearer $token'},
    );

    if (response.statusCode == 200) {
      return jsonDecode(response.body) as Map<String, dynamic>;
    }
    return null;
  }

  /// Notify the backend that a VPN session has been requested.

  Future<bool> startVpnSession() async {
    final token = await auth.getValidAccessToken();
    if (token == null) return false;
    final response = await http.post(
      Uri.parse('$baseUrl/vpn/start'),
      headers: {'Authorization': 'Bearer $token'},
    );

    return response.statusCode == 200;
  }
}
