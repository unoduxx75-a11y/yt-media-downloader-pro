import sys
import os
import time
import urllib.request
import json
from pathlib import Path

from PyQt6.QtCore import Qt, QThread, pyqtSignal, QSize, QUrl
from PyQt6.QtGui import QIcon, QPixmap, QFont, QColor, QPainter, QDesktopServices
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QLineEdit, QPushButton, QComboBox, QCheckBox, QProgressBar,
    QListWidget, QListWidgetItem, QFrame, QDialog, QFileDialog, QMessageBox,
    QGraphicsDropShadowEffect, QSplitter
)

import yt_dlp

APP_VERSION = "1.0.0"
UPDATE_CHECK_URL = "https://raw.githubusercontent.com/unoduxx75-a11y/yt-downloader-pro/main/version.json"

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)


DARK_GREEN_GLASS_STYLE = """
QMainWindow {
    background-color: #080c09;
}
QWidget#CentralWidget {
    background-color: transparent;
}
QFrame#CardFrame {
    background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 rgba(16, 26, 19, 0.82), stop:1 rgba(10, 18, 12, 0.82));
    border: 1px solid rgba(72, 187, 120, 0.3);
    border-radius: 16px;
}
QFrame#HeaderCard {
    background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 rgba(18, 30, 22, 0.88), stop:1 rgba(11, 20, 13, 0.88));
    border: 1px solid rgba(72, 187, 120, 0.35);
    border-bottom: 2px solid rgba(8, 15, 10, 0.95);
    border-radius: 16px;
}
QLabel {
    color: #E2E8F0;
    font-family: 'Segoe UI', sans-serif;
    background: transparent;
}
QLabel#TitleLabel {
    font-size: 20px;
    font-weight: bold;
    color: #FFFFFF;
}
QLabel#SubtitleLabel {
    font-size: 12px;
    color: #A0AEC0;
}
QLabel#SectionTitle {
    font-size: 13px;
    font-weight: bold;
    color: #48BB78;
}
QLineEdit {
    background-color: rgba(10, 16, 11, 0.88);
    border: 1px solid rgba(72, 187, 120, 0.35);
    border-radius: 10px;
    padding: 10px 14px;
    color: #FFFFFF;
    font-size: 13px;
    selection-background-color: #38A169;
}
QLineEdit:focus {
    border: 1px solid #48BB78;
}
QComboBox {
    background-color: rgba(10, 16, 11, 0.88);
    border: 1px solid rgba(72, 187, 120, 0.35);
    border-radius: 10px;
    padding: 8px 12px;
    color: #FFFFFF;
    font-size: 13px;
}
QComboBox:hover {
    border: 1px solid #48BB78;
}
QComboBox::drop-down {
    border: none;
    width: 24px;
}
QComboBox QAbstractItemView {
    background-color: #121e14;
    color: #FFFFFF;
    selection-background-color: #38A169;
    border: 1px solid #2F855A;
}
QCheckBox {
    color: #CBD5E0;
    font-size: 13px;
    spacing: 8px;
    background: transparent;
}
QCheckBox::indicator {
    width: 18px;
    height: 18px;
    border-radius: 5px;
    border: 1px solid #2F855A;
    background-color: rgba(10, 16, 11, 0.88);
}
QCheckBox::indicator:checked {
    background-color: #48BB78;
    border: 1px solid #48BB78;
}
QPushButton#PrimaryButton {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #38A169, stop:1 #48BB78);
    color: white;
    font-weight: bold;
    font-size: 14px;
    border: none;
    border-radius: 10px;
    padding: 12px 24px;
}
QPushButton#PrimaryButton:hover {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #48BB78, stop:1 #68D391);
}
QPushButton#PrimaryButton:pressed {
    background-color: #2F855A;
}
QPushButton#SecondaryButton {
    background-color: rgba(22, 38, 27, 0.85);
    color: #e2e8f0;
    font-size: 12px;
    font-weight: bold;
    border: 1px solid rgba(72, 187, 120, 0.35);
    border-radius: 8px;
    padding: 8px 14px;
}
QPushButton#SecondaryButton:hover {
    background-color: rgba(32, 56, 40, 0.95);
    border: 1px solid #48BB78;
    color: white;
}
QProgressBar {
    border: 1px solid rgba(72, 187, 120, 0.25);
    border-radius: 6px;
    background-color: rgba(10, 16, 11, 0.85);
    text-align: center;
    color: white;
    font-weight: bold;
    font-size: 11px;
}
QProgressBar::chunk {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #38A169, stop:1 #48BB78);
    border-radius: 5px;
}
QListWidget {
    background-color: rgba(8, 14, 9, 0.75);
    border: 1px solid rgba(72, 187, 120, 0.25);
    border-radius: 10px;
    color: #E2E8F0;
    padding: 6px;
}
QListWidget::item {
    background: transparent;
    border: none;
    margin-bottom: 6px;
    padding: 0px;
}
QScrollBar:vertical {
    border: none;
    background: rgba(10, 16, 11, 0.5);
    width: 8px;
    border-radius: 4px;
}
QScrollBar::handle:vertical {
    background: rgba(72, 187, 120, 0.4);
    border-radius: 4px;
}
QScrollBar::handle:vertical:hover {
    background: rgba(72, 187, 120, 0.7);
}
"""

