# Mobile Release

## Android (.apk)
flutter clean
flutter pub get
flutter build apk --release --dart-define=BASE_URL=https://api.example.com
# Çıktı: build/app/outputs/flutter-apk/app-release.apk

## Keystore (ilk sefer)
# keytool -genkey -v -keystore chameleon.keystore -alias chameleon -keyalg RSA -keysize 2048 -validity 10000
# android/key.properties dosyasını doldurun.

## iOS (ipa - özet)
# Xcode ile archive -> Distribute App (manual signing)

## Versiyonlama
# pubspec.yaml: version: MAJOR.MINOR+BUILD
