import 'dart:convert';

import 'package:google_sign_in/google_sign_in.dart';
import 'package:http/http.dart' as http;

import 'constants.dart';

/// Geliştirici modundaki sahte girişin yerine gerçek Google OAuth akışını
/// başlatır. Kullanıcı Google ile oturum açtıktan sonra elde edilen ID
/// token'ı backend API'sine ileterek uygulama için bir erişim jetonu alır.
///
/// Dönüş değeri backend'den alınan erişim jetonudur. İşlem herhangi bir
/// aşamada başarısız olursa `null` döner.
Future<String?> signInWithGoogle() async {
  try {
    // Google kimlik doğrulamasını başlat.
    final GoogleSignInAccount? account = await GoogleSignIn().signIn();
    if (account == null) return null; // Kullanıcı iptal etti.

    // Google'dan ID token elde et.
    final GoogleSignInAuthentication auth = await account.authentication;
    final String? idToken = auth.idToken;
    if (idToken == null) return null;

    // ID token'ı backend'e göndererek uygulama erişim jetonu al.
    final response = await http.post(
      Uri.parse('$baseUrl/auth/google/token'),
      headers: {'Content-Type': 'application/json'},
      body: jsonEncode({'token': idToken}),
    );

    if (response.statusCode != 200) return null;
    final data = jsonDecode(response.body) as Map<String, dynamic>;
    return data['access_token'] as String?;
  } catch (_) {
    return null;
  }
}

