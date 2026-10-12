# Quick Recorder 2

A macOS screen recorder based on [QuickRecorder](https://github.com/lihaoyun6/QuickRecorder), with fixes for macOS 27 and optional floating controls for Ice users.

Current version: **1.6.10**. Requires macOS 12.3 or later; the menu-bar fix was tested on macOS 27.0.1.

## What changed

- **macOS 27 menu-bar controls:** restore clicks on stop, pause/resume, camera and the main panel, incorporating [dabeeeenster’s upstream fix](https://github.com/lihaoyun6/QuickRecorder/pull/294).
- **Optional floating controller:** keep it hidden when Ice hides the menu-bar item, with a Recorder setting to restore the floating controls.
- **Separate app:** installs as Quick Recorder 2, with its own preferences and permissions. Upstream binary updates are disabled.

See [CHANGELOG.md](CHANGELOG.md) for changes and validation, including interactions that still need testing.

## Build and install

Clone this repository and open `QuickRecorder.xcodeproj` in Xcode. Select the **QuickRecorder** scheme and configure the app target’s signing with your own Apple Development identity. Build with **Product → Build**.

Use **Product → Show Build Folder in Finder**, then open `Products/Debug` and copy **Quick Recorder 2.app** to Applications. macOS will ask for recording permissions when needed.

To check menu-bar click routing:

```sh
python3 scripts/test-menu-bar-routing.py
```

## Licence and credits

Copyright © 2024 lihaoyun6. Fork modifications © 2026 Jacob Corbett, started 1 October 2026. Modification dates and contributors are recorded in Git and the changelog.

Licensed under the [GNU Affero General Public License v3](LICENSE), without warranty. Keep the licence and copyright notices with redistributed copies, and provide the corresponding source when distributing binaries. This repository contains the fork’s source; third-party components retain their own licences.

Credit to lihaoyun6 and the [QuickRecorder contributors](https://github.com/lihaoyun6/QuickRecorder), dabeeeenster for the macOS 27 fix, and the upstream projects [Azayaka](https://github.com/Mnpn/Azayaka), [KeyboardShortcuts](https://github.com/sindresorhus/KeyboardShortcuts), [SwiftLAME](https://github.com/hidden-spectrum/SwiftLAME) and [Sparkle](https://github.com/sparkle-project/Sparkle).
