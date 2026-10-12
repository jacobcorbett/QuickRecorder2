#!/usr/bin/env python3
"""Package a signed build and create the GitHub-hosted Sparkle feed."""
import argparse
from email.utils import formatdate
from pathlib import Path
import plistlib
import subprocess
import shutil
import tempfile
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
FEED = 'https://raw.githubusercontent.com/jacobcorbett/QuickRecorder2/main/updates/appcast.xml'
REPO = 'https://github.com/jacobcorbett/QuickRecorder2'
SPARKLE = 'http://www.andymatuschak.org/xml-namespaces/sparkle'
ET.register_namespace('sparkle', SPARKLE)

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('app', type=Path)
parser.add_argument('--sparkle-bin', type=Path, required=True)
parser.add_argument('--output', type=Path, default=ROOT / 'build/releases')
args = parser.parse_args()
app = args.app.resolve()
info = plistlib.loads((app / 'Contents/Info.plist').read_bytes())
if info['CFBundleIdentifier'] != 'com.jacobcorbett.QuickRecorder2' or info.get('SUFeedURL') != FEED:
    parser.error('Build must have the Quick Recorder 2 identity and production feed.')
public_key = info.get('SUPublicEDKey')
expected_key = plistlib.loads((ROOT / 'QuickRecorder/Info.plist').read_bytes())['SUPublicEDKey']
if public_key != expected_key:
    parser.error('Build public signing key does not match the source configuration.')
subprocess.run(['codesign', '--verify', '--deep', '--strict', str(app)], check=True)
version, build = info['CFBundleShortVersionString'], info['CFBundleVersion']
args.output.mkdir(parents=True, exist_ok=True)
archive = args.output / f'QuickRecorder2-{version}.zip'
if archive.exists():
    parser.error(f'Refusing to replace existing release archive: {archive}')
with tempfile.TemporaryDirectory(prefix='qr2-release-') as directory:
    staging = Path(directory)
    subprocess.run(['ditto', str(app), str(staging / app.name)], check=True)
    for notice in ('LICENSE', 'THIRD_PARTY_NOTICES.md'):
        shutil.copyfile(ROOT / notice, staging / notice)
    (staging / 'SOURCE.txt').write_text(
        f'Quick Recorder 2 {version}\nCorresponding source: {REPO}/tree/v{version}\n'
        'Copyright 2024 lihaoyun6. Fork modifications copyright 2026 Jacob Corbett.\n'
        'GNU AGPLv3, without warranty. See LICENSE and THIRD_PARTY_NOTICES.md.\n')
    subprocess.run(['ditto', '-c', '-k', '--sequesterRsrc', str(staging), str(archive)], check=True)
signature = subprocess.check_output([str(args.sparkle_bin / 'sign_update'), '--account', 'QuickRecorder2', '-p', str(archive)], text=True).strip()
subprocess.run(['xcrun', 'swift', str(ROOT / 'scripts/verify-update.swift'), public_key, signature, str(archive)], check=True)
rss = ET.Element('rss', version='2.0')
channel = ET.SubElement(rss, 'channel')
ET.SubElement(channel, 'title').text = 'Quick Recorder 2 updates'
ET.SubElement(channel, 'link').text = REPO
item = ET.SubElement(channel, 'item')
ET.SubElement(item, 'title').text = f'Quick Recorder 2 {version}'
ET.SubElement(item, 'pubDate').text = formatdate(usegmt=True)
ET.SubElement(item, f'{{{SPARKLE}}}version').text = build
ET.SubElement(item, f'{{{SPARKLE}}}shortVersionString').text = version
ET.SubElement(item, f'{{{SPARKLE}}}minimumSystemVersion').text = info['LSMinimumSystemVersion']
ET.SubElement(item, f'{{{SPARKLE}}}releaseNotesLink').text = f'{REPO}/releases/tag/v{version}'
ET.SubElement(item, 'enclosure', url=f'{REPO}/releases/download/v{version}/{archive.name}', length=str(archive.stat().st_size), type='application/octet-stream', **{f'{{{SPARKLE}}}edSignature': signature})
feed_path = ROOT / 'updates/appcast.xml'
feed_path.parent.mkdir(exist_ok=True)
ET.indent(rss)
ET.ElementTree(rss).write(feed_path, encoding='utf-8', xml_declaration=True)
print(f'Archive: {archive}\nFeed: {feed_path}')
