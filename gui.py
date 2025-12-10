import threading
import os
import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
from downloader import run_yt_dlp, DEFAULT_DOWNLOAD_DIR

class MusicDownloaderGUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Music Downloader")
        self.geometry("750x580")
        self.resizable(False, False)

        # --- URL Input ---
        frm_top = ttk.Frame(self, padding=10)
        frm_top.pack(fill="x")
        ttk.Label(frm_top, text="Video/Playlist URL:").pack(anchor="w")
        self.url_var = tk.StringVar()
        self.url_entry = ttk.Entry(frm_top, textvariable=self.url_var, width=95)
        self.url_entry.pack(fill="x", pady=4)

        # --- Destination Folder ---
        dest_frm = ttk.Frame(self, padding=(10,0))
        dest_frm.pack(fill="x")
        ttk.Label(dest_frm, text="Output folder:").pack(anchor="w")
        self.folder_var = tk.StringVar(value=DEFAULT_DOWNLOAD_DIR)
        self.folder_entry = ttk.Entry(dest_frm, textvariable=self.folder_var, width=75)
        self.folder_entry.pack(side="left", padx=(0,6))
        ttk.Button(dest_frm, text="Choose folder...", command=self.choose_folder).pack(side="left")

        # --- Options (Format and Playlist) ---
        options_frame = ttk.Frame(self, padding=10)
        options_frame.pack(fill="x")
        
        ttk.Label(options_frame, text="Select format:").pack(side="left", anchor="w")
        self.format_var = tk.StringVar(value="Best")
        self.format_menu = ttk.Combobox(options_frame, textvariable=self.format_var, values=["Best", "mp3", "opus"], state="readonly")
        self.format_menu.pack(side="left", padx=5)

        self.playlist_var = tk.BooleanVar()
        self.playlist_check = ttk.Checkbutton(options_frame, text="Download playlist", variable=self.playlist_var)
        self.playlist_check.pack(side="left", padx=20)

        # --- Progress Bar and Status ---
        pr_frm = ttk.Frame(self, padding=10)
        pr_frm.pack(fill="x")
        self.progress = ttk.Progressbar(pr_frm, length=620, mode="determinate")
        self.progress.pack(pady=(0,6))
        self.status_var = tk.StringVar(value="Ready")
        ttk.Label(pr_frm, textvariable=self.status_var).pack(anchor="w")

        # --- Action Buttons ---
        btn_frm = ttk.Frame(self, padding=10)
        btn_frm.pack(fill="x")
        self.download_button = ttk.Button(btn_frm, text="Download", command=self.start_download)
        self.download_button.pack(side="left")
        ttk.Button(btn_frm, text="Clear log", command=self.clear_log).pack(side="left", padx=(8,0))
        ttk.Button(btn_frm, text="Exit", command=self.quit).pack(side="right")

        # --- Log Area ---
        ttk.Label(self, text="Log:").pack(anchor="w", padx=10)
        self.log = scrolledtext.ScrolledText(self, height=14, state="disabled")
        self.log.pack(fill="both", padx=10, pady=6, expand=True)

        self._download_thread = None

    def choose_folder(self):
        f = filedialog.askdirectory(initialdir=self.folder_var.get() or DEFAULT_DOWNLOAD_DIR)
        if f:
            self.folder_var.set(f)

    def log_msg(self, msg):
        def _log():
            self.log.configure(state="normal")
            self.log.insert("end", msg + "\n")
            self.log.see("end")
            self.log.configure(state="disabled")
        self.after(0, _log)

    def clear_log(self):
        self.log.configure(state="normal")
        self.log.delete("1.0", "end")
        self.log.configure(state="disabled")

    def start_download(self):
        if self._download_thread and self._download_thread.is_alive():
            messagebox.showinfo("Download in progress", "A download is already running.")
            return

        url = self.url_var.get().strip()
        if not url:
            messagebox.showwarning("Error", "Please enter a URL.")
            return

        outfolder = self.folder_var.get().strip() or DEFAULT_DOWNLOAD_DIR
        os.makedirs(outfolder, exist_ok=True)

        self.progress["value"] = 0
        self.status_var.set("Starting download...")
        self.log_msg(f"Starting download from: {url}")
        self.download_button.config(state="disabled")

        format_choice = self.format_var.get().lower()
        download_playlist = self.playlist_var.get()

        self._download_thread = threading.Thread(
            target=self._download_worker,
            args=(url, outfolder, format_choice, download_playlist),
            daemon=True
        )
        self._download_thread.start()

    def _download_worker(self, url, outfolder, format_choice, download_playlist):
        try:
            run_yt_dlp(
                url, 
                outfolder, 
                format_choice=format_choice, 
                download_playlist=download_playlist,
                progress_output_callback=self.log_msg
            )
            self.status_var.set(f"Download complete.")
        except Exception as e:
            self.log_msg("Error: " + str(e))
            self.status_var.set("Error during download.")
            messagebox.showerror("Error", str(e))
        finally:
            self.after(0, self.on_download_finish)
            
    def on_download_finish(self):
        self.progress["value"] = 100
        self.download_button.config(state="normal")

