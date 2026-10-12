#!/usr/bin/env python3
"""Exercise the shipped menu-bar router without needing recording permission."""
from pathlib import Path
import subprocess
import tempfile

root = Path(__file__).resolve().parents[1]
source = (root / "QuickRecorder/ViewModel/StatusBar.swift").read_text()
router = source[source.index("final class StatusBarHitTest {"):source.index("private struct StatusBarHitRegion:")]
cases = 'let router = StatusBarHitTest.shared\nvar stop = 0\nvar pause = 0\nrouter.reset()\nlet old = router.generation\nrouter.register(id: "stop", frame: CGRect(x: 4,y:0,width:16,height:22), generation: old) { stop += 1 }\nrouter.register(id: "pause", frame: CGRect(x: 24,y:0,width:16,height:22), generation: old) { pause += 1 }\nrouter.handleClick(atX: 22)\nassert(stop == 0 && pause == 0, "spacing should not fire controls")\nrouter.handleClick(atX: 12)\nassert(stop == 1 && pause == 0, "stop click routed incorrectly")\nrouter.handleClick(atX: 32)\nrouter.handleClick(atX: 32)\nassert(pause == 1, "duplicate pause click must not cancel itself")\nThread.sleep(forTimeInterval: 0.2)\nrouter.handleClick(atX: 32)\nassert(pause == 2, "subsequent pause click must work")\nrouter.reset()\nlet fresh = router.generation\nrouter.register(id: "pause", frame: CGRect(x: 50,y:0,width:16,height:22), generation: fresh) { pause += 1 }\nrouter.unregister(id: "pause", generation: old)\nrouter.register(id: "stop", frame: CGRect(x: 50,y:0,width:16,height:22), generation: old) { stop += 1 }\nrouter.handleClick(atX: 58)\nassert(pause == 3 && stop == 1, "stale teardown/registration affected replacement")\nrouter.reset()\nrouter.handleClick(atX: 58)\nassert(pause == 3, "reset should clear old recording controls")\nrouter.register(id: "zero", frame: .zero, generation: router.generation) { stop += 1 }\nrouter.handleClick(atX: 0)\nassert(stop == 1, "zero width region should not fire")\nprint("PASS: stop/pause routing, gaps, debounce, subsequent clicks, stale registration/teardown, reset, zero-width controls")\n'
with tempfile.TemporaryDirectory(prefix="qr2-routing-") as directory:
    test_file = Path(directory) / "HitRouting.swift"
    test_file.write_text("import Foundation\nimport CoreGraphics\nfunc qrLog(_ message: @autoclosure () -> String) {}\n" + router + cases)
    subprocess.run(["xcrun", "swift", str(test_file)], check=True)
