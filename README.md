# YouTube Media Downloader Pro

## How Auto-Updater Works
The application checks `https://raw.githubusercontent.com/unoduxx75-a11y/yt-downloader-pro/main/version.json` on startup in a background thread.

### To release a new update:
1. Edit `version.json` in your repository.
2. Change `"version": "1.0.0"` to a higher version number like `"version": "1.0.1"`.
3. Add release notes in `"release_notes"`.
4. Push to your GitHub repository `unoduxx75-a11y/yt-downloader-pro`.

All users running the app will automatically get an **"🚀 Update Available!"** notification popup and button leading to your GitHub release.

## Files included in this repository folder:
- `main.py` -> Source code
- `version.json` -> Updater configuration file
- `app_icon.png` & `app_icon.ico` -> Cat icon logo
- `bg_green_blurred.png` -> Green blurred background wallpaper
