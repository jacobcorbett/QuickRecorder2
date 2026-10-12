# Changelog

## 1.6.10 - 2026-10-12

- Restore menu-bar stop, pause/resume, camera and main-panel clicks on macOS 27, incorporating dabeeeenster's upstream PR #294 at f0d2e3441963a1188f22155f233a7fd044a14c2b.
- Keep the Quick Recorder 2 name, separate app identity and disabled upstream updater.
- Preserve the existing opt-in floating controller setting for Ice users, with recording duration and automatic-stop processing retained.

Validation: this fork passed a signed universal Release build and launched as Quick Recorder 2 v1.6.10; its click-routing checks passed. The upstream patch built on macOS 27.0.1; click-routing checks passed; Jacob stopped a real recording using the menu-bar button and the resulting 54.6-second HEVC video decoded without errors. The floating-controller and camera interactions have not been independently exercised on macOS 27.