class BackgroundWidget(QWidget):
    """Background container rendering blurred abstract green wallpaper."""
    def __init__(self, bg_pixmap=None, parent=None):
        super().__init__(parent)
        self.bg_pixmap = bg_pixmap

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        painter.fillRect(self.rect(), QColor("#080c09"))
        
        if self.bg_pixmap and not self.bg_pixmap.isNull():
            scaled = self.bg_pixmap.scaled(
                self.size(),
                Qt.AspectRatioMode.KeepAspectRatioByExpanding,
                Qt.TransformationMode.SmoothTransformation
            )
            x = (self.width() - scaled.width()) // 2
            y = (self.height() - scaled.height()) // 2
            painter.drawPixmap(x, y, scaled)


class UpdateCheckerWorker(QThread):
    update_found_signal = pyqtSignal(str, str, str) # new_version, release_notes, download_url

    def run(self):
        try:
            req = urllib.request.Request(UPDATE_CHECK_URL, headers={'User-Agent': 'Mozilla/5.0'})
            with urllib.request.urlopen(req, timeout=4) as response:
                if response.status == 200:
                    data = json.loads(response.read().decode('utf-8'))
                    latest_version = data.get('version', '')
                    if latest_version and latest_version != APP_VERSION:
                        self.update_found_signal.emit(
                            latest_version,
                            data.get('release_notes', 'A new update is available!'),
                            data.get('download_url', 'https://github.com/unoduxx75-a11y')
                        )
        except Exception:
            pass


class DownloadWorker(QThread):
    progress_signal = pyqtSignal(float, str, str)
    status_signal = pyqtSignal(str)
    finished_signal = pyqtSignal(bool, dict)

    def __init__(self, url, options, save_dir):
        super().__init__()
        self.url = url
        self.options = options
        self.save_dir = save_dir

    def run(self):
        def progress_hook(d):
            if d['status'] == 'downloading':
                total_bytes = d.get('total_bytes') or d.get('total_bytes_estimate') or 0
                downloaded = d.get('downloaded_bytes', 0)
                percent = (downloaded / total_bytes * 100) if total_bytes > 0 else 0
                speed = d.get('_speed_str', 'N/A')
                eta = d.get('_eta_str', 'N/A')
                self.progress_signal.emit(percent, speed, eta)
            elif d['status'] == 'finished':
                self.progress_signal.emit(100.0, "Done", "0s")
                self.status_signal.emit("Processing output file...")

        ydl_opts = {
            'outtmpl': os.path.join(self.save_dir, '%(title)s.%(ext)s'),
            'progress_hooks': [progress_hook],
            'quiet': True,
            'no_warnings': True,
        }

        fmt_type = self.options.get('format', 'MP4 (Video)')
        quality = self.options.get('quality', '4K Ultra HD (2160p)')

        if 'MP3' in fmt_type:
            ydl_opts['format'] = 'bestaudio/best'
            ydl_opts['postprocessors'] = [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '320',
            }]
        elif 'WAV' in fmt_type:
            ydl_opts['format'] = 'bestaudio/best'
            ydl_opts['postprocessors'] = [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'wav',
            }]
        else:
            if '4K' in quality:
                ydl_opts['format'] = 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best'
            elif '2K' in quality:
                ydl_opts['format'] = 'bestvideo[height<=1440][ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best'
            elif '1080p' in quality:
                ydl_opts['format'] = 'bestvideo[height<=1080][ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best'
            elif '720p' in quality:
                ydl_opts['format'] = 'bestvideo[height<=720][ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best'
            elif '480p' in quality:
                ydl_opts['format'] = 'bestvideo[height<=480][ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best'
            elif '360p' in quality:
                ydl_opts['format'] = 'bestvideo[height<=360][ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best'
            else:
                ydl_opts['format'] = 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best'

        if self.options.get('metadata', True):
            ydl_opts['addmetadata'] = True

        cookie_browser = self.options.get('cookies', 'None')
        if cookie_browser != 'None':
            ydl_opts['cookiesfrombrowser'] = (cookie_browser.lower(),)

        try:
            self.status_signal.emit("Fetching video info...")
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(self.url, download=True)
                title = info.get('title', 'Downloaded Media')
                filename = ydl.prepare_filename(info)
                if 'MP3' in fmt_type:
                    filename = os.path.splitext(filename)[0] + '.mp3'
                elif 'WAV' in fmt_type:
                    filename = os.path.splitext(filename)[0] + '.wav'

                item_info = {
                    'title': title,
                    'file_path': filename,
                    'format': fmt_type,
                    'quality': quality,
                    'url': self.url,
                    'time': time.strftime("%H:%M:%S")
                }
                self.status_signal.emit("Download complete!")
                self.finished_signal.emit(True, item_info)
        except Exception as e:
            self.status_signal.emit(f"Error: {str(e)}")
            self.finished_signal.emit(False, {'error': str(e)})


