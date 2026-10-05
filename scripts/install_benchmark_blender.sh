#!/bin/bash
# Install the official 5.2.0 bundle without launching or changing an existing app.
set -euo pipefail
cd "$(dirname "$0")/.."
if [ -e /Applications/Blender.app ]; then echo 'Blender exists; preserve it and verify separately.'; exit 1; fi
stage=$(mktemp -d "$PWD/work/blender-install.XXXXXX")
mount="$stage/mount"
mkdir "$mount"
curl -fL https://download.blender.org/release/Blender5.2/blender-5.2.0-macos-arm64.dmg -o "$stage/blender.dmg"
echo "ed4d8390166dec5ea0a2813a03db6221f206ce016442be7f59f41d760972568a  $stage/blender.dmg" | shasum -a 256 -c -
trap 'hdiutil detach "$mount" >/dev/null 2>&1 || true' EXIT
hdiutil attach -nobrowse -readonly -mountpoint "$mount" "$stage/blender.dmg"
codesign --verify --deep --strict "$mount/Blender.app"
spctl --assess --type execute "$mount/Blender.app"
ditto "$mount/Blender.app" "$stage/Blender.app"
codesign --verify --deep --strict "$stage/Blender.app"
test ! -e /Applications/Blender.app
mv "$stage/Blender.app" /Applications/Blender.app
hdiutil detach "$mount"
trap - EXIT
rm -rf "$stage"
echo 'Official Blender 5.2.0 installed and verified; not launched.'
