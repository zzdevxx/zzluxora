"""Cross-repository parity verifier for the 4-repo ZZLUXORA ecosystem + portal."""

from __future__ import annotations

import hashlib
import json
import sys
import xml.etree.ElementTree as ET
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PERSONAL_ROOT = ROOT.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from core.version import APP_TAG, APP_VERSION


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as fp:
        for chunk in iter(lambda: fp.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def check_firmware_parity(failures: list[str]) -> None:
    fw_repo = PERSONAL_ROOT / "esp32-artnet-dmx"
    thesis_repo = PERSONAL_ROOT / "zzluxora-thesis"
    fw_dir = fw_repo / "firmware"
    thesis_artnet = thesis_repo / "artnet_projects"
    if not fw_repo.is_dir() or not thesis_repo.is_dir():
        print("[SKIP] esp32-artnet-dmx or zzluxora-thesis sibling not found.")
        return

    files = (
        "artnet_dmx_final.ino",
        "artnet_dmx_prompt.txt",
        "artnet_dmx_v1.txt",
        "artnet_dmx_v2.txt",
        "artnet_dmx_v3.txt",
        "artnet_dmx_v4.txt",
        "artnet_dmx_v5.txt",
    )
    for name in files:
        a = fw_dir / name
        b = thesis_artnet / name
        if not a.is_file() or not b.is_file():
            failures.append(f"Missing firmware file pair: {a} <-> {b}")
            continue
        if sha256_file(a) != sha256_file(b):
            failures.append(f"SHA-256 mismatch: {a} != {b}")
    print(f"[OK] Checked {len(files)} firmware files between esp32-artnet-dmx and zzluxora-thesis.")


def check_fixture_parity(failures: list[str]) -> None:
    fixture_repo = PERSONAL_ROOT / "zz-fixture"
    zfx_dir = ROOT / "fixtures"
    if not fixture_repo.is_dir():
        print("[SKIP] zz-fixture sibling not found.")
        return

    pairs = 0
    for qxf_path in sorted(fixture_repo.glob("*.qxf")):
        zfx_path = zfx_dir / f"{qxf_path.stem}.zfx"
        if not zfx_path.is_file():
            failures.append(f"Missing .zfx mirror in zzluxora/fixtures for {qxf_path.name}")
            continue
        tree = ET.parse(qxf_path)
        qxf_channels = [
            elem.attrib.get("Name", "")
            for elem in tree.getroot()
            if elem.tag.rsplit("}", 1)[-1] == "Channel"
        ]
        zfx_data = json.loads(zfx_path.read_text(encoding="utf-8"))
        zfx_channels = [ch.get("label", "") for ch in zfx_data.get("channels", [])]
        if len(qxf_channels) != len(zfx_channels) or zfx_channels != qxf_channels:
            failures.append(
                f"Channel mismatch for {qxf_path.stem}: qxf={qxf_channels} zfx={zfx_channels}"
            )
        pairs += 1
    if pairs == 0:
        failures.append("No .qxf fixture files found in zz-fixture root.")
    print(f"[OK] Checked {pairs} QXF <-> ZFX fixture definitions.")


def check_blackbox_parity(failures: list[str]) -> None:
    a = ROOT / "tools" / "verify_blackbox_fb.py"
    b = PERSONAL_ROOT / "zzluxora-thesis" / "tools" / "verify_blackbox_fb.py"
    if not b.is_file():
        print("[SKIP] zzluxora-thesis/tools/verify_blackbox_fb.py not found.")
        return
    if sha256_file(a) != sha256_file(b):
        failures.append(f"SHA-256 mismatch: {a} != {b}")
    else:
        print("[OK] verify_blackbox_fb.py matches zzluxora-thesis/tools/.")


def check_manifest_and_portal(failures: list[str]) -> None:
    manifest_path = ROOT / "release_manifest.json"
    dl_repo = PERSONAL_ROOT / "zzluxora-download"
    if not manifest_path.is_file():
        print("[INFO] release_manifest.json not yet generated (run build.py to generate).")
        return
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    if manifest.get("version") != APP_VERSION or manifest.get("tag") != APP_TAG:
        failures.append(
            f"release_manifest.json version mismatch: {manifest.get('tag')}/{manifest.get('version')} != {APP_TAG}/{APP_VERSION}"
        )
    if dl_repo.is_dir():
        dl_manifest = dl_repo / "release_manifest.json"
        if not dl_manifest.is_file():
            failures.append("zzluxora-download/release_manifest.json missing.")
        elif sha256_file(manifest_path) != sha256_file(dl_manifest):
            failures.append("zzluxora-download/release_manifest.json differs from zzluxora/release_manifest.json.")
        else:
            print("[OK] release_manifest.json matches zzluxora-download.")


def main() -> int:
    failures: list[str] = []
    check_firmware_parity(failures)
    check_fixture_parity(failures)
    check_blackbox_parity(failures)
    check_manifest_and_portal(failures)
    if failures:
        for item in failures:
            print(f"[FAIL] {item}", file=sys.stderr)
        return 1
    print("[PASS] Ecosystem cross-repo parity verified.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
