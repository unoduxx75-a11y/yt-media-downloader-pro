# YouTube Media Downloader Pro

A fast, easy-to-use YouTube downloader for downloading videos and audio in multiple formats and qualities. Built with Python and PyQt6, this app supports batch-friendly downloads, cross-platform execution, and an automatic update system.

## Features

- Download YouTube videos and playlists
- Save audio as MP3 or WAV
- Choose video quality from 360p up to 4K
- Browse and select a custom save folder
- Preserve metadata and thumbnails when enabled
- Compatible with Windows, macOS, and Linux
- Built-in GitHub auto-updater

## App Preview

This project includes a polished desktop UI with a dark green glassmorphism design and download history panel.

## Requirements

- Python 3.10+
- PyQt6
- yt-dlp
- FFmpeg (required for audio conversion and video processing)

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/unoduxx75-a11y/yt-media-downloader-pro.git
   cd yt-media-downloader-pro
   ```

2. Create and activate a virtual environment (optional but recommended):

   ```bash
   python -m venv .venv
   source .venv/bin/activate   # Linux/macOS
   .venv\Scripts\activate      # Windows
   ```

3. Install dependencies:

   ```bash
   pip install PyQt6 yt-dlp
   ```

4. Install FFmpeg and make sure it is available in your system PATH.

5. Run the app:

   ```bash
   python main.py
   ```

   Or on Unix-like systems:

   ```bash
   ./run_linux.sh
   ```

   On macOS:

   ```bash
   ./run_mac.sh
   ```

## How to Use

1. Paste a YouTube video or playlist URL.
2. Select the format: MP4, MP3, or WAV.
3. Choose a quality level.
4. Pick a save directory.
5. Click Start Download.
6. View the saved files in your download history panel.

## Auto-Updater

The app checks for updates at startup by polling the public GitHub raw file:

```text
https://raw.githubusercontent.com/unoduxx75-a11y/yt-downloader-pro/main/version.json
```

If a newer version is available, the app shows an update notification and opens the GitHub release page.

### To release a new update

1. Edit `version.json` in the repository.
2. Increase the version value, for example from `1.0.0` to `1.0.1`.
3. Add release notes in the `release_notes` field.
4. Push the change to GitHub.
5. Users running the app will receive an automatic update prompt.

## Project Files

- `main.py` — main application code
- `version.json` — updater configuration and release metadata
- `app_icon.png` and `app_icon.ico` — app icon assets
- `bg_green_blurred.png` — background wallpaper
- `run_linux.sh` — Linux launcher script
- `run_mac.sh` — macOS launcher script
- `BUILD_CROSS_PLATFORM.md` — cross-platform build notes

## Notes

- This app is designed for downloading media from platforms supported by `yt-dlp`.
- Always respect the platform's terms of service and local copyright laws.
- For best results, keep FFmpeg installed and ensure Python dependencies are current.

## License

This project does not currently declare a license file. If you plan to distribute or publish it publicly, consider adding an open-source license such as MIT.

## Repository

https://github.com/unoduxx75-a11y/yt-media-downloader-pro

