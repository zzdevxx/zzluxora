"""
about_panel.py | Academic Thesis Information & Software Credentials Dialog
Presents official student credentials, advisor information, UNNES affiliation, and research title.
"""

from __future__ import annotations

import threading

from core.paths import asset_path
from core.version import (
    APP_TAG,
    APP_VERSION,
    ECOSYSTEM_REPOS,
    PORTAL_URL,
    check_latest_release,
)
from ui.qt_compat import (
    HAS_QT, QDialog, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QFrame, QPushButton,
    QScrollArea, QPixmap, QIcon, Qt
)
from ui.styles import Theme, CONSOLE_QSS


class AboutDialog(QDialog if HAS_QT else object):
    """About Dialog: Academic Thesis Metadata & Software Credentials."""
    def __init__(self, parent: QWidget | None = None):
        if not HAS_QT: return
        super().__init__(parent)
        self.setWindowFlags(Qt.Window | Qt.WindowMinMaxButtonsHint | Qt.WindowCloseButtonHint)
        self.setWindowTitle("About")
        self.resize(740, 620)
        self.setStyleSheet(CONSOLE_QSS)

        logo_path = asset_path("logo_zz.png")
        if logo_path.exists():
            self.setWindowIcon(QIcon(str(logo_path)))

        self._init_ui()

    def _init_ui(self) -> None:
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(20, 18, 20, 18)
        main_layout.setSpacing(12)

        logo_path = asset_path("logo_zz.png")

        # Header Row (Official Logo Badge + Title)
        header_row = QHBoxLayout()
        header_row.setSpacing(14)
        if logo_path.exists():
            logo_lbl = QLabel()
            pix = QPixmap(str(logo_path)).scaled(48, 48, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            logo_lbl.setPixmap(pix)
            logo_lbl.setFixedSize(48, 48)
            logo_lbl.setStyleSheet("border-radius: 4px; background: transparent;")
            header_row.addWidget(logo_lbl)

        title_box = QVBoxLayout()
        title = QLabel(f"ZZLUXORA ({APP_TAG})")
        title.setStyleSheet(f"font-size: 16px; font-weight: 800; color: {Theme.TEXT_PRIMARY};")
        subtitle = QLabel("Intelligent Audio-Reactive Stage Lighting Controller | Computer Engineering FT UNNES")
        subtitle.setStyleSheet(f"font-size: 11px; color: {Theme.ACCENT_CYAN};")
        title_box.addWidget(title)
        title_box.addWidget(subtitle)
        header_row.addLayout(title_box)
        header_row.addStretch()
        main_layout.addLayout(header_row)

        # Scrollable Content Card for spacious readability
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet(f"""
            QScrollArea {{
                border: 1px solid {Theme.BORDER_STRONG};
                border-radius: 6px;
                background-color: {Theme.BG_SURFACE};
            }}
        """)

        card = QWidget()
        card_layout = QVBoxLayout(card)
        card_layout.setContentsMargins(16, 14, 16, 14)
        card_layout.setSpacing(10)

        fields = [
            ("Application", f"ZZLUXORA ({APP_TAG} / v{APP_VERSION} Next-Gen Production Stage Console)"),
            ("Description", "Audio-Reactive Stage Lighting Design System based on Worship Music Mood Analysis with HSV-RGBW Color Mapping and Art-Net DMX512 Protocol."),
            ("Researcher", "Andreas Restuawanta Christwara"),
            ("Student ID (NIM)", "5312422036"),
            ("Study Program", "S1 Teknik Komputer (Computer Engineering)"),
            ("Department", "Teknik Elektro (Electrical Engineering)"),
            ("Faculty", "Fakultas Teknik (Faculty of Engineering)"),
            ("University", "Universitas Negeri Semarang (UNNES)"),
            ("Thesis Advisor", "Mario Norman Syah, S.Pd., M.Eng."),
            ("Research Title", "Rancang Bangun Sistem Audio-Reactive Lighting Design Berbasis Analisis Mood Lagu Rohani dengan Pemetaan Warna HSV-RGBW dan Protokol Art-Net DMX512"),
            ("Field Location", "Gereja Isa Almasih (GIA) Deliksari, Kota Semarang"),
        ]

        for label_text, val_text in fields:
            row = QHBoxLayout()
            row.setSpacing(12)
            lbl = QLabel(label_text + ":")
            lbl.setFixedWidth(135)
            lbl.setAlignment(Qt.AlignTop | Qt.AlignLeft)
            lbl.setStyleSheet(f"font-weight: 700; color: {Theme.TEXT_SECONDARY}; font-size: 12px;")

            val = QLabel(val_text)
            val.setWordWrap(True)
            val.setStyleSheet(f"color: {Theme.TEXT_PRIMARY}; font-size: 12px; line-height: 1.4;")

            row.addWidget(lbl)
            row.addWidget(val, 1)
            card_layout.addLayout(row)

        ecosystem_links = [
            ("Release Portal", PORTAL_URL, "zzdree.my.id/zzluxora/"),
            ("Console Repo", ECOSYSTEM_REPOS["console"], "github.com/zzdevxx/zzluxora"),
            ("ESP32 Firmware", ECOSYSTEM_REPOS["firmware"], "gitlab.com/zzdevxx/esp32-artnet-dmx"),
            ("Fixture Library", ECOSYSTEM_REPOS["fixtures"], "github.com/zzdevxx/zz-fixture"),
            ("Thesis Repo", ECOSYSTEM_REPOS["thesis"], "gitlab.com/zzdevxx/zzluxora-thesis"),
        ]
        for label_text, url, display in ecosystem_links:
            row = QHBoxLayout()
            row.setSpacing(12)
            lbl = QLabel(label_text + ":")
            lbl.setFixedWidth(135)
            lbl.setAlignment(Qt.AlignTop | Qt.AlignLeft)
            lbl.setStyleSheet(f"font-weight: 700; color: {Theme.TEXT_SECONDARY}; font-size: 12px;")

            val = QLabel(f'<a href="{url}" style="color: {Theme.ACCENT_CYAN}; text-decoration: none;">{display}</a>')
            val.setOpenExternalLinks(True)
            val.setTextInteractionFlags(Qt.TextBrowserInteraction)
            val.setStyleSheet(f"color: {Theme.ACCENT_CYAN}; font-size: 12px;")

            row.addWidget(lbl)
            row.addWidget(val, 1)
            card_layout.addLayout(row)

        card_layout.addStretch()
        scroll.setWidget(card)
        main_layout.addWidget(scroll, 1)

        # Bottom Status + Check Update + Close Button
        btn_bar = QHBoxLayout()
        self._update_status = QLabel(f"Current build: {APP_TAG} ({APP_VERSION})")
        self._update_status.setOpenExternalLinks(True)
        self._update_status.setStyleSheet(f"font-size: 11px; color: {Theme.TEXT_SECONDARY};")
        btn_bar.addWidget(self._update_status, 1)

        self._btn_check_update = QPushButton("Check Updates")
        self._btn_check_update.setStyleSheet("min-width: 110px; padding: 6px 14px; border-radius: 4px;")
        self._btn_check_update.clicked.connect(self._on_check_updates)
        btn_bar.addWidget(self._btn_check_update)

        btn_close = QPushButton("Close")
        btn_close.setStyleSheet("min-width: 80px; padding: 6px 14px; border-radius: 4px;")
        btn_close.clicked.connect(self.close)
        btn_bar.addWidget(btn_close)
        main_layout.addLayout(btn_bar)

    def _on_check_updates(self) -> None:
        self._btn_check_update.setEnabled(False)
        self._update_status.setText("Checking GitHub Releases...")

        def _worker() -> None:
            from ui.qt_compat import QTimer

            # Button must leave the busy state on every path: an unexpected API
            # payload or worker exception must not strand About on "Checking".
            result = {"ok": False, "error": "update check did not return a result"}
            try:
                result = check_latest_release()
            except Exception as exc:
                result = {"ok": False, "error": str(exc)}
            finally:
                def _apply() -> None:
                    self._btn_check_update.setEnabled(True)
                    if not result.get("ok"):
                        self._update_status.setText(
                            f'Offline or rate-limited. Portal: <a href="{PORTAL_URL}" style="color: {Theme.ACCENT_CYAN};">zzdree.my.id/zzluxora/</a>'
                        )
                        return
                    latest_tag = result.get("latest_tag")
                    if result.get("update_available"):
                        self._update_status.setText(
                            f'Update {latest_tag} ready: <a href="{PORTAL_URL}" style="color: {Theme.ACCENT_CYAN};">Download from portal</a>'
                        )
                    else:
                        self._update_status.setText(f"Up to date ({APP_TAG} / latest remote {latest_tag}).")

                QTimer.singleShot(0, self, _apply)

        threading.Thread(target=_worker, daemon=True).start()
