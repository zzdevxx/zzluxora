"""
Project path resolution for ZZLUXORA.

Read-only bundled assets (fixtures, showfiles, icons) resolve relative to
``_MEIPASS`` when frozen with PyInstaller or the repository root in dev mode.
Writable runtime paths (user showfiles, custom fixtures, imported audio) map to
``%LOCALAPPDATA%/ZZLUXORA`` (Windows) or ``~/.local/share/ZZLUXORA`` (POSIX)
when running as a frozen executable so standard non-admin installs work cleanly.
"""

from __future__ import annotations

import os
import sys
from pathlib import Path


def is_frozen() -> bool:
    """Return True when executing from a PyInstaller frozen bundle."""
    return bool(getattr(sys, "frozen", False))


def bundle_root() -> Path:
    """Read-only bundle root (_MEIPASS when frozen, repository root in dev)."""
    if is_frozen():
        meipass = getattr(sys, "_MEIPASS", None)
        if meipass:
            return Path(meipass).resolve()
        return Path(sys.executable).resolve().parent
    return Path(__file__).resolve().parent.parent


# core/paths.py -> repository root in dev mode, or PyInstaller bundle root.
REPO_ROOT = bundle_root()


def user_data_dir() -> Path:
    """Writable directory for user data when installed, or REPO_ROOT in dev."""
    if not is_frozen():
        return REPO_ROOT
    if os.name == "nt":
        base = os.environ.get("LOCALAPPDATA") or os.environ.get("APPDATA") or str(Path.home())
        return Path(base).resolve() / "ZZLUXORA"
    xdg = os.environ.get("XDG_DATA_HOME")
    base_dir = Path(xdg) if xdg else Path.home() / ".local" / "share"
    return base_dir.resolve() / "ZZLUXORA"


def asset_path(*parts: str) -> Path:
    """Resolve a bundled UI asset path (for example ``asset_path('logo_zz.png')``)."""
    return bundle_root() / "ui" / "assets" / Path(*parts)


def fixtures_dir() -> Path:
    """Directory holding bundled fixture profiles (.zfx)."""
    return REPO_ROOT / "fixtures"


def showfiles_dir() -> Path:
    """Directory holding bundled show files (.zlx) and QLC+ workspaces (.qxw)."""
    return REPO_ROOT / "showfiles"


def audio_dir() -> Path:
    """Directory holding imported and bundled audio files."""
    return REPO_ROOT / "data" / "audio"


def docs_dir() -> Path:
    """Directory holding the project markdown documentation."""
    return REPO_ROOT / "markdowns"


def writable_fixtures_dir() -> Path:
    """Writable directory for custom fixture profiles (.zfx)."""
    return user_data_dir() / "fixtures" if is_frozen() else fixtures_dir()


def writable_showfiles_dir() -> Path:
    """Writable directory for user showfiles (.zlx)."""
    return user_data_dir() / "showfiles" if is_frozen() else showfiles_dir()


def writable_audio_dir() -> Path:
    """Writable directory for downloaded/imported audio files."""
    return user_data_dir() / "data" / "audio" if is_frozen() else audio_dir()


def ensure(directory: Path) -> Path:
    """Create the directory if needed and return it, for use in file dialogs."""
    directory.mkdir(parents=True, exist_ok=True)
    return directory


__all__ = [
    "REPO_ROOT",
    "asset_path",
    "audio_dir",
    "bundle_root",
    "docs_dir",
    "ensure",
    "fixtures_dir",
    "is_frozen",
    "showfiles_dir",
    "user_data_dir",
    "writable_audio_dir",
    "writable_fixtures_dir",
    "writable_showfiles_dir",
]
