import 'dart:convert';
import 'package:http/http.dart' as http;

/// Simple API client for interacting with the backend.
class ApiService {
  ApiService({required this.baseUrl});

  final String baseUrl;

  /// Authenticate the user and return an auth token on success.
  Future<String?> login(String email, String password) async {
    final response = await http.post(
      Uri.parse('$baseUrl/login'),
      body: {'email': email, 'password': password},
    );

    if (response.statusCode == 200) {
      final data = jsonDecode(response.body) as Map<String, dynamic>;
      return data['token'] as String?;
    }
    return null;
  }

  /// Retrieve the current subscription information for the user.
  Future<Map<String, dynamic>?> fetchSubscription(String token) async {
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
  Future<bool> startVpnSession(String token) async {
    final response = await http.post(
      Uri.parse('$baseUrl/vpn/start'),
      headers: {'Authorization': 'Bearer $token'},
    );

    return response.statusCode == 200;
  }
}
