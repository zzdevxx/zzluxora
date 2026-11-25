# CLAUDE.md | ZZLUXORA (Production Stage Lighting Console)

Panduan arsitektur, instruksi pengembangan, dan konteks operasional untuk **ZZLUXORA** (mulai rilis `v10.0` / `10.0.0`, skema inkremental `+0.1`; GrandMA Industrial Console Architecture | Anti-Slop Professional Edition).

---

## MULAI DARI SINI (WAJIB DIBACA)

**Baca `HANDOFF.md` di akar repo lebih dulu.** Dokumen itu memuat status terkini, apa yang sudah selesai (jangan dikerjakan ulang), apa yang belum, jebakan Qt yang harus diketahui, preferensi desain owner, dan lokasi memori.

Perintah wajib:
```powershell
# Windows PowerShell (venv Python 3.15.2)
$env:PYTHONPATH="$PWD\tools"; .\.venv\Scripts\python.exe tools\run_tests_guarded.py   # 197 test unik (166 unittest + 31 pytest), tanpa popup
node scripts/check-anti-slop.js --summary                                             # audit anti-slop kode dan dokumentasi
python D:\ANDREAS\PERSONAL\agent-memory\tools\memlog.py search "kata kunci"           # memori agen lintas proyek
```

---

## 1. Ikhtisar & Identitas Proyek

- **Nama Aplikasi:** **ZZLUXORA** (`core/version.py`: `v10.0` / `10.0.0`, naik `+0.1` tiap rilis)
- **Repositori (origin):** `https://gitlab.com/zzdevxx/zzluxora.git` (Branch: `main`); mirror: `codeberg` dan `github`. Portal unduhan: `https://zzdree.my.id/zzluxora/` (`zzdevxx/zzluxora-download`).
- **Peneliti / Pengembang:** Andreas Restuawanta Christwara (`NIM: 5312422036`)
- **Dosen Pembimbing:** Mario Norman Syah, S.Pd., M.Eng.
- **Institusi:** Program Studi S1 Teknik Komputer, Fakultas Teknik, Universitas Negeri Semarang (UNNES)
- **Karakter Desain:** Modern-minimalis industri panggung pertunjukan (mengadopsi estetika **grandMA2 / grandMA3 onPC** dan utilitas **QLC+**).
- **Format Showfile Project:** `.zlx` (JSON showfile).
- **Format Profil Fixture:** `.zfx` (JSON profil lampu berstandar QLC+).

---

## 2. Arsitektur Perangkat Lunak (Clean Modular Architecture | Feedback v3)

Aplikasi dibangun menggunakan **Python 3.10+** (runtime aktif `.venv`: **Python 3.15.2** CPython standar) dan **Universal Qt6 Compatibility Layer (`ui/qt_compat.py`)** yang mendukung **PySide6** maupun **PyQt6** secara transparan:

