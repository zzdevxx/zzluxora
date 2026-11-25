"""Centralized ZZLUXORA release version metadata and update helpers."""

from __future__ import annotations

import json
import urllib.error
import urllib.request
from typing import Any

APP_NAME = "ZZLUXORA"
APP_VERSION = "10.0.0"
APP_TAG = "v10.0"
PORTAL_URL = "https://zzdree.my.id/zzluxora/"
RELEASES_API_URL = "https://api.github.com/repos/zzdevxx/zzluxora/releases/latest"
RELEASES_PAGE_URL = "https://github.com/zzdevxx/zzluxora/releases/latest"
ECOSYSTEM_REPOS = {
    "console": "https://github.com/zzdevxx/zzluxora",
    "firmware": "https://gitlab.com/zzdevxx/esp32-artnet-dmx",
    "fixtures": "https://github.com/zzdevxx/zz-fixture",
    "thesis": "https://gitlab.com/zzdevxx/zzluxora-thesis",
    "portal": PORTAL_URL,
}


def parse_version_tuple(raw: str) -> tuple[int, ...]:
    """Normalize version strings such as 'v10.1' or '10.1.0' into integer tuples."""
    cleaned = raw.strip().lstrip("vV").split("-", 1)[0]
    parts: list[int] = []
    for segment in cleaned.split("."):
        digits = "".join(ch for ch in segment if ch.isdigit())
        if not digits:
            break
        parts.append(int(digits))
    while len(parts) < 3:
        parts.append(0)
    return tuple(parts[:3])


def is_newer_version(candidate: str, current: str = APP_VERSION) -> bool:
    """Return True when candidate semantic version is strictly greater than current."""
    return parse_version_tuple(candidate) > parse_version_tuple(current)


def check_latest_release(timeout: float = 5.0) -> dict[str, Any]:
    """Fetch latest GitHub Release metadata for zzdevxx/zzluxora safely."""
    req = urllib.request.Request(
        RELEASES_API_URL,
        headers={
            "Accept": "application/vnd.github+json",
            "User-Agent": f"{APP_NAME}/{APP_VERSION}",
        },
    )
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            payload = json.loads(resp.read().decode("utf-8"))
        latest_tag = str(payload.get("tag_name") or APP_TAG)
        html_url = str(payload.get("html_url") or RELEASES_PAGE_URL)
        assets = payload.get("assets") or []
        installer = next(
            (a for a in assets if str(a.get("name", "")).lower().endswith(".exe")),
            None,
        )
        return {
            "ok": True,
            "current_version": APP_VERSION,
            "current_tag": APP_TAG,
            "latest_tag": latest_tag,
            "update_available": is_newer_version(latest_tag, APP_VERSION),
            "release_url": html_url,
            "portal_url": PORTAL_URL,
            "installer_name": installer.get("name") if installer else None,
            "installer_url": installer.get("browser_download_url") if installer else PORTAL_URL,
            "installer_size": installer.get("size") if installer else None,
        }
    except (urllib.error.URLError, TimeoutError, ValueError, OSError) as exc:
        return {
            "ok": False,
            "current_version": APP_VERSION,
            "current_tag": APP_TAG,
            "error": str(exc),
            "portal_url": PORTAL_URL,
            "release_url": RELEASES_PAGE_URL,
        }
