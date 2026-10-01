# Quick Recorder 2 agent guidance

- This is Jacob Corbett's independent public fork of lihaoyun6/QuickRecorder, licensed under GNU AGPLv3. Preserve LICENSE, upstream copyright notices, attribution and Git history. Do not describe upstream as abandoned without evidence.
- Work in small, reversible commits using specific conventional prefixes: feat:, fix:, chore:, docs:, refactor:.
- Check git status --short before staging. Stage explicit files, preserve user edits, and keep secrets out of Git.
- Run the smallest meaningful verification before committing. The existing Xcode project is QuickRecorder.xcodeproj and the shared scheme is QuickRecorder. Discover build requirements; do not invent signing credentials or team IDs.
- Whenever Jacob asks to create, open, prepare, or make a pull request, run the personal local-pr-autoreview skill before committing, pushing, or opening that PR. Keep review local; do not install hosted review bots.
- origin points to jacobcorbett/QuickRecorder2; upstream points to lihaoyun6/QuickRecorder. Push only to the fork when authorised. Keep changes clearly distinguishable from upstream.
- For a separately installed fork build, establish a distinct app bundle identifier and disable the upstream Sparkle update feed before installation. Preserve file format compatibility and attribution.
- Validate the Ice fix by hiding and revealing the recording controls, stopping a recording, and checking the output. A build alone does not prove recording behaviour.
