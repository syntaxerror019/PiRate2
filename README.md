# PiRate (Revison 2) Cable Box
Stream your favorite movies and TV shows at no price!

**Disclaimer:** This software is simply a wrapper for The Pirate Bay (TPB) torrent sharing site and the QBittorrent API. Use at your own discretion, as pirating copyrighted material is ILLEGAL and put you in court and/ or under heavy fines! I am in no way responsible for your actions regarding the use of this software. You have been warned.

A nice and tidily packaged "wrapper" for QBitorrent and 1337x. Find and watch any movie from the comfort of your couch, at no cost! 

*Side Note:*
For all torrenting, a VPN is strongly recommended. I personally use [Proton VPN](https://protonvpn.com) as they have good support. 

## Features
- Downloading, streaming, and interfacing movies (torrents) is all handled within PiRate2 cable box.
- Run on any linux machine. Including RPi boards (RPi 3 and newer due to video performance requirements)
- Easy control; use any device as a remote! Any smartphone, laptop, tablet, etc.
- Basic UI; intuitive for anybody to learn real quick.

## Installation
### 1. Clone the Repository
```sh
git clone https://github.com/syntaxerror019/PiRate2.git
cd PiRate2
```

### 1.5 Create Virtual Environment (optional)
This step is optional, however it often times resolves package errors and conflicts
```sh
python3 -m venv .env
```

### 2. Install Dependencies
```sh
pip install -r requirements.txt
```

### 3. Install VLC Media Player
#### Windows (via Chocolatey):
```sh
choco install vlc
```
#### macOS (via Homebrew):
```sh
brew install --cask vlc
```
#### Linux (Debian-based):
```sh
sudo apt update && sudo apt install vlc
```

### 4. Install qBittorrent
#### Windows (via Chocolatey):
```sh
choco install qbittorrent
```
#### macOS (via Homebrew):
```sh
brew install --cask qbittorrent
```
#### Linux (Debian-based):
```sh
sudo apt update && sudo apt install qbittorrent
```

### 5. Set Up a VPN
To ensure secure media streaming, set up a VPN:
- **Proton VPN (Recommended):** [Download and Install](https://protonvpn.com/download)
  I personally have had some problems with the GUI on Linux. This may or may not apply to you.
  

### 6. Run main.py
```sh
python3 main.py
```
A window will open up and direct you with further instructions. Be sure to start QBittorrent, as it is required for this script to operate properly.

**You will likely need to configure `config.yaml` to set the correct download location of QBittorrent.**

## Troubleshooting
If you have questions or comments open an issue.
If you want to suggest something, please create a pull request.
