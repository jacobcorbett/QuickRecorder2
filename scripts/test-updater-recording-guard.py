#!/usr/bin/env python3
"""Run the production Sparkle delegate against a recording-state fixture."""
from pathlib import Path
import argparse
import subprocess
import tempfile

root = Path(__file__).resolve().parents[1]
parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--sparkle-framework', type=Path, required=True)
args = parser.parse_args()
source = (root / 'QuickRecorder/Supports/Sparkle.swift').read_text()
delegate = source[source.index('final class RecorderUpdaterDelegate:'):]
cases = '''
let delegate = RecorderUpdaterDelegate()
let controller = SPUStandardUpdaterController(startingUpdater: false, updaterDelegate: delegate, userDriverDelegate: nil)
let updater = controller.updater
try delegate.updater(updater, mayPerform: .updates)
SCContext.streamType = 1
for check in [SPUUpdateCheck.updates, .updatesInBackground, .updateInformation] {
    do {
        try delegate.updater(updater, mayPerform: check)
        fatalError("Recording allowed an update check")
    } catch { assert(error.localizedDescription.contains("finish your recording")) }
}
let item = SUAppcastItem(dictionary: ["title": "Test update", "enclosure": ["url": "https://example.com/update.zip", "sparkle:version": "171", "length": "1"]])!
var installed = 0
assert(delegate.updater(updater, shouldPostponeRelaunchForUpdate: item, untilInvokingBlock: { installed += 1 }))
RunLoop.current.run(until: Date(timeIntervalSinceNow: 1.2))
assert(installed == 0, "Installer ran during recording")
SCContext.streamType = nil
RunLoop.current.run(until: Date(timeIntervalSinceNow: 1.2))
assert(installed == 1, "Installer did not resume after recording")
RunLoop.current.run(until: Date(timeIntervalSinceNow: 1.2))
assert(installed == 1, "Installer resumed twice")
assert(!delegate.updater(updater, shouldPostponeRelaunchForUpdate: item, untilInvokingBlock: { installed += 1 }))
print("PASS: idle checks, blocked recording checks, deferred restart, resume once, idle restart")
'''
with tempfile.TemporaryDirectory(prefix='qr2-updater-') as directory:
    path = Path(directory) / 'Guard.swift'
    path.write_text('import Foundation\nimport Sparkle\nclass SCContext { static var streamType: Int? }\n' + delegate + cases)
    subprocess.run(['xcrun', 'swift', '-F', str(args.sparkle_framework.parent), '-framework', 'Sparkle', str(path)], check=True)
