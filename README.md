# Pomf.tv VOD Downloader
[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://gnu.org/licenses/gpl-3.0)

An *amateurish* program in python to download VODs from Pomf.tv using their **[public API](https://pomf.tv/help#api)**.

## Requirements
- Python 3.x
- `yt_dlp` (a fork of youtube-dl)
- `tabulate`
- `inquirer`
- `requests`

## Usage
1. Clone or downlod the script.
2. Install the required libraries by running:
```
pip install -r requirements.txt
```
3. Run the script:
```
python pomftv_vod_dl.py
```
4. Enter the streamer's username when prompted.
5. Choose the VOD(s) you want to download from the list.

## Configuration
- **DOWNLOAD_PATH**: Default download path for VODs. Default is `./PomfTV`

## TODO

- [ ] A better project name
- [X] Better ID choosing 
- [X] Multiple download
- [X] Configuration line
- [X] Downloaded VODs folder
- [ ] Somehow use **[lower ping servers](https://pomf.tv/help#streaming)**

## Other Repositories
- [ATF](https://git.allthefallen.moe/i4gor/pomf-vod-dl)
- [Github](https://github.com/i4gort/pomftv-vod-downloader)
