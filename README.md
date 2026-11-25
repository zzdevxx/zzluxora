# ZZLUXORA v10.0 | Intelligent Stage Lighting Console

[![Release](https://img.shields.io/badge/Release-v10.0.0-16a34a?style=flat-square)](https://github.com/zzdevxx/zzluxora/releases/latest)
[![Portal](https://img.shields.io/badge/Web%20Portal-zzdree.my.id%2Fzzluxora-2563eb?style=flat-square)](https://zzdree.my.id/zzluxora/)
[![Python](https://img.shields.io/badge/Python-3.10%2B%20%7C%203.15.2-3776AB?style=flat-square&logo=python&logoColor=white)](https://python.org)
[![Qt](https://img.shields.io/badge/PySide6-Qt6-41CD52?style=flat-square&logo=qt)](https://doc.qt.io/qtforpython/)
[![Tests](https://img.shields.io/badge/Tests-200%20passing-brightgreen?style=flat-square)](https://github.com/zzdevxx/zzluxora)
[![License](https://img.shields.io/badge/License-Apache--2.0-blue?style=flat-square)](LICENSE)

> **Portal Unduhan Resmi:** [`https://zzdree.my.id/zzluxora/`](https://zzdree.my.id/zzluxora/) (Installer Windows `ZZLUXORA-Setup-10.0.0.exe` & Simulator DMX512 Interaktif).  
> Skema rilis naik `+0.1` per pembaruan mulai dari **`v10.0`** (`10.0.0` -> `v10.1` / `10.1.0` -> `v10.2` ...), menggantikan arsip seri lama (`zzluxora-v7`, `zzluxora-v8`, `zzluxora-v8.5`, `zzluxora-v9`).


> **Tugas Akhir / Skripsi Sarjana Teknik Komputer**  
> **Judul:** *"Rancang Bangun Sistem Audio-Reactive Lighting Design Berbasis Analisis Mood Lagu Rohani dengan Pemetaan Warna HSV-RGBW dan Protokol Art-Net DMX512"*  
> **Peneliti:** Andreas Restuawanta Christwara (`NIM: 5312422036`)  
> **Dosen Pembimbing:** Mario Norman Syah, S.Pd., M.Eng.  
> **Institusi:** Program Studi S1 Teknik Komputer, Jurusan Teknik Elektro, Fakultas Teknik, Universitas Negeri Semarang (UNNES)

---

## Ekosistem Riset & Pengembangan ZZLUXORA (4 Repositori + Portal)

Proyek ini merupakan perangkat lunak konsol utama dari ekosistem riset terintegrasi **ZZLUXORA**:

| Komponen | Repositori | Peran & Deskripsi |
|---|---|---|
| **Software Konsol** | [**`zzdevxx/zzluxora`**](https://github.com/zzdevxx/zzluxora) *(Repo Ini)* | Perangkat lunak konsol pencahayaan panggung (Python 3.10+ / 3.15.2, PySide6/Qt6, NumPy STFT/MIR Core Engine, grandMA3 style mixer 513 fader, 2D/3D stage visualizer, Art-Net 4 DMX512 UDP transmitter). |
| **Hardware Node** | [**`zzdevxx/esp32-artnet-dmx`**](https://gitlab.com/zzdevxx/esp32-artnet-dmx) | Prototipe perangkat keras konverter nirkabel Art-Net ke DMX512 berbasis ESP32 Dual-Core (FreeRTOS SMP Core 0 DMX / Core 1 WiFi), transceiver RS-485 MAX485, LCD 16x2 I2C, dan boks fabrikasi Box X4 DIY. |
| **Library Fixture** | [**`zzdevxx/zz-fixture`**](https://github.com/zzdevxx/zz-fixture) | Katalog profil fixture `.qxf` & `.zfx` (`Alien-AL36`, `Illumsolid-YSP01`, `Kumastb-STL47`, `Wisdom-54X3`, `zzdree-36X`) beserta showfile template QLC+. |
| **Naskah & Riset** | [**`zzdevxx/zzluxora-thesis`**](https://gitlab.com/zzdevxx/zzluxora-thesis) | Naskah akademik skripsi S1 Teknik Komputer FT UNNES, pemodelan matematis STFT Hann & Russell 2D, protokol uji lapangan 41-kolom, instrumen evaluasi (SUS & Kesesuaian), serta draf ilmiah Bab 1-5 lengkap. |
| **Portal Unduhan** | [**`zzdree.my.id/zzluxora/`**](https://zzdree.my.id/zzluxora/) | Halaman web publik distribusi installer Windows `ZZLUXORA-Setup-10.0.0.exe` & simulator warna RGBW/DMX512 ([`zzdevxx/zzluxora-download`](https://github.com/zzdevxx/zzluxora-download)). |

---

## Fitur Utama

1. **Pure Zero-GUI Core Engine:**
   - Komputasi STFT diskrit dengan Hann Windowing ($f_s = 22.050\text{ Hz}$, $N=2048$, $H=512$, laju $\approx 43\text{ FPS}$ selaras dengan DMX512).
   - Ekstraksi Fitur Akustik Spektral: RMS Energy, Spectral Centroid, Chroma 12-Semitone, dan MFCC.
   - Pemodelan Emosi Musik 2D Russell (Valence-Arousal).
   - Dekomposisi 4-Kanal Physical RGBW untuk mencegah desaturasi warna pada lampu PAR LED panggung, disertai rekombinasi W dan skalasi dimmer otomatis untuk fixture 3CH RGB tanpa kanal dimmer (seperti `zzdree-36X`).
   - Art-Net 4 DMX512 Transmitter (UDP port 6454 ke ESP32 Node atau simulator).

2. **Antarmuka Konsol Panggung (grandMA3 & QLC+ Inspired):**
   - Desain gelap (*dark industrial console*), modern-minimalis, tanpa ikon/emoji berlebih.
   - Header Bar terintegrasi: status Art-Net live, toggle Play/Stop, dan tombol instan Blackout.
   - Tab Address: Grid patch DMX 512 kanal dalam 20 kolom horizontal dengan indikator visual kanal serta quick-patch langsung 4x `zzdree-36X` (DMX 001, 017, 033, 049).
   - Tab Mixer: 513 Slider Fader (1 Master Dimmer + 512 Kanal DMX fisik) bernilai 0-255.
   - Tab Preview: Visualisasi panggung 2D & 3D tampak depan dengan panel kontrol fixture dan koordinat.
   - Fixture Library & Editor: 5 profil fixture `.zfx` resmi (`Alien-AL36`, `Illumsolid-YSP01`, `Kumastb-STL47`, `Wisdom-54X3`, `zzdree-36X`) beserta pembuat profil custom format JSON.

---

## Menjalankan Core Engine (CLI Standalone)

Untuk menguji mesin komputasi sinyal dan transmisi Art-Net secara mandiri tanpa GUI:

```powershell
# Jalankan demo streaming Art-Net ke localhost
.\.venv\Scripts\python.exe main.py --cli --duration 4.0

# Jalankan ke IP modul ESP32 panggung (Mode AP: 192.168.4.1)
.\.venv\Scripts\python.exe main.py --cli --ip 192.168.4.1 --duration 10.0
```

---

## Menjalankan Pengujian (Unit Tests)

```bash
# Linux / macOS
PYTHONPATH=$PWD/tools python3 tools/run_tests_guarded.py
```

```powershell
# Windows PowerShell (venv Python 3.15.2)
$env:PYTHONPATH="$PWD\tools"; .\.venv\Scripts\python.exe tools\run_tests_guarded.py
```

Ini adalah runner resmi. `python -m unittest discover -s tests` **jangan** dipakai: perintah itu ikut mengumpulkan berkas gaya-pytest (menghitung ganda) dan dapat memunculkan dialog `QMessageBox`. `run_tests_guarded.py` menetralkan dialog dan memilih runner per berkas. Suite saat ini mencakup **197 test unik** (166 unittest + 31 pytest).

> Catatan bahan uji: 10 berkas WAV di `data/audio/` adalah **audio sintetis** yang dibangkitkan `tools/generate_benchmark_audio.py` (12 detik, 22.050 Hz, mono) dan dinamai menurut lagu referensi; ini **bukan rekaman berlisensi**. Untuk bahan uji persepsi, gunakan `tools/fetch_test_audio.py` yang mengunduh audio nyata beserta sidecar provenance.

---

## Lisensi

Hak Cipta (C) 2026 Andreas Restuawanta Christwara. Dirilis di bawah lisensi [Apache-2.0](LICENSE).
