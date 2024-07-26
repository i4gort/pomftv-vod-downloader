from yt_dlp import YoutubeDL
import requests as req
import inquirer
from tabulate import tabulate

class PomfTVDownloader:
    def __init__(self, download_path):
        # Append user after each

        self.DOWNLOAD_PATH = download_path
        self.URL_VOD = "https://pomf.tv/api/history/getuserhistory.php?user="
        self.URL_FETCH_USER = "https://pomf.tv/api/streams/getinfo.php?data=streamdata&stream="

    # Get correct username for vod history, for some reason it's case sensitive
    def get_correct_username(self, user: str):
        url = self.URL_FETCH_USER + user
        try:
            response = req.get(url)
            data = response.json()
            if "error" in data:
                print(data["message"])
                return None
            elif "result" in data:
                return data["streamer"]
        except Exception as e:
            print(f"Error: {e}")
            return None

    # Fetch user's vod history as json
    def fetch_vod_history(self, user: str):
        try:
            url = self.URL_VOD + user
            response = req.get(url)
            data = response.json()
            return data

        except Exception as e:
            print(f"Error: {e}")
            return None

    # YoutubeDL Hooks, don't brother with
    def progress_hooks(self, d):
        if d['status'] == 'finished':
            print(f"\nDownloaded to {str(self.DOWNLOAD_PATH / self.user)}\n")

    # Download vod using YoutubeDL
    def download_vod(self, url: str, user: str):
        self.user = user
        ydl_opts = {
            "outtmpl": str(self.DOWNLOAD_PATH / user / "%(title)s.%(ext)s"),
            "quiet": True,
            "noprogress": False,
            "progress_hooks": [self.progress_hooks]
        }
        try:
            with YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
        except Exception as e:
            print(f"Error downloading: {e}")

    # Pretty user input
    def user_input(self, json_data: dict):
        if len(json_data) > 1:
            json_data.pop('result')
            data_to_display = []
            print("Available VODs:")
            for key, value in json_data.items():
                data_to_display.append([value['id'], value['stream_title'], value['date']])

            print(tabulate(data_to_display, headers=['ID', 'Stream Title', 'Date'], tablefmt='fancy_grid', colalign=('center', 'center', 'center')))

            questions = [
                inquirer.Checkbox('ID',
                message="Which VOD would you like to download (space to select/enter to confirm)",
                choices=json_data)
            ]
            answer = inquirer.prompt(questions)

            if answer == None:
                print("No selection made.")
                exit(1)
            else:
                return answer['ID']
        else:
            return None

