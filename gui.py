"""
Media Downloader — Modern PyQt6 GUI
pip install PyQt6
"""

import threading
import os
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QLineEdit, QPushButton, QComboBox, QCheckBox, QSpinBox,
    QProgressBar, QTextEdit, QFileDialog, QDialog, QScrollArea,
    QFrame, QSizePolicy, QSpacerItem,
)
from PyQt6.QtCore import (
    Qt, QThread, pyqtSignal, QPropertyAnimation, QEasingCurve,
    QPoint, pyqtProperty
)
from PyQt6.QtGui import (
    QFont, QColor, QPalette, QPainter, QBrush,
)

Media_dir = os.path.join(os.path.expanduser("~"), "Media")

from downloader import run_yt_dlp, run_yt_dlp_single, fetch_playlist_entries, DEFAULT_DOWNLOAD_DIR

# ─────────────────────────────────────────────────────────────────────────────
# Design Tokens
# ─────────────────────────────────────────────────────────────────────────────
C_BG      = "#0A0C12"
C_SURFACE = "#111520"
C_CARD    = "#161B27"
C_BORDER  = "#1E2535"
C_ACCENT  = "#3B82F6"
C_ACCENT2 = "#06B6D4"
C_SUCCESS = "#10B981"
C_DANGER  = "#EF4444"
C_TEXT    = "#E8EEFF"
C_TEXT_DIM= "#5A6480"
C_TEXT_MID= "#8B93B0"

# Which formats are video (show quality picker)
VIDEO_FORMATS = {"mp4", "webm", "mkv"}

GLOBAL_STYLE = f"""
QMainWindow, QDialog {{
    background-color: {C_BG};
}}
QWidget {{
    background-color: transparent;
    color: {C_TEXT};
    font-family: 'Segoe UI', 'SF Pro Text', 'Inter', sans-serif;
    font-size: 13px;
    selection-background-color: {C_ACCENT};
}}
QLabel {{
    color: {C_TEXT};
    background: transparent;
}}
QLineEdit {{
    background-color: {C_CARD};
    border: 1.5px solid {C_BORDER};
    border-radius: 8px;
    padding: 8px 12px;
    color: {C_TEXT};
    font-size: 13px;
}}
QLineEdit:focus {{
    border-color: {C_ACCENT};
    background-color: #1A2035;
}}
QLineEdit::placeholder {{
    color: {C_TEXT_DIM};
}}
QPushButton {{
    background-color: {C_CARD};
    border: 1.5px solid {C_BORDER};
    border-radius: 8px;
    color: {C_TEXT};
    padding: 8px 18px;
    font-size: 13px;
    font-weight: 500;
}}
QPushButton:hover {{
    border-color: {C_ACCENT};
    color: {C_ACCENT};
    background-color: #1A2035;
}}
QPushButton:pressed {{
    background-color: #0F1626;
}}
QPushButton:disabled {{
    color: {C_TEXT_DIM};
    border-color: {C_BORDER};
    background-color: {C_CARD};
}}
QPushButton#primaryBtn {{
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                stop:0 {C_ACCENT}, stop:1 {C_ACCENT2});
    border: none;
    border-radius: 8px;
    color: #FFFFFF;
    font-weight: 700;
    font-size: 14px;
    padding: 10px 28px;
}}
QPushButton#primaryBtn:hover {{
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                stop:0 #5B9BFF, stop:1 #22D3EE);
    color: #FFFFFF;
}}
QPushButton#primaryBtn:disabled {{
    background: {C_BORDER};
    color: {C_TEXT_DIM};
}}
QPushButton#dangerBtn {{
    border-color: {C_DANGER};
    color: {C_DANGER};
}}
QPushButton#dangerBtn:hover {{
    background-color: #2A1520;
}}
QComboBox {{
    background-color: {C_CARD};
    border: 1.5px solid {C_BORDER};
    border-radius: 8px;
    padding: 7px 12px;
    color: {C_TEXT};
    min-width: 90px;
}}
QComboBox:hover {{ border-color: {C_ACCENT}; }}
QComboBox::drop-down {{ border: none; width: 28px; }}
QComboBox QAbstractItemView {{
    background-color: {C_CARD};
    border: 1.5px solid {C_ACCENT};
    border-radius: 8px;
    color: {C_TEXT};
    selection-background-color: {C_ACCENT};
    padding: 4px;
}}
QSpinBox {{
    background-color: {C_CARD};
    border: 1.5px solid {C_BORDER};
    border-radius: 8px;
    padding: 7px 10px;
    color: {C_TEXT};
    min-width: 70px;
}}
QSpinBox:focus {{ border-color: {C_ACCENT}; }}
QSpinBox::up-button, QSpinBox::down-button {{
    background: transparent;
    border: none;
    width: 20px;
}}
QCheckBox {{
    spacing: 8px;
    color: {C_TEXT};
}}
QCheckBox::indicator {{
    width: 18px; height: 18px;
    border: 1.5px solid {C_BORDER};
    border-radius: 5px;
    background: {C_CARD};
}}
QCheckBox::indicator:checked {{
    background-color: {C_ACCENT};
    border-color: {C_ACCENT};
}}
QCheckBox::indicator:hover {{ border-color: {C_ACCENT}; }}
QProgressBar {{
    background-color: {C_CARD};
    border: none;
    border-radius: 6px;
    height: 8px;
    text-align: center;
    color: transparent;
}}
QProgressBar::chunk {{
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                stop:0 {C_ACCENT}, stop:1 {C_ACCENT2});
    border-radius: 6px;
}}
QTextEdit {{
    background-color: {C_CARD};
    border: 1.5px solid {C_BORDER};
    border-radius: 10px;
    padding: 10px;
    color: {C_TEXT_MID};
    font-family: 'Cascadia Code', 'JetBrains Mono', 'Consolas', monospace;
    font-size: 12px;
}}
QScrollBar:vertical {{
    background: transparent;
    width: 6px;
    margin: 0;
}}
QScrollBar::handle:vertical {{
    background: {C_BORDER};
    border-radius: 3px;
    min-height: 30px;
}}
QScrollBar::handle:vertical:hover {{ background: {C_TEXT_DIM}; }}
QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{ height: 0; }}
QFrame#divider {{
    background-color: {C_BORDER};
    max-height: 1px;
    border: none;
}}
QFrame#card {{
    background-color: {C_SURFACE};
    border: 1.5px solid {C_BORDER};
    border-radius: 12px;
}}
QScrollArea {{
    border: 1.5px solid {C_BORDER};
    border-radius: 12px;
    background: {C_SURFACE};
}}
"""