class HistoryCardItem(QFrame):
    """Card widget for individual history items."""
    def __init__(self, info, parent=None):
        super().__init__(parent)
        self.info = info

        self.setStyleSheet("""
            QFrame {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 rgba(22, 36, 26, 0.8), stop:1 rgba(14, 24, 17, 0.8));
                border: 1px solid rgba(72, 187, 120, 0.25);
                border-radius: 10px;
            }
            QFrame:hover {
                border: 1px solid #48BB78;
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 rgba(28, 46, 33, 0.9), stop:1 rgba(18, 30, 22, 0.9));
            }
        """)

        layout = QHBoxLayout(self)
        layout.setContentsMargins(12, 10, 12, 10)
        layout.setSpacing(12)

        icon_box = QLabel("🎬" if "Video" in info['format'] else "🎵")
        icon_box.setFont(QFont("Segoe UI Emoji", 14))
        icon_box.setStyleSheet("background: transparent; border: none;")
        layout.addWidget(icon_box)

        text_layout = QVBoxLayout()
        text_layout.setSpacing(2)

        title_lbl = QLabel(info['title'])
        title_lbl.setFont(QFont("Segoe UI", 10, QFont.Weight.Bold))
        title_lbl.setStyleSheet("color: #FFFFFF; border: none; background: transparent;")

        sub_lbl = QLabel(f"{info['format']} • {info['quality']} • {info['time']}")
        sub_lbl.setFont(QFont("Segoe UI", 8))
        sub_lbl.setStyleSheet("color: #48BB78; border: none; background: transparent;")

        text_layout.addWidget(title_lbl)
        text_layout.addWidget(sub_lbl)
        layout.addLayout(text_layout, stretch=1)

        open_btn = QPushButton("📁")
        open_btn.setToolTip("Open Folder")
        open_btn.setFixedSize(32, 32)
        open_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        open_btn.setStyleSheet("""
            QPushButton {
                background-color: rgba(48, 80, 56, 0.6);
                border: 1px solid rgba(72, 187, 120, 0.3);
                border-radius: 6px;
                color: #FFFFFF;
                font-size: 13px;
            }
            QPushButton:hover {
                background-color: #38A169;
                border: 1px solid #48BB78;
            }
        """)
        open_btn.clicked.connect(lambda: QDesktopServices.openUrl(QUrl.fromLocalFile(os.path.dirname(info['file_path']))))
        layout.addWidget(open_btn)


