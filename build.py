"""PyInstaller + Inno Setup release builder for ZZLUXORA."""

from __future__ import annotations

import hashlib
import json
import os
import shutil
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))

from core.version import APP_TAG, APP_VERSION, ECOSYSTEM_REPOS, PORTAL_URL

DIST_APP_DIR = ROOT / "dist" / "ZZLUXORA"
DIST_INSTALLER_DIR = ROOT / "dist" / "installer"
ISS_SCRIPT = ROOT / "installer" / "zzluxora.iss"
DEFAULT_ISCC = Path(os.environ.get("LOCALAPPDATA", "")) / "Programs" / "Inno Setup 6" / "ISCC.exe"


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as fp:
        for chunk in iter(lambda: fp.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def run_step(cmd: list[str], label: str) -> None:
    print(f"\n==> {label}: {' '.join(cmd)}")
    proc = subprocess.run(cmd, cwd=str(ROOT))
    if proc.returncode != 0:
        raise RuntimeError(f"{label} failed with exit code {proc.returncode}")


def main() -> int:
    installer_name = f"ZZLUXORA-Setup-{APP_VERSION}.exe"
    if "--manifest-only" not in sys.argv:
        for clean_dir in (ROOT / "build" / "ZZLUXORA", DIST_APP_DIR):
            if clean_dir.exists():
                shutil.rmtree(clean_dir)

        icon_arg = f"--icon={ROOT / 'ui' / 'assets' / 'logo_zz.ico'}"
        pyinstaller_cmd = [
            sys.executable,
            "-m",
            "PyInstaller",
            "--noconfirm",
            "--clean",
            "--windowed",
            "--onedir",
            "--name=ZZLUXORA",
            icon_arg,
            "--add-data", f"{ROOT / 'ui' / 'assets'};ui/assets",
            "--add-data", f"{ROOT / 'fixtures'};fixtures",
            "--add-data", f"{ROOT / 'showfiles'};showfiles",
            "--add-data", f"{ROOT / 'LICENSE'};.",
            "--hidden-import=yt_dlp",
            "--collect-submodules=yt_dlp",
            "--collect-binaries=imageio_ffmpeg",
            "--collect-data=imageio_ffmpeg",
            "--exclude-module=tkinter",
            "--exclude-module=matplotlib",
            "--exclude-module=scipy",
            "--exclude-module=librosa",
            str(ROOT / "main.py"),
        ]
        run_step(pyinstaller_cmd, "PyInstaller bundle build")

        exe_path = DIST_APP_DIR / "ZZLUXORA.exe"
        if not exe_path.is_file():
            raise FileNotFoundError(f"Expected built binary missing: {exe_path}")

        run_step([str(exe_path), "--cli", "--duration", "0.5"], "Smoke test frozen CLI")

        iscc = Path(shutil.which("ISCC.exe") or DEFAULT_ISCC)
        if not iscc.is_file():
            raise FileNotFoundError(f"Inno Setup compiler ISCC.exe not found at {iscc}")
        DIST_INSTALLER_DIR.mkdir(parents=True, exist_ok=True)
        run_step(
            [str(iscc), f"/DMyAppVersion={APP_VERSION}", str(ISS_SCRIPT)],
            "Inno Setup 6 installer compilation",
        )

    installer_path = DIST_INSTALLER_DIR / installer_name
    if not installer_path.is_file():
        raise FileNotFoundError(f"Expected installer missing: {installer_path}")

    manifest = {
        "app": "ZZLUXORA",
        "tag": APP_TAG,
        "version": APP_VERSION,
        "increment_step": "+0.1",
        "released_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "installer_name": installer_name,
        "installer_size_bytes": installer_path.stat().st_size,
        "installer_size_mb": round(installer_path.stat().st_size / (1024 * 1024), 1),
        "installer_sha256": sha256_file(installer_path),
        "download_url": f"https://github.com/zzdevxx/zzluxora/releases/download/{APP_TAG}/{installer_name}",
        "release_url": f"https://github.com/zzdevxx/zzluxora/releases/tag/{APP_TAG}",
        "portal_url": PORTAL_URL,
        "ecosystem": ECOSYSTEM_REPOS,
    }
    manifest_text = json.dumps(manifest, indent=2) + "\n"
    (ROOT / "release_manifest.json").write_text(manifest_text, encoding="utf-8")
    dl_dir = ROOT.parent / "zzluxora-download"
    if dl_dir.is_dir():
        (dl_dir / "release_manifest.json").write_text(manifest_text, encoding="utf-8")

    print("\n=== BUILD SUMMARY ===")
    print(manifest_text)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