# ─────────────────────────────────────────────────────────────────────────────
# Worker Threads
# ─────────────────────────────────────────────────────────────────────────────

class ScanThread(QThread):
    done  = pyqtSignal(list)
    error = pyqtSignal(str)

    def __init__(self, url, max_entries):
        super().__init__()
        self.url = url
        self.max_entries = max_entries

    def run(self):
        try:
            entries = fetch_playlist_entries(self.url, max_entries=self.max_entries)
            self.done.emit(entries)
        except Exception as e:
            self.error.emit(str(e))


class DownloadThread(QThread):
    log_msg    = pyqtSignal(str)
    progress   = pyqtSignal(int)
    status_msg = pyqtSignal(str)
    finished   = pyqtSignal(bool)

    def __init__(self, url, outfolder, format_choice, stop_event):
        super().__init__()
        self.url = url
        self.outfolder = outfolder
        self.format_choice = format_choice
        self.stop_event = stop_event

    def run(self):
        try:
            run_yt_dlp(
                self.url, self.outfolder,
                format_choice=self.format_choice,
                download_playlist=False,
                progress_output_callback=self.log_msg.emit,
                stop_event=self.stop_event,
            )
            self.progress.emit(100)
            self.finished.emit(not self.stop_event.is_set())
        except Exception as e:
            self.log_msg.emit(f"Error: {e}")
            self.finished.emit(False)


