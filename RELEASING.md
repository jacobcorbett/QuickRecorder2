# Publishing an update

Quick Recorder 2 uses Sparkle 2.10.0. Its appcast is hosted in `updates/appcast.xml` on this repository's `main` branch; archives are hosted in GitHub Releases. Only updates signed with the matching Ed25519 key are accepted. The private key stays in the maintainer's login Keychain under account `QuickRecorder2`; never commit or upload it.

## Build and publish

1. Increase `MARKETING_VERSION` and `CURRENT_PROJECT_VERSION` in both build configurations. The build number must increase for Sparkle to offer an update. Update the changelog and README.
2. Build a universal Release app with your signing identity. For public distribution, use a Developer ID Application certificate and notarize/staple the app before packaging. The initial 1.6.11 release uses Apple Development signing and is **not notarized**; first-time downloads may require a manual Gatekeeper approval.
3. Run the routing and recording-guard checks, then package the app:

```sh
python3 scripts/test-menu-bar-routing.py
python3 scripts/test-updater-recording-guard.py --sparkle-framework build/ReleaseValidation/SourcePackages/artifacts/sparkle/Sparkle/Sparkle.xcframework/macos-arm64_x86_64/Sparkle.framework
python3 scripts/package-update.py 'build/ReleaseValidation/Build/Products/Release/Quick Recorder 2.app' --sparkle-bin build/ReleaseValidation/SourcePackages/artifacts/sparkle/Sparkle/bin
```

The packaging script verifies the app's identity, production feed, public signing key and code signature, creates a ZIP with symlinks intact plus licence, component notices and a corresponding-source link, signs it from Keychain, verifies its signature and writes the appcast. It refuses to overwrite an existing archive. Never alter an archive after signing it. Keep the signing key backed up securely outside the repository: losing it prevents updates to existing installations.

4. Test an upgrade from a lower build in a disposable app directory. Use a copy with its plist feed pointed at a localhost test server, re-sign that test copy, and serve a copy of the appcast whose enclosure points at the same signed release archive locally. Check download, installation, relaunch and the resulting build number. Verify the production archive signature and rejection of a tampered copy.
5. Review the diff and commit source changes. Push that commit, create tag `vVERSION`, and publish a GitHub release with `build/releases/QuickRecorder2-VERSION.zip`. Publish `updates/appcast.xml` only once its archive is publicly downloadable; it can be committed separately after the release. Include a link to the tagged corresponding source and the signing/notarization status in the release notes.
6. Verify the public feed and download, their signature and size, and the installed app's **Check for Updates…** result. Do not replace or modify a published archive; publish a higher build instead.

## User behaviour

Automatic checks are enabled by default. Automatic downloading/installation is opt-in in **Settings → General → Updates**. Manual checks are also available in the app menu. Checks are declined during recording; if a recording starts after an update is downloaded, its restart is deferred until recording ends. Sparkle runs its usual installation flow rather than a custom GitHub API client.

Versions before 1.6.11 have no fork updater. Users must install 1.6.11 or later once manually; subsequent releases can arrive through Sparkle. The original QuickRecorder app has a separate bundle identity and is never replaced by this updater.
