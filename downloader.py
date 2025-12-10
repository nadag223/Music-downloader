import os
from urllib.parse import urlparse
import requests
import yt_dlp

DEFAULT_DOWNLOAD_DIR = r"C:\Users\User\Music"
FFMPEG_PATH = r"C:\Users\User\Downloads\ffmpeg-master-latest-win64-gpl-shared\ffmpeg-master-latest-win64-gpl-shared\bin" # you need to add your ffmpeg path if you want it to convert to

def safe_filename_from_url(url):
    p = urlparse(url)
    name = os.path.basename(p.path) or "downloaded_file"
    return name

def download_direct(url, path, progress_callback=None, chunk_size=1024*16):
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

def run_yt_dlp(url, outfolder, format_choice="best", download_playlist=False, progress_output_callback=None):
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
        if progress_output_callback:
            if d['status'] == 'downloading':
                total = d.get('total_bytes') or d.get('total_bytes_estimate')
                if total:
                    downloaded = d.get('downloaded_bytes', 0)
                    pct = (downloaded / total * 100)
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
            progress_output_callback(f"Download completed successfully.")
    except yt_dlp.utils.DownloadError as e:
        if progress_output_callback:
            progress_output_callback(f"Error: {e}")
            if 'ffmpeg' in str(e).lower() and postprocessor:
                progress_output_callback("FFMPEG error. Trying to download without conversion.")
                ydl_opts.pop('postprocessors')
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    ydl.download([url])
    except Exception as e:
        if progress_output_callback:
            progress_output_callback(f"An unexpected error occurred: {e}")
