# KoHighlights Mobile Setup Guide

## Prerequisites

### Android
- Android SDK (API 24+)
- Android NDK
- JDK 11+
- gradle

### iOS (macOS only)
- Xcode 14+
- iOS 13.0+ SDK

## Initialize Android

```bash
cd tauri/KoHighlights
bunx tauri android init
```

This creates `src-tauri/gen/android/` with gradle build files.

## Initialize iOS

```bash
cd tauri/KoHighlights
bunx tauri ios init
```

This creates `src-tauri/gen/apple/` with Xcode project files.

## Android Configuration

Edit `src-tauri/gen/android/app/src/main/AndroidManifest.xml`:

```xml
<!-- After <uses-sdk> tag, add: -->
<uses-permission android:name="android.permission.READ_EXTERNAL_STORAGE" android:maxSdkVersion="32"/>
<uses-permission android:name="android.permission.MANAGE_EXTERNAL_STORAGE"/>
<uses-permission android:name="android.permission.WRITE_EXTERNAL_STORAGE" android:maxSdkVersion="28"/>
```

## iOS Configuration

Edit `src-tauri/gen/apple/KoHighlights/Info.plist`:

```xml
<!-- Add before </dict>: -->
<key>UIFileSharingEnabled</key>
<true/>
<key>LSSupportsOpeningDocumentsInPlace</key>
<true/>
<key>NSDocumentsFolderUsageDescription</key>
<string>KoHighlights needs access to find KOReader highlight files.</string>
```

## Capabilities

Mobile permissions configured in `src-tauri/capabilities/mobile.json`:
- fs:allow-read-file, fs:allow-write-file (file access)
- dialog:allow-open (directory picking)

On Android, before scanning, call `request_scan_permission` to request `MANAGE_EXTERNAL_STORAGE`.

On iOS, directory picking returns security-scoped URLs that Tauri handles automatically.

## Build & Run

### Android
```bash
bunx tauri android dev              # dev build on emulator/device
bunx tauri android build --release   # production APK
```

### iOS
```bash
bunx tauri ios dev                   # dev build on simulator/device
bunx tauri ios build --release       # production IPA
```

## Notes

- DuckDB bundled feature: verify cross-compilation for ARM64 (Android/iOS)
- If DuckDB fails on mobile, fallback: use SQLite for notes instead (schema identical)
- System paths resolved via `tauri::path::app_data_dir()` — platform-specific automatically