```text
zzluxora/
├── core/                      # PURE PYTHON ENGINE (ZERO-GUI DEPENDENCY)
│   ├── __init__.py
│   ├── audio_loader.py        # Pemuat audio multi-format (.wav, .mp3, .flac, .ogg)
│   ├── fft_engine.py          # STFT engine (Hann Window, N=2048, H=512, fs=22050, laju analisis 43.07 FPS; FFT via np.fft.rfft)
│   ├── feature_extractor.py   # Ekstraksi RMS, Spectral Centroid, Chroma 12-semitone, MFCC, Flux
│   ├── emotion_model.py       # Model Afektif Russell 2D Plane (Valence-Arousal)
│   ├── color_engine.py        # Konversi (V, A, RMS) -> HSV -> RGB -> Physical 4-Kanal RGBW
│   ├── artnet_sender.py       # Transmisi UDP socket Port 6454 ke Node DMX (530-byte ArtDmx, Universe 0)
│   ├── models.py              # Data structures: Fixture, Patch, Scene, Chase, ProjectState
│   └── project_io.py          # Serialisasi & Deserialisasi berkas .zlx & .zfx
│
├── ui/                        # USER INTERFACE (PYSIDE6 / PYQT6 DUAL-BINDING COMPATIBLE)
│   ├── __init__.py
│   ├── qt_compat.py           # Universal Qt6 binding compatibility layer with automatic enum promotion
│   ├── styles.py              # Pure Dark Grey (#1e2024 - #282c34), high-contrast white text, master QSS
│   ├── icons.py               # Vektor SVG icons & custom painter helpers
│   ├── assets/                # Asset resmi logo & icon (logo_zz.png 1024x1024, logo_zz.ico multi-size)
│   ├── main_window.py         # Root window, pure native QMenuBar, program view bar, telemetry, blackout
│   ├── panels/
│   │   ├── address_tab.py     # Grid DMX Address 512 kanal (20 kolom horizontal, color-coded, 46x46)
│   │   ├── analyze_tab.py     # Core skripsi audio analyzer, YouTube downloader, non-blocking DSP
│   │   ├── result_tab.py      # Metrik afektif Russell 2D, kuadran mood, export to perform
│   │   ├── perform_tab.py     # Live show controller, playlist reordering, cue transitions
│   │   ├── page_tab.py        # Virtual executor sheet (clean blank start, flash triggers)
│   │   ├── mixer_tab.py       # 513 Slider fader (1 Grand Master + 512 DMX) grandMA style (190px compact)
│   │   ├── fixture_list.py    # Floating window: Drawer fixture & drag-and-drop patching
│   │   ├── fixture_editor.py  # Floating window: QLC+ style fixture definition editor (.zfx)
│   │   ├── preview_tab.py     # Floating window: Visualizer panggung 2D multi-screen support
│   │   ├── settings_panel.py  # Floating window: Konfigurasi IP Art-Net (127.0.0.1, 192.168.4.1, Custom)
│   │   ├── help_panel.py      # Floating window: Panduan penggunaan & tabel keyboard shortcuts
│   │   └── about_panel.py     # Floating window: Lembar informasi akademis & identitas pengembang
│   └── widgets/
│       ├── tactile_fader.py   # Custom grandMA fader widget (rel LED menyala, cap bertakik, garis kalibrasi)
│       └── youtube_dialog.py  # Pop-up mandiri pengunduh audio YouTube ke data/audio/ lokal
│
├── markdowns/                 # 7 DOKUMEN REKAYASA SISTEMATIS LENGKAP
│   ├── DESIGN.md              # Spesifikasi sistem desain grandMA, token, responsivitas 768p/1080p
│   ├── PRD.md                 # Product Requirements Document & spesifikasi fungsional
│   ├── ARCHITECTURE.md        # Arsitektur sistem, threading model, & skema data
│   ├── COMPONENT_SPEC.md      # Spesifikasi detail setiap komponen antarmuka
│   ├── STATE_MANAGEMENT.md    # Global QUndoStack, DMX buffer, & Art-Net state machine
│   ├── TEST_PLAN.md           # Rencana pengujian berjenjang (Unit, SITL, Lapangan)
│   └── ROADMAP.md             # Rencana aksi eksekusi Big Plan v3 bertahap
│
├── fixtures/                  # 5 Preset profil lampu resmi (.zfx saja)
│   ├── Alien-AL36.zfx         # 8CH RGB (Dimmer, RGB, Empty, Program, Speed, Emptz)
│   ├── Illumsolid-YSP01.zfx   # 8CH RGBW (Dimmer, RGBW, Program, Empty, Emptz)
│   ├── Kumastb-STL47.zfx      # 8CH RGBW (Dimmer, RGBW, Strobe, Program, Speed)
│   ├── Wisdom-54X3.zfx        # 8CH RGB (Dimmer, Strobe, Effect, Speed, RGB, Empty)
│   └── zzdree-36X.zfx         # 3CH pure RGB (Red, Green, Blue, tanpa kanal Dimmer)
│
├── showfiles/                 # Berkas pertunjukan live (.zlx) & simulasi (.qxw)
│   ├── zzdree_36x_4x.zlx      # Showfile resmi aktif 4x zzdree-36X (DMX 1, 17, 33, 49)
│   ├── demo_church_worship.zlx # Berkas proyek demo resmi (File -> Open Project...)
│   ├── gia_deliksari_alien_4x.zlx # Showfile 4x Alien AL36 panggung GIA (DMX 1, 17, 33, 49)
│   ├── bench_kumastb_stl47.zlx # Showfile 1x Kumastb STL47 bench test RGBW (DMX 1)
│   ├── qlcplus_template.qxw   # Template SITL loopback QLC+ (8CH)
│   └── zzluxora_test.qxw      # Workspace pengujian visualizer loopback
│
├── tests/                     # 15 berkas, 197 test unik (166 unittest + 31 pytest)
│   ├── test_fft_engine.py, test_audio_loader.py, test_feature_extractor.py
│   ├── test_emotion_model.py, test_color_engine.py, test_artnet_sender.py
│   ├── test_project_io.py, test_ui_components.py, test_audit_regressions.py
├── requirements.txt           # Dependensi pustaka Python
├── README.md                  # Dokumentasi proyek
└── main.py                    # Entry point aplikasi (Instant launch, clean blank start)
```

