# Changelog

## 1.6.11 - 2026-10-12

- Upgrade the inherited Sparkle 2.6.0 dependency to 2.10.0, including intervening security fixes.
- Enable Sparkle updates from this fork’s GitHub-hosted feed and release archives, authenticated with a dedicated Ed25519 signing key.
- Restore Check for Updates in the app menu and General settings, with automatic checking and optional automatic downloads.
- Block checks during recording and defer an update restart if recording starts after download.
- Add a reproducible packaging script and release instructions. Existing 1.6.10 installations require one manual upgrade.

Validation: signed universal Release build with Sparkle 2.10.0; menu-bar routing and recording-guard checks passed; the signed archive verified and a tampered copy was rejected. Sparkle downloaded, installed and relaunched the app locally from test build 170 to release build 171 in Applications. The original QuickRecorder app remained unchanged. This release is Apple Development signed and is not notarized.

## 1.6.10 - 2026-10-12

- Restore menu-bar stop, pause/resume, camera and main-panel clicks on macOS 27, incorporating dabeeeenster's upstream PR #294 at f0d2e3441963a1188f22155f233a7fd044a14c2b.
- Keep the Quick Recorder 2 name, separate app identity and disabled upstream updater.
- Preserve the existing opt-in floating controller setting for Ice users, with recording duration and automatic-stop processing retained.

Validation: this fork passed a signed universal Release build and launched as Quick Recorder 2 v1.6.10; its click-routing checks passed. The upstream patch built on macOS 27.0.1; click-routing checks passed; Jacob stopped a real recording using the menu-bar button and the resulting 54.6-second HEVC video decoded without errors. The floating-controller and camera interactions have not been independently exercised on macOS 27.