class PlaylistDownloadThread(QThread):
    log_msg    = pyqtSignal(str)
    progress   = pyqtSignal(int)
    status_msg = pyqtSignal(str)
    finished   = pyqtSignal(bool)

    def __init__(self, entries, outfolder, format_choice, stop_event):
        super().__init__()
        self.entries = entries
        self.outfolder = outfolder
        self.format_choice = format_choice
        self.stop_event = stop_event

    def run(self):
        total = len(self.entries)
        for i, entry in enumerate(self.entries, start=1):
            if self.stop_event.is_set():
                self.log_msg.emit("Stopped by user.")
                self.finished.emit(False)
                return

            title = entry["title"]
            self.status_msg.emit(f"[{i}/{total}] {title}")
            self.log_msg.emit(f"\n[{i}/{total}]  {title}")

            try:
                run_yt_dlp_single(
                    entry["url"], self.outfolder,
                    format_choice=self.format_choice,
                    progress_output_callback=self.log_msg.emit,
                    stop_event=self.stop_event,
                )
            except Exception as e:
                if self.stop_event.is_set():
                    self.finished.emit(False)
                    return
                self.log_msg.emit(f"  Error on '{title}': {e}")

            self.progress.emit(int(i / total * 100))

        self.finished.emit(not self.stop_event.is_set())


# ─────────────────────────────────────────────────────────────────────────────
# Animated Pulse Dot
# ─────────────────────────────────────────────────────────────────────────────