---

## 3. Spesifikasi UI/UX & Standar Mutu (Feedback v3 Full Alignment)

1. **Peluncuran Instan (Zero Splashscreen) & Clean Initial State:**
   - Aplikasi terbuka seketika (*instant cold launch* < 500 ms) menyerupai QLC+, tanpa jeda splash screen.
   - Tampilan awal 100% kosong (*clean blank state* tanpa demo otomatis). Berkas showfile resmi tersedia di `showfiles/zzdree_36x_4x.zlx` dan `showfiles/demo_church_worship.zlx`.
2. **Transmisi Art-Net Play-Gated & Skalasi Dimmer Fixture 3CH RGB:**
   - Paket UDP Art-Net Port 6454 **HANYA DIKIRIMKAN ketika tombol PLAY aktif** (`is_transmitting == True`). Ketika Play belum ditekan, pergerakan fader hanya memperbarui GUI internal tanpa memancarkan paket ke jaringan.
   - Pada `_get_target_dmx_for_cue`, fixture tanpa kanal dimmer (seperti `zzdree-36X` 3CH RGB) menskalakan nilai RGB(W) secara proporsional terhadap `intensity / 255.0` sehingga fade black, blackout cue, dan dimmer parsial bekerja penuh tanpa memengaruhi fixture ber-dimmer.
3. **Hierarki Header Desktop Standar:**
   - **OS Window Title Bar:** Memuat logo resmi `ZZ` (Arial Black Italic, solid black, pure white, no glow) dan judul format bersih: `ZZLUXORA [NamaProject.zlx]`.
   - **Main Menu Bar (Native QMenuBar):** Pure menu bar (`File`, `Fixture`, `Preview`, `Setting`, `Help`, `About`) tanpa duplikasi logo/nama app di dalamnya.
   - **Program View Bar:** Sisi kiri memuat 6 tab workspace, sisi kanan memuat badge status Art-Net (klik membuka Setting), tombol Blackout, dan tombol Play/Stop toggle.
4. **Desain Anti-Slop (No Emojis & Industrial Console Look):**
   - Bebas dari emoji di tombol/header.
   - Menggunakan pemisah teknis standar konsol: pipa `|` atau titik dua `:`, tanpa em-dash dekoratif.
   - Kode channel visual di Tab Address: `DIM`, `RED`, `GRN`, `BLU`, `WHT`, `STR`, `FX`.
5. **Jendela Pop-up Mandiri (Floating Windows):**
   - `Fixture List`, `Fixture Editor`, `Stage Visualizer (2D & 3D Perspective with Volumetric Beams & Haze/Smoke FX)`, `Settings`, `Help`, `About` adalah jendela pop-up non-modal independen dengan kontrol *Minimize, Maximize, Close*.
6. **Enam Tab Utama Program (Workspaces):**
   - `Tab 1: Address`: Grid 512 kanal DMX (20 kolom horizontal, warna sel mengikuti tipe kanal, Clear All dengan konfirmasi, Undo `Ctrl+Z` / Redo `Ctrl+Shift+Z`, tombol `PATCH` langsung memasang 4x `zzdree-36X` 3CH RGB pada DMX001/017/033/049 = 12 kanal total).
   - `Tab 2: Analyze`: Audio file loader, YouTube audio downloader & converter otomatis, tombol Analyze & Remove, analisis asinkron non-blocking dengan efek blur/dimmed pada area analisis dan tips saintifik DSP.
   - `Tab 3: Result`: Dashboard metrik analisis lengkap (12 parameter: RMS Energy, Spectral Centroid Hz, Chroma STFT 12-Semitone + Deteksi Tonalitas Mayor/Minor, MFCC Density, Spectral Flux, Russell 2D V-A plane, BPM, kuadran mood Praise/Worship, dan Dekomposisi Physical RGBW).
   - `Tab 4: Perform`: Manajemen urutan playlist pertunjukan panggung, auto-populate section cues lagu (Intro/Verse/Chorus/Bridge/Ending), master playback `[GO+]`, `[PREV]`, `[FADE BLACK]`, dan smooth cosine crossfading.
   - `Tab 5: Page`: Lembar tombol virtual executor untuk eksekusi instan suasana panggung (Praise, Worship, Strobe Flash).
   - `Tab 6: Mixer`: Meja 513 fader fisik dengan Grand Master fader lebih tinggi & dominan (230px, 68px), tombol cepat `[x]` clear/zero pada setiap fader, bilah navigasi lompat cepat Bank Fader 1 s.d. 8, tag fader ringkas (`36X-1:RED`, `AL36-1:DIM`, `YSP01-1:DIM`, `54X3-1:FX`), *tactile ribbed cap*, *illuminated groove rail*, dan garis skala kalibrasi analog.

