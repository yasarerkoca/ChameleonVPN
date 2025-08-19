import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'state.dart';

class ConnectionStatusPage extends ConsumerWidget {
  const ConnectionStatusPage({super.key});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final state = ref.watch(appProvider);
    return Scaffold(
      appBar: AppBar(title: const Text('Connection Status'), actions: [
        IconButton(
          icon: const Icon(Icons.person),
          onPressed: () => Navigator.pushNamed(context, '/profile'),
        )
      ]),
      body: Padding(
        padding: const EdgeInsets.all(16),
        child: Column(
          children: [
            Text(state.selectedServer?.name ?? 'No server'),
            const SizedBox(height: 16),
            ElevatedButton(
              key: const Key('connectButton'),
              onPressed: () {
                final notifier = ref.read(appProvider.notifier);
                state.isConnected ? notifier.disconnect() : notifier.connect();
              },
              child: Text(state.isConnected ? 'Disconnect' : 'Connect'),
            ),
            const SizedBox(height: 16),
            Expanded(
              child: ListView(
                children: [for (final log in state.logs) Text(log)],
              ),
            )
          ],
        ),
      ),
    );
  }
}