class PulseDot(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedSize(12, 12)
        self._color   = QColor(C_TEXT_DIM)
        self._opacity = 1.0
        self._anim    = None

    def set_active(self, active: bool, color: str = C_ACCENT):
        self._color = QColor(color)
        if active:
            self._anim = QPropertyAnimation(self, b"opacity_prop")
            self._anim.setDuration(900)
            self._anim.setStartValue(1.0)
            self._anim.setEndValue(0.2)
            self._anim.setEasingCurve(QEasingCurve.Type.SineCurve)
            self._anim.setLoopCount(-1)
            self._anim.start()
        else:
            if self._anim:
                self._anim.stop()
            self._opacity = 1.0
            self.update()

    def get_opacity(self): return self._opacity
    def set_opacity(self, v):
        self._opacity = v
        self.update()
    opacity_prop = pyqtProperty(float, get_opacity, set_opacity)

    def paintEvent(self, event):
        p = QPainter(self)
        p.setRenderHint(QPainter.RenderHint.Antialiasing)
        col = QColor(self._color)
        col.setAlphaF(self._opacity)
        p.setBrush(QBrush(col))
        p.setPen(Qt.PenStyle.NoPen)
        p.drawEllipse(1, 1, 10, 10)


# ─────────────────────────────────────────────────────────────────────────────
# Playlist Selector Dialog
# ─────────────────────────────────────────────────────────────────────────────

class TrackRow(QWidget):
    def __init__(self, index, entry, parent=None):
        super().__init__(parent)
        self._entry   = dict(entry)
        self._editing = False
        self.setFixedHeight(42)

        layout = QHBoxLayout(self)
        layout.setContentsMargins(12, 0, 12, 0)
        layout.setSpacing(10)

        num = QLabel(f"{index:>3}.")
        num.setFixedWidth(36)
        num.setStyleSheet(f"color: {C_TEXT_DIM}; font-family: monospace; font-size: 12px;")
        layout.addWidget(num)

        self.check = QCheckBox()
        self.check.setChecked(True)
        self.check.setFixedWidth(24)
        layout.addWidget(self.check)

        self.title_lbl = QLabel(entry["title"])
        self.title_lbl.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
        self.title_lbl.setStyleSheet(f"color: {C_TEXT}; font-size: 13px;")
        layout.addWidget(self.title_lbl)

        self.title_edit = QLineEdit(entry["title"])
        self.title_edit.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
        self.title_edit.setFixedHeight(30)
        self.title_edit.hide()
        self.title_edit.returnPressed.connect(self._commit)
        self.title_edit.editingFinished.connect(self._commit)
        layout.addWidget(self.title_edit)

        self.rename_btn = QPushButton("✏")
        self.rename_btn.setFixedSize(28, 28)
        self.rename_btn.setStyleSheet(f"""
            QPushButton {{
                background: transparent; border: 1px solid {C_BORDER};
                border-radius: 6px; color: {C_TEXT_DIM}; font-size: 13px; padding: 0;
            }}
            QPushButton:hover {{ border-color: {C_ACCENT}; color: {C_ACCENT}; }}
        """)
        self.rename_btn.clicked.connect(self._toggle_edit)
        layout.addWidget(self.rename_btn)

        self.setStyleSheet(f"TrackRow {{ border-bottom: 1px solid {C_BORDER}; }}")

    def _toggle_edit(self):
        if not self._editing:
            self.title_lbl.hide()
            self.title_edit.setText(self.title_lbl.text())
            self.title_edit.show()
            self.title_edit.setFocus()
            self.title_edit.selectAll()
            self.rename_btn.setText("✔")
            self._editing = True
        else:
            self._commit()

    def _commit(self):
        new_title = self.title_edit.text().strip() or self._entry["title"]
        self._entry["title"] = new_title
        self.title_lbl.setText(new_title)
        self.title_edit.hide()
        self.title_lbl.show()
        self.rename_btn.setText("✏")
        self._editing = False

    def is_selected(self):  return self.check.isChecked()
    def get_entry(self):    return dict(self._entry)


class PlaylistSelectorDialog(QDialog):
    def __init__(self, parent, entries):
        super().__init__(parent)
        self.setWindowTitle("Select Tracks")
        self.resize(740, 580)
        self.setStyleSheet(GLOBAL_STYLE + f"QDialog {{ background: {C_BG}; }}")
        self.selected_entries = []
        self._rows = []

        root = QVBoxLayout(self)
        root.setContentsMargins(20, 20, 20, 20)
        root.setSpacing(14)

        hdr = QLabel(f"<b>{len(entries)}</b> tracks found — uncheck to skip, ✏ to rename")
        hdr.setStyleSheet(f"color: {C_TEXT_MID}; font-size: 13px;")
        root.addWidget(hdr)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        container = QWidget()
        container.setStyleSheet(f"background: {C_SURFACE};")
        vbox = QVBoxLayout(container)
        vbox.setContentsMargins(0, 0, 0, 0)
        vbox.setSpacing(0)

        for entry in entries:
            row = TrackRow(entry["index"], entry)
            self._rows.append(row)
            vbox.addWidget(row)

        vbox.addStretch()
        scroll.setWidget(container)
        root.addWidget(scroll)

        bar = QHBoxLayout()
        sel_all = QPushButton("Select All")
        sel_all.clicked.connect(lambda: [r.check.setChecked(True)  for r in self._rows])
        desel   = QPushButton("Deselect All")
        desel.clicked.connect(lambda: [r.check.setChecked(False) for r in self._rows])
        bar.addWidget(sel_all)
        bar.addWidget(desel)
        bar.addStretch()

        cancel = QPushButton("Cancel")
        cancel.clicked.connect(self.reject)
        confirm = QPushButton("Download Selected")
        confirm.setObjectName("primaryBtn")
        confirm.clicked.connect(self._confirm)
        bar.addWidget(cancel)
        bar.addSpacing(8)
        bar.addWidget(confirm)
        root.addLayout(bar)

    def _confirm(self):
        self.selected_entries = [r.get_entry() for r in self._rows if r.is_selected()]
        self.accept()


# ─────────────────────────────────────────────────────────────────────────────
# Main Window
# ─────────────────────────────────────────────────────────────────────────────

class MediaDownloaderGUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Media Downloader")
        self.setMinimumSize(800, 680)
        self.resize(820, 720)
        self.setStyleSheet(GLOBAL_STYLE)

        self._stop_event    = threading.Event()
        self._active_thread = None

        central = QWidget()
        self.setCentralWidget(central)
        root = QVBoxLayout(central)
        root.setContentsMargins(24, 24, 24, 24)
        root.setSpacing(16)

        # ── Title bar ─────────────────────────────────────────────────────
        title_row = QHBoxLayout()
        ico = QLabel("🎵")
        ico.setStyleSheet("font-size: 26px;")
        title_row.addWidget(ico)

        title = QLabel("Media Downloader")
        title.setStyleSheet(f"""
            font-size: 22px; font-weight: 700;
            color: {C_TEXT};
            letter-spacing: -0.5px;
        """)
        title_row.addWidget(title)
        title_row.addStretch()

        self._pulse = PulseDot()
        title_row.addWidget(self._pulse)
        self._status_lbl = QLabel("Ready")
        self._status_lbl.setStyleSheet(f"color: {C_TEXT_DIM}; font-size: 12px;")
        title_row.addWidget(self._status_lbl)
        root.addLayout(title_row)

        # Thin divider
        div = QFrame()
        div.setObjectName("divider")
        div.setFixedHeight(1)
        root.addWidget(div)

        # ── URL Card ──────────────────────────────────────────────────────
        url_card = self._card()
        url_layout = QVBoxLayout(url_card)
        url_layout.setContentsMargins(16, 14, 16, 14)
        url_layout.setSpacing(8)

        url_layout.addWidget(self._section_label("URL"))
        self.url_edit = QLineEdit()
        self.url_edit.setPlaceholderText("Paste a YouTube video or playlist URL…")
        self.url_edit.setFixedHeight(42)
        url_layout.addWidget(self.url_edit)

        url_layout.addWidget(self._section_label("OUTPUT FOLDER"))
        folder_row = QHBoxLayout()
        self.folder_edit = QLineEdit(DEFAULT_DOWNLOAD_DIR)
        self.folder_edit.setFixedHeight(42)
        folder_row.addWidget(self.folder_edit)
        browse = QPushButton("Browse…")
        browse.setFixedHeight(42)
        browse.clicked.connect(self._choose_folder)
        folder_row.addWidget(browse)
        url_layout.addLayout(folder_row)
        root.addWidget(url_card)

        # ── Options Card ──────────────────────────────────────────────────
        opt_card = self._card()
        opt_layout = QHBoxLayout(opt_card)
        opt_layout.setContentsMargins(16, 14, 16, 14)
        opt_layout.setSpacing(16)

        # Format label + combo
        opt_layout.addWidget(QLabel("Format"))
        self.format_combo = QComboBox()
        self.format_combo.setFixedHeight(38)
        self.format_combo.setMinimumWidth(130)

        FORMATS = [
            ("── Auto ──", False),
            ("default", True),
            ("── Audio ──", False),
            ("mp3",         True),
            ("aac",         True),
            ("m4a",         True),
            ("flac",        True),
            ("wav",         True),
            ("opus",        True),
            ("vorbis",      True),
            ("── Video ──", False),
            ("mp4",         True),
            ("webm",        True),
            ("mkv",         True),
        ]
        for label, enabled in FORMATS:
            self.format_combo.addItem(label)
            if not enabled:
                idx = self.format_combo.count() - 1
                item = self.format_combo.model().item(idx)
                item.setEnabled(False)
                item.setForeground(QColor(C_TEXT_DIM))

        self.format_combo.setCurrentText("default")
        self.format_combo.currentTextChanged.connect(self._on_format_changed)
        opt_layout.addWidget(self.format_combo)

        # ── Video quality widgets (hidden by default) ──────────────────────
        self._sep_quality = QFrame()
        self._sep_quality.setFrameShape(QFrame.Shape.VLine)
        self._sep_quality.setStyleSheet(f"background: {C_BORDER}; max-width: 1px;")
        opt_layout.addWidget(self._sep_quality)

        self._lbl_quality = QLabel("Quality")
        self._lbl_quality.setStyleSheet(f"color: {C_TEXT_MID};")
        opt_layout.addWidget(self._lbl_quality)

        self.quality_combo = QComboBox()
        self.quality_combo.setFixedHeight(38)
        self.quality_combo.setMinimumWidth(110)
        self.quality_combo.addItems([
            "Best available",
            "4K  (2160p)",
            "1440p",
            "1080p (FHD)",
            "720p  (HD)",
            "480p",
            "360p",
            "240p",
            "144p",
        ])
        opt_layout.addWidget(self.quality_combo)

        # Hide quality widgets initially (mp3 is default)
        self._sep_quality.hide()
        self._lbl_quality.hide()
        self.quality_combo.hide()

        # Divider before playlist
        sep = QFrame()
        sep.setFrameShape(QFrame.Shape.VLine)
        sep.setStyleSheet(f"background: {C_BORDER}; max-width: 1px;")
        opt_layout.addWidget(sep)

        # Playlist options
        self.playlist_chk = QCheckBox("Playlist mode")
        self.playlist_chk.stateChanged.connect(self._toggle_playlist_opts)
        opt_layout.addWidget(self.playlist_chk)

        self._lbl_scan = QLabel("  Scan up to")
        self._lbl_scan.setStyleSheet(f"color: {C_TEXT_MID};")
        self.max_spin = QSpinBox()
        self.max_spin.setRange(0, 9999)
        self.max_spin.setValue(0)
        self.max_spin.setFixedHeight(38)
        self._lbl_all = QLabel("tracks  (0 = all)")
        self._lbl_all.setStyleSheet(f"color: {C_TEXT_MID};")
        for w in (self._lbl_scan, self.max_spin, self._lbl_all):
            w.hide()
            opt_layout.addWidget(w)

        opt_layout.addStretch()
        root.addWidget(opt_card)

        # ── Progress ──────────────────────────────────────────────────────
        self.progress = QProgressBar()
        self.progress.setFixedHeight(8)
        self.progress.setValue(0)
        self.progress.setTextVisible(False)
        root.addWidget(self.progress)

        # ── Action Buttons ────────────────────────────────────────────────
        btn_row = QHBoxLayout()
        btn_row.setSpacing(10)

        self.dl_btn = QPushButton("▶   Download")
        self.dl_btn.setObjectName("primaryBtn")
        self.dl_btn.setFixedHeight(44)
        self.dl_btn.clicked.connect(self.start_download)
        btn_row.addWidget(self.dl_btn)

        self.stop_btn = QPushButton("⏹   Stop")
        self.stop_btn.setObjectName("dangerBtn")
        self.stop_btn.setFixedHeight(44)
        self.stop_btn.setEnabled(False)
        self.stop_btn.clicked.connect(self.stop_download)
        btn_row.addWidget(self.stop_btn)

        btn_row.addStretch()

        clear_btn = QPushButton("Clear Log")
        clear_btn.setFixedHeight(44)
        clear_btn.clicked.connect(self._clear_log)
        btn_row.addWidget(clear_btn)

        quit_btn = QPushButton("Quit")
        quit_btn.setFixedHeight(44)
        quit_btn.clicked.connect(QApplication.instance().quit)
        btn_row.addWidget(quit_btn)

        root.addLayout(btn_row)

        # ── Log ───────────────────────────────────────────────────────────
        root.addWidget(self._section_label("LOG"))
        self.log = QTextEdit()
        self.log.setReadOnly(True)
        self.log.setPlaceholderText("Download activity will appear here…")
        root.addWidget(self.log)

    # ── Widget helpers ─────────────────────────────────────────────────────

    def _card(self):
        card = QFrame()
        card.setObjectName("card")
        return card

    def _section_label(self, text: str):
        lbl = QLabel(text)
        lbl.setStyleSheet(
            f"color: {C_TEXT_DIM}; font-size: 10px; font-weight: 700; letter-spacing: 1.5px;"
        )
        return lbl

    # ── Format / quality logic ─────────────────────────────────────────────

    def _on_format_changed(self, fmt: str):
        """Show quality picker only when a video format is selected."""
        is_video = fmt.lower() in VIDEO_FORMATS
        self._sep_quality.setVisible(is_video)
        self._lbl_quality.setVisible(is_video)
        self.quality_combo.setVisible(is_video)

    def _quality_to_yt_format(self, quality_label: str, container: str) -> str:
        """
        Convert the human-readable quality label into a yt-dlp format string.
        Returns a string to pass as format_choice to the downloader.
        """
        mapping = {
            "Best available": f"bestvideo[ext={container}]+bestaudio/best[ext={container}]/best",
            "4K  (2160p)":    f"bestvideo[height<=2160][ext={container}]+bestaudio/best",
            "1440p":          f"bestvideo[height<=1440][ext={container}]+bestaudio/best",
            "1080p (FHD)":    f"bestvideo[height<=1080][ext={container}]+bestaudio/best",
            "720p  (HD)":     f"bestvideo[height<=720][ext={container}]+bestaudio/best",
            "480p":           f"bestvideo[height<=480][ext={container}]+bestaudio/best",
            "360p":           f"bestvideo[height<=360][ext={container}]+bestaudio/best",
            "240p":           f"bestvideo[height<=240][ext={container}]+bestaudio/best",
            "144p":           f"bestvideo[height<=144][ext={container}]+bestaudio/best",
        }
        return mapping.get(quality_label, "best")

    # ── UI logic ───────────────────────────────────────────────────────────

    def _choose_folder(self):
        start = self.folder_edit.text().strip() or Media_dir
        d = QFileDialog.getExistingDirectory(self, "Select Output Folder", start)
        if d:
            self.folder_edit.setText(d)

    def _toggle_playlist_opts(self, state):
        visible = bool(state)
        for w in (self._lbl_scan, self.max_spin, self._lbl_all):
            w.setVisible(visible)

    def _set_busy(self, busy: bool):
        self.dl_btn.setEnabled(not busy)
        self.stop_btn.setEnabled(busy)
        self._pulse.set_active(busy)

    def _set_status(self, msg: str):
        self._status_lbl.setText(msg)

    def log_msg(self, msg: str):
        self.log.append(msg)
        self.log.ensureCursorVisible()

    def _clear_log(self):
        self.log.clear()

    def stop_download(self):
        self._stop_event.set()
        self.log_msg("⏹ Stop requested…")
        self._set_status("Stopping…")
        self.stop_btn.setEnabled(False)

    # ── Shake for empty URL ────────────────────────────────────────────────

    def _shake(self, widget):
        orig = widget.pos()
        anim = QPropertyAnimation(widget, b"pos")
        anim.setDuration(320)
        for t, dx in [(0.0,0),(0.15,-8),(0.30,8),(0.45,-6),(0.60,6),(0.75,-3),(0.90,3),(1.0,0)]:
            anim.setKeyValueAt(t, orig + QPoint(dx, 0))
        anim.setEasingCurve(QEasingCurve.Type.Linear)
        anim.start(QPropertyAnimation.DeletionPolicy.DeleteWhenStopped)
        self._shake_ref = anim

    # ── Build the final format_choice string ──────────────────────────────

    def _get_format_choice(self) -> str:
        raw_fmt = self.format_combo.currentText().strip()
        if not raw_fmt or raw_fmt.startswith("──"):
            return "best"

        fmt = raw_fmt.lower()

        # Video format → combine with quality selection
        if fmt in VIDEO_FORMATS:
            quality_label = self.quality_combo.currentText()
            return self._quality_to_yt_format(quality_label, fmt)

        return fmt  # audio or "best"

    # ── Download flow ──────────────────────────────────────────────────────

    def start_download(self):
        if self._active_thread and self._active_thread.isRunning():
            return

        url = self.url_edit.text().strip()
        if not url:
            self._shake(self.url_edit)
            return

        outfolder = self.folder_edit.text().strip() or DEFAULT_DOWNLOAD_DIR
        os.makedirs(outfolder, exist_ok=True)

        fmt = self._get_format_choice()

        self._stop_event.clear()
        self.progress.setValue(0)

        if self.playlist_chk.isChecked():
            max_t = self.max_spin.value()
            self._set_busy(True)
            self._set_status("Scanning playlist…")
            self.log_msg(f"Scanning: {url}")

            self._scan_thread = ScanThread(url, max_t if max_t > 0 else None)
            self._scan_thread.done.connect(lambda e: self._open_selector(e, url, outfolder, fmt))
            self._scan_thread.error.connect(self._on_scan_error)
            self._scan_thread.start()
        else:
            self._set_busy(True)
            self._set_status("Downloading…")
            self.log_msg(f"Starting: {url}")

            t = DownloadThread(url, outfolder, fmt, self._stop_event)
            t.log_msg.connect(self.log_msg)
            t.progress.connect(self.progress.setValue)
            t.status_msg.connect(self._set_status)
            t.finished.connect(self._on_finish)
            self._active_thread = t
            t.start()

    def _on_scan_error(self, msg):
        self.log_msg(f"Scan error: {msg}")
        self._set_status("Scan failed.")
        self._set_busy(False)

    def _open_selector(self, entries, url, outfolder, fmt):
        if not entries:
            self.log_msg("No tracks found.")
            self._set_status("No tracks found.")
            self._set_busy(False)
            return

        self._set_status(f"Found {len(entries)} tracks.")
        dlg = PlaylistSelectorDialog(self, entries)
        if dlg.exec() != QDialog.DialogCode.Accepted or not dlg.selected_entries:
            self.log_msg("Cancelled.")
            self._set_status("Cancelled.")
            self._set_busy(False)
            return

        selected = dlg.selected_entries
        self.log_msg(f"Downloading {len(selected)} track(s)…")

        t = PlaylistDownloadThread(selected, outfolder, fmt, self._stop_event)
        t.log_msg.connect(self.log_msg)
        t.progress.connect(self.progress.setValue)
        t.status_msg.connect(self._set_status)
        t.finished.connect(self._on_finish)
        self._active_thread = t
        t.start()

    def _on_finish(self, completed: bool):
        if completed:
            self.progress.setValue(100)
            self._set_status("All done ✔")
            self.log_msg("\nDownload complete!")
        else:
            self._set_status("Stopped.")
            self.log_msg("Stopped.")
        self._set_busy(False)


