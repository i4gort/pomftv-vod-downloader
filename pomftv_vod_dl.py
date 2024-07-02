from pathlib import Path
from yt_dlp import YoutubeDL
from tabulate import tabulate
import sys
import requests as req
import inquirer

# Append user after each
URL_VOD = "https://pomf.tv/api/history/getuserhistory.php?user="
URL_FETCH_USER = "https://pomf.tv/api/streams/getinfo.php?data=streamdata&stream="

##################################################################
#                                                                #
#                       CONFIGURATION (?)                        #
#                                                                #
##################################################################

DOWNLOAD_PATH = Path("./PomfTV") # Same folder as the script by default. DO NOT FORGET THE LAST "/" !!!!!

##################################################################

# Get the correct username for vod history, for some reason it is case sensitive
def fetch_user_info(user: str):
    url = URL_FETCH_USER + user
    try:
        response = req.get(url)
        data = response.json()
        if "error" in data:
            print(data["message"])
            sys.exit()
        elif "result" in data:
            return data["streamer"]
    except Exception as e:
        print(f"Error: {e}")

# Fetch user's vod history as json
def fetch_vod_history(user: str):
    try:
        url = URL_VOD + user
        response = req.get(url)
        data = response.json()
        return data

    except Exception as e:
        print(f"Error: {e}")
        sys.exit()

# YoutubeDL Hooks, don't bother with
def progress_hooks(d):
    if d['status'] == 'finished':
        print(f"\nDownloaded to {str(DOWNLOAD_PATH / user)}")

# Download vod using YoutubeDL
def download_vod(url: str):
    ydl_opts = {
            "outtmpl": str(DOWNLOAD_PATH / user / "%(title)s.%(ext)s"), # Default config using the serverside filename. Change as you wish
            "quiet": True,
            "noprogress": False,
            "progress_hooks": [progress_hooks] # The above function
            }
    try:
        with YoutubeDL(ydl_opts) as ydl:
            ydl.download(url)
    except Exception:
        pass # YoutubeDL will handle that

# User input
def user_input(json_data: dict):
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

            return answer['ID']
        else:
            return None

# Main script, might change to a separated file
if __name__ == "__main__":
    try:
        user = fetch_user_info(str(input("Stream username: ").strip())) 
        print("Wait a second...")

        if user:
            json_data = fetch_vod_history(user)


            try:
                vod_id = user_input(json_data)
                if vod_id != None:
                    try:
                        for number_id in vod_id:
                            url = "https:" + json_data[number_id]["raw_url"]
                            download_vod(url)
                    
                    except Exception:
                        print("Invalid ID.")
                else:
                    print("There's no VOD available.")


            except:
                pass

    except KeyboardInterrupt:
        print("\nExiting...")
