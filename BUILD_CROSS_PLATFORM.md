# Building YouTube Media Downloader Pro for macOS and Linux

Because PyInstaller produces native OS-specific binaries (an `.app` bundle / Unix executable on macOS and a ELF binary / AppImage on Linux), binaries must be compiled on each respective target system or built automatically via **GitHub Actions**.

We have added a pre-configured **GitHub Actions Workflow** file in `.github/workflows/build.yml` inside your project repo!

---

## 🛠 Option 1: Automated Cross-Platform Build via GitHub Actions (Recommended)

When you push your code to GitHub (`unoduxx75-a11y/yt-downloader-pro`), GitHub's cloud servers will automatically build all 3 versions for you simultaneously:
- 🪟 `YT-Downloader-Pro-Windows.exe`
- 🍎 `YT-Downloader-Pro-macOS.dmg` / `.app`
- 🐧 `YT-Downloader-Pro-Linux`

---

## 💻 Option 2: Building Manually on macOS or Linux

### On macOS:
1. Open Terminal and clone your repo:
   ```bash
   git clone https.github.com/unoduxx75-a11y/yt-downloader-pro.git
   cd yt-downloader-pro
   ```
2. Install Python dependencies:
   ```bash
   pip install PyQt6 yt-dlp pillow pyinstaller
   ```
3. Run PyInstaller build command:
   ```bash
   pyinstaller --noconfirm --onefile --windowed --icon="app_icon.png" --add-data "app_icon.png:." --add-data "bg_green_blurred.png:." main.py
   ```
4. Find your macOS app bundle in `dist/main.app`!

---

### On Linux (Ubuntu / Debian / Arch / Fedora):
1. Open Terminal and install system dependencies:
   ```bash
   sudo apt update && sudo apt install python3-pip python3-pyqt6 ffmpeg
   ```
2. Install Python dependencies:
   ```bash
   pip install yt-dlp pillow pyinstaller
   ```
3. Run PyInstaller build command:
   ```bash
   pyinstaller --noconfirm --onefile --windowed --icon="app_icon.png" --add-data "app_icon.png:." --add-data "bg_green_blurred.png:." main.py
   ```
4. Find your Linux standalone executable in `dist/main`!
