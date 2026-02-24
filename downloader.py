import os
from urllib.parse import urlparse
import requests
import yt_dlp
import sys


DEFAULT_DOWNLOAD_DIR = os.path.join(os.path.expanduser("~"), "Media")
def resource_path(filename):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, filename)
    return os.path.join(os.path.abspath("."), filename)

FFMPEG_PATH = resource_path("ffmpeg.exe")


def safe_filename_from_url(url):
    p = urlparse(url)
    name = os.path.basename(p.path) or "downloaded_file"
    return name


def download_direct(url, path, progress_callback=None, chunk_size=1024 * 16):
    with requests.get(url, stream=True, timeout=15) as r:
        r.raise_for_status()
        total = r.headers.get("content-length")
        total = int(total) if total else 0
        downloaded = 0
        with open(path, "wb") as f:
            for chunk in r.iter_content(chunk_size=chunk_size):
                if not chunk:
                    continue
                f.write(chunk)
                downloaded += len(chunk)
                if progress_callback:
                    progress_callback(downloaded, total)


def fetch_playlist_entries(url, max_entries=None):
    """
    Returns a list of dicts: [{'index': 1, 'title': '...', 'url': '...'}, ...]
    max_entries=None  → fetch all tracks in the playlist.
    max_entries=N     → fetch only the first N tracks.
    Does NOT download anything.
    """
    ydl_opts = {
        'quiet': True,
        'extract_flat': True,
        'noplaylist': False,
    }
    if max_entries is not None:
        ydl_opts['playlistend'] = max_entries

    entries = []
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=False)
        if 'entries' in info:
            for i, entry in enumerate(info['entries'], start=1):
                if entry is None:
                    continue
                entries.append({
                    'index': i,
                    'title': entry.get('title') or entry.get('id') or f"Track {i}",
                    'url': entry.get('url') or entry.get('webpage_url') or url,
                    'id': entry.get('id', ''),
                })
        else:
            # Single video
            entries.append({
                'index': 1,
                'title': info.get('title') or 'Single video',
                'url': info.get('webpage_url') or url,
                'id': info.get('id', ''),
            })
    return entries


def run_yt_dlp_single(url, outfolder, format_choice="best",
                      progress_output_callback=None, stop_event=None):
    """
    Downloads a single URL (no playlist logic).
    stop_event: threading.Event — if set, the download is aborted.
    """
    ydl_opts = {
        'format': 'bestaudio/best' if format_choice in ["mp3", "opus"] else 'best',
        'outtmpl': os.path.join(outfolder, '%(title)s.%(ext)s'),
        'noplaylist': True,
        'ffmpeg_location': FFMPEG_PATH,
    }

    postprocessor = None
    if format_choice in ["mp3", "opus"]:
        postprocessor = {
            'key': 'FFmpegExtractAudio',
            'preferredcodec': format_choice,
            'preferredquality': '192',
        }

    def progress_hook(d):
        # Stop mid-download if requested
        if stop_event and stop_event.is_set():
            raise yt_dlp.utils.DownloadError("Stopped by user.")
        if progress_output_callback:
            if d['status'] == 'downloading':
                total = d.get('total_bytes') or d.get('total_bytes_estimate')
                if total:
                    downloaded = d.get('downloaded_bytes', 0)
                    pct = downloaded / total * 100
                    progress_output_callback(f"  Downloading {pct:.1f}%")
                else:
                    progress_output_callback("  Downloading... (size unknown)")
            elif d['status'] == 'finished':
                progress_output_callback(f"  ✔ Done: {d.get('filename')}")

    ydl_opts['progress_hooks'] = [progress_hook]
    if postprocessor:
        ydl_opts['postprocessors'] = [postprocessor]

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])

    except yt_dlp.utils.DownloadError as e:
        if stop_event and stop_event.is_set():
            raise  # re-raise so the caller knows we stopped
        if progress_output_callback:
            progress_output_callback(f"  Error: {e}")
        if 'ffmpeg' in str(e).lower() and postprocessor:
            if progress_output_callback:
                progress_output_callback("  FFMPEG error. Retrying without conversion.")
            ydl_opts.pop('postprocessors', None)
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])

    except Exception as e:
        if progress_output_callback:
            progress_output_callback(f"  Unexpected error: {e}")


def run_yt_dlp(url, outfolder, format_choice="best", download_playlist=False,
               progress_output_callback=None, stop_event=None):
    """Legacy download (single URL or full playlist, no selection UI)."""
    ydl_opts = {
        'format': 'bestaudio/best' if format_choice in ["mp3", "opus"] else 'best',
        'outtmpl': os.path.join(outfolder, '%(title)s.%(ext)s'),
        'noplaylist': not download_playlist,
        'ffmpeg_location': FFMPEG_PATH,
    }

    postprocessor = None
    if format_choice in ["mp3", "opus"]:
        postprocessor = {
            'key': 'FFmpegExtractAudio',
            'preferredcodec': format_choice,
            'preferredquality': '192',
        }

    def progress_hook(d):
        if stop_event and stop_event.is_set():
            raise yt_dlp.utils.DownloadError("Stopped by user.")
        if progress_output_callback:
            if d['status'] == 'downloading':
                total = d.get('total_bytes') or d.get('total_bytes_estimate')
                if total:
                    downloaded = d.get('downloaded_bytes', 0)
                    pct = downloaded / total * 100
                    progress_output_callback(f"Downloading: {d.get('filename')} {pct:.1f}%")
                else:
                    progress_output_callback(f"Downloading: {d.get('filename')} (size unknown)")
            elif d['status'] == 'finished':
                progress_output_callback(f"Finished downloading: {d.get('filename')}")

    ydl_opts['progress_hooks'] = [progress_hook]
    if postprocessor:
        ydl_opts['postprocessors'] = [postprocessor]

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        if progress_output_callback:
            progress_output_callback("Download completed successfully.")

    except yt_dlp.utils.DownloadError as e:
        if stop_event and stop_event.is_set():
            return
        if progress_output_callback:
            progress_output_callback(f"Error: {e}")
        if 'ffmpeg' in str(e).lower() and postprocessor:
            if progress_output_callback:
                progress_output_callback("FFMPEG error. Trying to download without conversion.")
            ydl_opts.pop('postprocessors', None)
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])

    except Exception as e:
        if progress_output_callback:
            progress_output_callback(f"An unexpected error occurred: {e}")