class SettingsModal(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Settings & Updater")
        self.setFixedSize(450, 350)
        self.setStyleSheet(DARK_GREEN_GLASS_STYLE)

        layout = QVBoxLayout()
        layout.setContentsMargins(24, 24, 24, 24)

        header_layout = QHBoxLayout()
        logo_label = QLabel()
        icon_path = resource_path("app_icon.png")
        if os.path.exists(icon_path):
            pix = QPixmap(icon_path).scaled(42, 42, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
            logo_label.setPixmap(pix)
        header_layout.addWidget(logo_label)

        title_box = QVBoxLayout()
        title = QLabel("YT Downloader Pro")
        title.setObjectName("TitleLabel")
        subtitle = QLabel(f"Version {APP_VERSION} • High Speed Media Downloader")
        subtitle.setObjectName("SubtitleLabel")
        title_box.addWidget(title)
        title_box.addWidget(subtitle)
        header_layout.addLayout(title_box)
        layout.addLayout(header_layout)

        layout.addSpacing(15)

        info_box = QFrame()
        info_box.setObjectName("CardFrame")
        ib_layout = QVBoxLayout(info_box)
        ib_layout.addWidget(QLabel("<b>Developer:</b> UNO XEO"))
        ib_layout.addWidget(QLabel("<b>License:</b> Free & Open Source"))
        ib_layout.addWidget(QLabel("<b>Auto Updater:</b> Enabled (GitHub Releases)"))
        layout.addWidget(info_box)

        layout.addSpacing(15)

        btn_layout = QHBoxLayout()
        gh_btn = QPushButton("GitHub Profile")
        gh_btn.setObjectName("SecondaryButton")
        gh_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        gh_btn.clicked.connect(lambda: QDesktopServices.openUrl(QUrl("https://github.com/unoduxx75-a11y")))
        btn_layout.addWidget(gh_btn)

        close_btn = QPushButton("Close")
        close_btn.setObjectName("PrimaryButton")
        close_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        close_btn.clicked.connect(self.accept)
        btn_layout.addWidget(close_btn)

        layout.addLayout(btn_layout)
        self.setLayout(layout)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("YouTube Media Downloader Pro")
        self.resize(960, 620)
        self.setMinimumSize(880, 560)

        # Set App Icon (White Cat)
        icon_path = resource_path("app_icon.png")
        if os.path.exists(icon_path):
            self.setWindowIcon(QIcon(icon_path))

        # Blurred Background Image
        bg_path = resource_path("bg_green_blurred.png")
        if os.path.exists(bg_path):
            self.bg_pixmap = QPixmap(bg_path)
        else:
            self.bg_pixmap = None

        self.save_directory = str(Path.home() / "Downloads")
        self.init_ui()

        # Check for updates in background without delaying launch speed
        self.checker = UpdateCheckerWorker()
        self.checker.update_found_signal.connect(self.on_update_found)
        self.checker.start()

    def init_ui(self):
        self.bg_canvas = BackgroundWidget(self.bg_pixmap, self)
        self.setCentralWidget(self.bg_canvas)

        root_layout = QVBoxLayout(self.bg_canvas)
        root_layout.setContentsMargins(20, 16, 20, 16)
        root_layout.setSpacing(14)

        # Header Glass Card
        header_card = QFrame()
        header_card.setObjectName("HeaderCard")
        header_shadow = QGraphicsDropShadowEffect(self)
        header_shadow.setBlurRadius(15)
        header_shadow.setColor(QColor(0, 0, 0, 150))
        header_shadow.setYOffset(4)
        header_card.setGraphicsEffect(header_shadow)

        header_layout = QHBoxLayout(header_card)
        header_layout.setContentsMargins(16, 12, 16, 12)

        logo_label = QLabel()
        icon_path = resource_path("app_icon.png")
        if os.path.exists(icon_path):
            pix = QPixmap(icon_path).scaled(42, 42, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
            logo_label.setPixmap(pix)
        header_layout.addWidget(logo_label)

        title_box = QVBoxLayout()
        header_title = QLabel("YT DOWNLOADER PRO")
        header_title.setFont(QFont("Segoe UI", 13, QFont.Weight.Bold))
        header_title.setStyleSheet("color: #ffffff; border: none; background: transparent;")

        header_sub = QLabel("Fast, 4K video & audio downloader by UNO XEO")
        header_sub.setFont(QFont("Segoe UI", 9))
        header_sub.setStyleSheet("color: #A0AEC0; border: none; background: transparent;")

        title_box.addWidget(header_title)
        title_box.addWidget(header_sub)
        header_layout.addLayout(title_box)

        header_layout.addStretch()

        self.update_btn = QPushButton("🚀 Update Available!")
        self.update_btn.setObjectName("SecondaryButton")
        self.update_btn.setStyleSheet("""
            QPushButton {
                background-color: #38A169;
                color: #FFFFFF;
                font-weight: bold;
                border: 1px solid #48BB78;
                border-radius: 8px;
                padding: 8px 14px;
            }
            QPushButton:hover {
                background-color: #48BB78;
            }
        """)
        self.update_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.update_btn.setVisible(False)
        header_layout.addWidget(self.update_btn)

        settings_btn = QPushButton("⚙️ Settings")
        settings_btn.setObjectName("SecondaryButton")
        settings_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        settings_btn.clicked.connect(self.open_settings)
        header_layout.addWidget(settings_btn)

        root_layout.addWidget(header_card)

        # Main Body Splitter
        body_splitter = QSplitter(Qt.Orientation.Horizontal)

        # Left Glass Card (Controls)
        left_card = QFrame()
        left_card.setObjectName("CardFrame")
        left_shadow = QGraphicsDropShadowEffect(self)
        left_shadow.setBlurRadius(20)
        left_shadow.setColor(QColor(0, 0, 0, 160))
        left_shadow.setYOffset(6)
        left_card.setGraphicsEffect(left_shadow)

        left_layout = QVBoxLayout(left_card)
        left_layout.setContentsMargins(20, 20, 20, 20)
        left_layout.setSpacing(14)

        url_label = QLabel("Video or Playlist URL:")
        url_label.setObjectName("SectionTitle")
        left_layout.addWidget(url_label)

        self.url_input = QLineEdit()
        self.url_input.setPlaceholderText("Paste YouTube, Vimeo, or video link here...")
        left_layout.addWidget(self.url_input)

        opts_layout = QHBoxLayout()

        fmt_vbox = QVBoxLayout()
        fmt_vbox.addWidget(QLabel("Format:"))
        self.format_combo = QComboBox()
        self.format_combo.addItems(["MP4 (Video)", "MP3 (Audio)", "WAV (Audio)"])
        self.format_combo.currentTextChanged.connect(self.on_format_changed)
        fmt_vbox.addWidget(self.format_combo)
        opts_layout.addLayout(fmt_vbox)

        quality_vbox = QVBoxLayout()
        quality_vbox.addWidget(QLabel("Quality:"))
        self.quality_combo = QComboBox()
        self.quality_combo.addItems([
            "4K Ultra HD (2160p)",
            "2K Quad HD (1440p)",
            "1080p Full HD",
            "720p HD",
            "480p SD",
            "360p Low"
        ])
        quality_vbox.addWidget(self.quality_combo)
        opts_layout.addLayout(quality_vbox)

        left_layout.addLayout(opts_layout)

        adv_layout = QHBoxLayout()
        self.meta_check = QCheckBox("Preserve Metadata & Thumbnail")
        self.meta_check.setChecked(True)
        adv_layout.addWidget(self.meta_check)

        cookies_vbox = QVBoxLayout()
        cookies_vbox.addWidget(QLabel("Browser Cookies:"))
        self.cookies_combo = QComboBox()
        self.cookies_combo.addItems(["None", "Chrome", "Firefox", "Edge", "Brave"])
        cookies_vbox.addWidget(self.cookies_combo)
        adv_layout.addLayout(cookies_vbox)

        left_layout.addLayout(adv_layout)

        dir_layout = QHBoxLayout()
        self.dir_label = QLabel(f"Save Path: {self.save_directory}")
        self.dir_label.setObjectName("SubtitleLabel")
        dir_layout.addWidget(self.dir_label, stretch=1)

        browse_btn = QPushButton("Browse...")
        browse_btn.setObjectName("SecondaryButton")
        browse_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        browse_btn.clicked.connect(self.choose_directory)
        dir_layout.addWidget(browse_btn)
        left_layout.addLayout(dir_layout)

        self.download_btn = QPushButton("⚡ Start Download")
        self.download_btn.setObjectName("PrimaryButton")
        self.download_btn.setFixedHeight(46)
        self.download_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.download_btn.clicked.connect(self.start_download)
        left_layout.addWidget(self.download_btn)

        self.progress_bar = QProgressBar()
        self.progress_bar.setValue(0)
        self.progress_bar.setFixedHeight(12)
        left_layout.addWidget(self.progress_bar)

        self.status_label = QLabel("Ready to download")
        self.status_label.setObjectName("SubtitleLabel")
        left_layout.addWidget(self.status_label)

        left_layout.addStretch()
        body_splitter.addWidget(left_card)

        # Right Glass Card (Download History)
        right_card = QFrame()
        right_card.setObjectName("CardFrame")
        right_shadow = QGraphicsDropShadowEffect(self)
        right_shadow.setBlurRadius(20)
        right_shadow.setColor(QColor(0, 0, 0, 160))
        right_shadow.setYOffset(6)
        right_card.setGraphicsEffect(right_shadow)

        right_layout = QVBoxLayout(right_card)
        right_layout.setContentsMargins(20, 20, 20, 20)

        history_title = QLabel("DOWNLOAD HISTORY")
        history_title.setObjectName("SectionTitle")
        right_layout.addWidget(history_title)

        self.history_list = QListWidget()
        right_layout.addWidget(self.history_list)

        clear_btn = QPushButton("Clear History")
        clear_btn.setObjectName("SecondaryButton")
        clear_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        clear_btn.clicked.connect(self.history_list.clear)
        right_layout.addWidget(clear_btn)

        body_splitter.addWidget(right_card)

        body_splitter.setSizes([540, 380])
        root_layout.addWidget(body_splitter)

        self.setStyleSheet(DARK_GREEN_GLASS_STYLE)

    def on_update_found(self, version, notes, download_url):
        self.update_btn.setVisible(True)
        self.update_btn.setText(f"🚀 Update v{version} Available!")
        self.update_btn.clicked.connect(lambda: QDesktopServices.openUrl(QUrl(download_url)))
        QMessageBox.information(
            self,
            "New Update Available",
            f"<b>A new version (v{version}) of YT Downloader Pro is available!</b><br><br>{notes}"
        )

    def on_format_changed(self, fmt_text):
        if "Audio" in fmt_text:
            self.quality_combo.setEnabled(False)
        else:
            self.quality_combo.setEnabled(True)

    def choose_directory(self):
        chosen = QFileDialog.getExistingDirectory(self, "Select Download Folder", self.save_directory)
        if chosen:
            self.save_directory = chosen
            self.dir_label.setText(f"Save Path: {self.save_directory}")

    def open_settings(self):
        modal = SettingsModal(self)
        modal.exec()

    def start_download(self):
        url = self.url_input.text().strip()
        if not url:
            QMessageBox.warning(self, "Missing URL", "Please enter or paste a valid video URL.")
            return

        options = {
            'format': self.format_combo.currentText(),
            'quality': self.quality_combo.currentText(),
            'metadata': self.meta_check.isChecked(),
            'cookies': self.cookies_combo.currentText()
        }

        self.download_btn.setEnabled(False)
        self.progress_bar.setValue(0)
        self.status_label.setText("Starting download...")

        self.worker = DownloadWorker(url, options, self.save_directory)
        self.worker.progress_signal.connect(self.on_progress)
        self.worker.status_signal.connect(self.on_status_update)
        self.worker.finished_signal.connect(self.on_download_finished)
        self.worker.start()

    def on_progress(self, percent, speed, eta):
        self.progress_bar.setValue(int(percent))
        self.status_label.setText(f"Downloading... {percent:.1f}% ({speed} • ETA: {eta})")

    def on_status_update(self, msg):
        self.status_label.setText(msg)

    def on_download_finished(self, success, info):
        self.download_btn.setEnabled(True)
        if success:
            self.status_label.setText("Download completed successfully! 🎉")
            self.progress_bar.setValue(100)

            card_widget = HistoryCardItem(info)
            list_item = QListWidgetItem(self.history_list)
            list_item.setSizeHint(card_widget.sizeHint())
            self.history_list.addItem(list_item)
            self.history_list.setItemWidget(list_item, card_widget)

            self.url_input.clear()
        else:
            QMessageBox.critical(self, "Download Failed", f"Could not download video:\n{info.get('error')}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
