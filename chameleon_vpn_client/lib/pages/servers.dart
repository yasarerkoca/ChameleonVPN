import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import '../state.dart';

/// Displays available VPN servers and allows connecting or disconnecting.
class ServersPage extends ConsumerWidget {
  const ServersPage({super.key});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final servers = ref.watch(serverListProvider);
    final appState = ref.watch(appProvider);
    return Scaffold(
      appBar: AppBar(
        title: const Text('Select Server'),
        actions: [
          IconButton(
            key: const Key('profileButton'),
            icon: const Icon(Icons.person),
            onPressed: () => Navigator.pushNamed(context, '/profile'),
          )
        ],
      ),
      body: servers.when(
        data: (list) => ListView.builder(
          itemCount: list.length,
          itemBuilder: (_, i) {
            final server = list[i];
            final isSelected = appState.selectedServer?.id == server.id;
            final isConnected = isSelected && appState.isConnected;
            return ListTile(
              title: Text(server.name),
              trailing: ElevatedButton(
                key: Key('connectButton-${server.id}'),
                onPressed: () {
                  final notifier = ref.read(appProvider.notifier);
                  if (isConnected) {
                    notifier.disconnect();
                  } else {
                    notifier.selectServer(server);
                    notifier.connect();
                  }
                },
                child: Text(isConnected ? 'Disconnect' : 'Connect'),
              ),
            );
          },
        ),
        loading: () => const Center(child: CircularProgressIndicator()),
        error: (e, _) => Center(child: Text('Error: $e')),
      ),
    );
  }
}