---

## 4. Kompatibilitas Multi-Platform & Responsivitas Layar

- **Development & Deployment Utama:** Windows 11 (Laptop Acer Swift 3, `D:\ANDREAS\PERSONAL\zzluxora`, 1920x1080, `.venv` Python 3.15.2).
- **Kompatibilitas Layar Kecil (768p):** Tetap terjaga untuk resolusi 1366x768.
- **Aturan Sizing Responsif:**
  * Default window size: `1200 x 680` px (pas di layar 768p tanpa terpotong panel OS).
  * Minimum window size: `960 x 560` px.
  * Tinggi fader disesuaikan ke `190px` (lebar `52px`) agar pas dan padat di 768p dan meregang elastis di 1080p.
  * Sel grid DMX berukuran `46x46px` (20 kolom = 920px, muat lega di layar 1366px).

---

## 5. Disiplin Git & Sinkronisasi

1. Repositori GitLab `zzdevxx/zzluxora` dan `zzdevxx/zzluxora-thesis` (origin) adalah **Single Source of Truth**; Codeberg dan GitHub adalah mirror. Verifikasi paritas 4-repo dijalankan lewat `python tools/verify_ecosystem.py`.
2. Setiap fitur yang selesai diuji wajib di-commit dan di-push ke branch `main` menggunakan `sync_cloud.py` saat pemilik meminta sinkronisasi.
3. Jangan commit atau push tanpa konfirmasi pemilik.

---

## 6. Design System Impeccable & Status Pengujian

**Integrasi Impeccable Design System (7 Okt 2026, commit `f938987`):**
- `PRODUCT.md` (akar repo): kebenaran produk tahan-lama skema Impeccable 1 | platform desktop, pengguna LD/FOH, mode *operate*, komitmen merek industrial, prinsip produk.
- `DESIGN.md` (akar repo): spesifikasi sistem desain bertoken (YAML frontmatter) dengan Creative North Star **"The Obsidian Control Deck"**, *10% accent rule*, skala tipografi 4-tier ber-`tabular-nums`, matriks 7-state interaktif, dan aturan anti-slop.
- `markdowns/DESIGN.md`: ringkasan token untuk kerja UI harian.

**Aturan kerja wajib untuk agent:**
1. **Semua warna UI wajib dari token `Theme` di `ui/styles.py`** | hex inline dilarang (hanya `ui/styles.py` dan `ui/icons.py` yang boleh memuat literal hex).
2. **Anti-slop keras:** tanpa emoji di chrome UI dan heading, tanpa em-dash/en-dash (`|` atau `-`), tanpa glow/cyberpunk palsu, tanpa biru web generik untuk aksi utama (hijau `#16a34a` / amber / cyan sesuai `DESIGN.md`).
3. **Kontras WCAG:** teks pada fill channel terang (amber, cyan, yellow, dll) wajib pakai `Theme.SURFACE_VOID`; gelap -> `Theme.TEXT_PRIMARY`. Peta lengkap di `ui/panels/address_tab.py::update_style`.
4. **Test wajib sebelum commit:** `$env:PYTHONPATH="$PWD\tools"; .\.venv\Scripts\python.exe tools\run_tests_guarded.py` -> saat ini **197 test unik lulus** (166 unittest + 31 pytest, exit 0). Wrapper ini menetralkan QMessageBox/QFileDialog/QInputDialog lebih dulu sehingga tidak ada popup yang muncul di layar operator saat pengujian. Perintah lama `python -m unittest discover -s tests -p "test_*.py"` tidak direkomendasikan karena dapat memunculkan popup dialog. Audit anti-slop: 0 error, 0 warning.
5. **Ditunda:** *Live Cue Ribbon* (swatch RGBW + pan/tilt per cue) menunggu arahan owner.

**Status uji terakhir:** 197 test unik OK (166 unittest [1 skipped] + 31 pytest) | Python 3.15.2 `.venv` | audit anti-slop bersih (0 error, 0 warning) | jalankan via `tools/run_tests_guarded.py`.
