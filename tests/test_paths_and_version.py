"""Tests for core.version and frozen-aware core.paths resolution."""

from __future__ import annotations

import os
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from core import paths, version


class TestVersionAndPaths(unittest.TestCase):
    def test_version_constants_and_comparison(self) -> None:
        self.assertEqual(version.APP_VERSION, "10.1.0")
        self.assertEqual(version.APP_TAG, "v10.1")
        self.assertTrue(version.is_newer_version("v10.2", "10.1.0"))
        self.assertTrue(version.is_newer_version("10.10.0", "10.9.0"))
        self.assertFalse(version.is_newer_version("v10.1", "10.1.0"))
        self.assertFalse(version.is_newer_version("9.9.9", "10.1.0"))

    def test_main_runs_from_external_working_directory(self) -> None:
        import subprocess
        main_script = paths.REPO_ROOT / "main.py"
        clean_env = {k: v for k, v in os.environ.items() if k != "PYTHONPATH"}
        with tempfile.TemporaryDirectory() as external_cwd:
            proc = subprocess.run(
                [sys.executable, str(main_script), "--help"],
                cwd=external_cwd,
                env=clean_env,
                capture_output=True,
                text=True,
                timeout=20,
            )
            self.assertEqual(proc.returncode, 0, proc.stderr)
            self.assertIn("ZZLUXORA v10.1.0", proc.stdout)

    def test_dev_paths_point_inside_repo_and_logo_exists(self) -> None:
        self.assertFalse(paths.is_frozen())
        self.assertEqual(paths.writable_fixtures_dir(), paths.fixtures_dir())
        self.assertEqual(paths.writable_showfiles_dir(), paths.showfiles_dir())
        self.assertEqual(paths.writable_audio_dir(), paths.audio_dir())
        self.assertTrue(paths.asset_path("logo_zz.png").is_file())

    def test_frozen_paths_use_meipass_and_localappdata(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            bundle = Path(tmp) / "bundle"
            local = Path(tmp) / "local"
            with (
                patch.object(sys, "frozen", True, create=True),
                patch.object(sys, "_MEIPASS", str(bundle), create=True),
                patch.dict(os.environ, {"LOCALAPPDATA": str(local)}, clear=False),
            ):
                self.assertTrue(paths.is_frozen())
                self.assertEqual(paths.bundle_root(), bundle.resolve())
                if os.name == "nt":
                    self.assertEqual(paths.user_data_dir(), local.resolve() / "ZZLUXORA")
                    self.assertEqual(
                        paths.writable_audio_dir(),
                        local.resolve() / "ZZLUXORA" / "data" / "audio",
                    )


if __name__ == "__main__":
    unittest.main()
