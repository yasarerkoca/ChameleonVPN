import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'state.dart';
import 'login_page.dart';

class ProfilePage extends ConsumerWidget {
  const ProfilePage({super.key});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final user = ref.watch(appProvider).user;
    return Scaffold(
      appBar: AppBar(title: const Text('Profile')),
      body: user == null
          ? const Center(child: Text('No user'))
          : Padding(
              padding: const EdgeInsets.all(16),
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Text('Name: ${user.name}', key: const Key('userName')),
                  Text('Subscription: ${user.subscription}', key: const Key('subscription')),
                  const SizedBox(height: 16),
                  ElevatedButton(
                    key: const Key('refreshToken'),
                    onPressed: () => ref.read(appProvider.notifier).refreshToken(),
                    child: const Text('Refresh Token'),
                  ),
                  ElevatedButton(
                    key: const Key('logoutButton'),
                    onPressed: () {
                      ref.read(appProvider.notifier).logout();
                      Navigator.pushNamedAndRemoveUntil(context, '/', (_) => false);
                    },
                    child: const Text('Logout'),
                  ),
                ],
              ),
            ),
    );
  }
}
