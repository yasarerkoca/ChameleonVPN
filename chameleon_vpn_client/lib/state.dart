import 'dart:convert';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:http/http.dart' as http;
import 'constants.dart';

class User {
  final String name;
  final String subscription;
  final String token;
  const User({required this.name, required this.subscription, required this.token});

  User copyWith({String? name, String? subscription, String? token}) =>
      User(
        name: name ?? this.name,
        subscription: subscription ?? this.subscription,
        token: token ?? this.token,
      );
}

class Server {
  final String id;
  final String name;
  const Server({required this.id, required this.name});
}

class AppState {
  final User? user;
  final Server? selectedServer;
  final bool isConnected;
  final List<String> logs;
  const AppState({this.user, this.selectedServer, this.isConnected = false, this.logs = const []});

  AppState copyWith({User? user, Server? selectedServer, bool? isConnected, List<String>? logs}) =>
      AppState(
        user: user ?? this.user,
        selectedServer: selectedServer ?? this.selectedServer,
        isConnected: isConnected ?? this.isConnected,
        logs: logs ?? this.logs,
      );
}

class AppNotifier extends StateNotifier<AppState> {
  AppNotifier() : super(const AppState());

  void login(User user) {
    state = state.copyWith(user: user);
  }

  Future<void> refreshToken() async {
    final token = state.user?.token;
    if (token == null) return;
    // Dummy refresh: call endpoint and update token
    final res = await http.post(Uri.parse('$baseUrl/auth/refresh'), headers: {'Authorization': 'Bearer $token'});
    if (res.statusCode == 200) {
      final data = jsonDecode(res.body) as Map<String, dynamic>;
      state = state.copyWith(user: state.user!.copyWith(token: data['access_token'] as String));
    }
  }

  void logout() {
    state = const AppState();
  }

  void selectServer(Server server) {
    state = state.copyWith(selectedServer: server);
  }

  void connect() {
    state = state.copyWith(isConnected: true, logs: [...state.logs, 'Connected to ${state.selectedServer?.name}']);
  }

  void disconnect() {
    state = state.copyWith(isConnected: false, logs: [...state.logs, 'Disconnected']);
  }

  void addLog(String log) {
    state = state.copyWith(logs: [...state.logs, log]);
  }
}

final appProvider = StateNotifierProvider<AppNotifier, AppState>((ref) => AppNotifier());

final serverListProvider = FutureProvider<List<Server>>((ref) async {
  final res = await http.get(Uri.parse('$baseUrl/servers'));
  if (res.statusCode == 200) {
    final data = jsonDecode(res.body) as List<dynamic>;
    return data
        .map((e) => Server(id: e['id'].toString(), name: e['name'] as String))
        .toList();
  } else {
    throw Exception('Failed to load servers');
  }
});
