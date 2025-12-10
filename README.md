# Music-downloader
a free open source music downloader

A Python-based GUI application for downloading audio and video from YouTube and other supported platforms. Supports multiple output formats including **OPUS**, **MP3**, and **MP4**. Built using `tkinter` and `yt-dlp`.

---

## Features

- Download audio or video from YouTube URLs.
- Supports full playlist downloads.
- Choose output format: **OPUS**, **MP3**, or **MP4**.
- Automatic fallback: if conversion fails, keeps original downloaded format.
- Real-time download progress and logging.
- Simple and intuitive GUI.

---

## Requirements

- **Python 3.11+**
- [yt-dlp](https://github.com/yt-dlp/yt-dlp) Python library  
  ```bash
  pip install yt-dlp
  pip install requests
