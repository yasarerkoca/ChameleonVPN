# Mobile Release

## v1.0.0
- Login + 2FA
- OpenVPN & WireGuard bağlantısı
- Plan/Proxy görüntüleme
- Hata düzeltmeleri

## Assets
- Icons: 512x512 (Play Store) and 1024x1024 (App Store) PNGs
- Screenshots: phone and tablet images for each store
- Feature graphic (Play Store): 1024x500

## Build & Signing
### Android
1. Update version in `pubspec.yaml` (`version: x.y.z+build`).
2. Configure release keystore in `android/key.properties`.
3. Build signed bundle: `flutter build appbundle --release`.
4. Optional: `make mobile-build` automates `flutter clean`, dependency fetch, and APK build.

### iOS
1. Update version/build in `pubspec.yaml` and Xcode.
2. Ensure signing certificates and provisioning profiles are installed.
3. Build release: `flutter build ipa --release` or **Product → Archive** in Xcode.
4. Export the `.ipa` via Xcode Organizer.

## Store Submission
### Google Play
1. Upload the AAB in the Play Console and provide release notes.
2. Supply required icon, screenshots, and feature graphic.
3. Fill short/full descriptions, content rating, and privacy policy URL.

### Apple App Store
1. Upload the `.ipa` through Xcode Organizer or Transporter.
2. Provide the App Icon set and required screenshots for each device size.
3. Add description, keywords, and promotional text.

## Metadata
- Versioning comes from `pubspec.yaml` (`x.y.z+build`) and maps to Android/iOS builds.
- Ensure store listings include up‑to‑date descriptions, keywords, and changelog text.
- Keep version numbers synchronized across Android and iOS submissions.

## Automation
- `make mobile-build` builds the Android release APK.
- No automated upload scripts are currently provided.
