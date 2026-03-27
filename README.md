# 🎵 Media Downloader

A modern, dark-themed desktop GUI for downloading YouTube videos and playlists — built with **PyQt6** and **yt-dlp**.

---

## ✨ Features

- **Single video & playlist download** — switch between modes with one click
- **Format selection** — MP3, AAC, M4A, FLAC, WAV, Opus, Vorbis, MP4, WebM, MKV, or auto-best
- **Video quality picker** — choose from 144p up to 4K when a video format is selected
- **Playlist selector dialog** — scan a playlist, check/uncheck individual tracks, and rename them before downloading
- **Live progress bar & log** — real-time feedback with an animated status indicator
- **Stop anytime** — gracefully cancel mid-download without corrupting files
- **Custom output folder** — browse or type a path; defaults to `~/Media`

---

## 🖥️ Requirements

| Dependency | Version |
|------------|---------|
| Python     | 3.9+    |
| PyQt6      | 6.4+    |
| yt-dlp     | latest  |
| ffmpeg     | any recent (for audio conversion & merging) |

---

## 🚀 Installation

```bash
# 1. Clone the repo
git clone https://github.com/your-username/media-downloader.git
cd media-downloader

# 2. Create a virtual environment (recommended)
python -m venv .venv
source .venv/bin/activate      # Windows: .venv\Scripts\activate

# 3. Install Python dependencies
pip install PyQt6 yt-dlp

# 4. Make sure ffmpeg is on your PATH
#    macOS:   brew install ffmpeg
#    Ubuntu:  sudo apt install ffmpeg
#    Windows: https://ffmpeg.org/download.html
```

---

## ▶️ Usage

```bash
python main.py
```

### Basic workflow

1. Paste a YouTube URL into the **URL** field.
2. Choose an **output folder** (defaults to `~/Media`).
3. Pick a **format** (and quality for video formats).
4. Click **▶ Download**.

### Playlist mode

1. Check **Playlist mode**.
2. Optionally set a **Scan up to N tracks** limit (0 = all).
3. Click **▶ Download** — the app will scan the playlist and open a track selector.
4. Uncheck any tracks you want to skip; rename them with the ✏ button if needed.
5. Click **Download Selected**.

---

## 📁 Project Structure

```
media-downloader/
├── main.py          # Entry point
├── gui.py           # PyQt6 GUI (MediaDownloaderGUI)
├── downloader.py    # yt-dlp wrappers (run_yt_dlp, fetch_playlist_entries, …)
└── README.md
```

---

## ⚙️ Configuration

| Setting | Default | Where to change |
|---------|---------|-----------------|
| Default download directory | `~/Media` | `downloader.py → DEFAULT_DOWNLOAD_DIR` |
| Max playlist scan | 0 (all) | UI spin-box at runtime |
| UI accent color | `#3B82F6` | `gui.py → C_ACCENT` |

---

## 🤝 Contributing

Pull requests are welcome! Please open an issue first to discuss major changes.

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/my-feature`
3. Commit your changes: `git commit -m "Add my feature"`
4. Push: `git push origin feature/my-feature`
5. Open a Pull Request

---

```

---

> **Disclaimer:** This tool is intended for downloading content you own or have permission to download. Please respect copyright law and the Terms of Service of any platform you use it with.
