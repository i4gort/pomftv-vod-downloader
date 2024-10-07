import sys
import getopt
import re
import html
import inquirer
import requests as req
from pathlib import Path
from tabulate import tabulate
from yt_dlp import YoutubeDL

##################################################################
#                       CONFIGURATION (?)                        #
##################################################################
#     Creates a folder from wherever the script is called        #
#      Beware it creates a folder with username inputted         #
#          Put the path you desire to store vods                 #
#     e.g. C:\Users\Anon\Videos\PomfTV OR ~/Videos/PomfTV        #
##################################################################

DEFAULT_DIR = ("./PomfTV")                                             

#################################################################
############# CONSTANTS #############

URL_VOD = "https://pomf.tv/api/history/getuserhistory.php?user="
URL_FETCH_USER = "https://pomf.tv/api/streams/getinfo.php?data=streamdata&stream="

############### CLASS ###############
class PomfTVDownloader:
    def __init__(self, download_path):
        # Append user after each

        self.DOWNLOAD_PATH = Path(download_path)

    # Get username for vod history,
    # For some reason it's case sensitive so we have to have to do something like get_user(user)["streamer"]
    # Where the field ["streamer"] is the correct username used in vod history
    def get_user(self, user: str):
        url = URL_FETCH_USER + user
        try:
            response = req.get(url)
            data = response.json()
            if "error" in data:
                print(data["message"])
                return None
                sys.exit(-1)
            elif "result" in data:
                return data
        except Exception as e:
            print(f"Error: {e}")
            return None
            sys.exit(-1)

    # Fetch user's vod history as json
    def fetch_vod_history(self, user: str):
        try:
            url = URL_VOD + user
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

############### END CLASS ###############
###############    OPT    ###############
help_message = f"""Usage:
 {sys.argv[0]} [OPTION] parameter

Options:
 -u, --user   <USERNAME>      Download through username, select which vod to download
 -U, --url    <URL>           Download through url e.g. https://pomf.tv/streamhistory/username/id
 -s, --search <USERNAME>      Search user's info
 -d, --dir    <DIRECTORY>     Exact location for file downloads"""


# Require two parameters
# Download from a streamhistory url e.g. https://pomf.tv/streamhistory/OkYmir/94972
# It extracts the user and id and then use download_vod() with the correct parameters
def url_opt(url_arg: str, handler: PomfTVDownloader):
    pattern = r"https://pomf\.tv/streamhistory/([A-Za-z0-9_]+)/(\d+)"
    match = re.search(pattern, url_arg)

    if match != None:
        user = match.group(1)
        vod_id = match.group(2)

        streamer_info = handler.get_user(user)
        if streamer_info != None:
            vod_history = handler.fetch_vod_history(streamer_info["streamer"])
            if vod_id in vod_history:
                handler.download_vod("https:" + vod_history[vod_id]["raw_url"], user)
            else:
                print("Invalid id. Perhaps it doesn't exist anymore?")
        else:
            pass
    else:
        print("Invalid url.")
        print("Expected: https://pomf.tv/streamhistory/username/id")
        # Nor {url_arg: <9} neither url_arg.rjust(9) worked
        print(f"Got:      {url_arg}")
        sys.exit(-1)
        
# Requires two parameters
# Search the user, idk... For debug and stalking purposes    
def search_opt(user_arg: str, handler: PomfTVDownloader):
    info = handler.get_user(user_arg)
    if (info != None):
        print("-" * 23)
        print(f"--User found: {info['streamer']}")
        print(f"Profile Image: {'https://pomf.tv/img/avatars/' + info['profileimage']}")
        print(f"Online: {'NO' if (info['stream_online'] == 0) else 'YES'}")
        print(f"Followers: {info['followers']}")
        print(f"Viewers: {info['viewers']}")
        print(f"Stream Title: {info['streamtitle']}")
        print(f"Stream Info: {info['streaminfo']}")
        print(f"Stream Banner: {'https://pomf.tv/img/stream/thumb/' + info['streambanner']}") 
#       print(f"Protection: {info['protection']}) # Empty so far
#       print(f"Stream Description:\n{html.unescape(info['streamdesc'])}") # Raw html
        print(f"Start Time: {info['starttime']}")
        print(f"Chat Access: {'NO' if (info['chat_access'] == False) else 'YES'}")
        print("-" * 23)
    else:
        sys.exit(-1)
        
# Requires two parameters
# Uses the "old" way of download
# Makes the user select which vods to download
def user_opt(user_arg: str, handler: PomfTVDownloader):
    user = handler.get_user(user_arg)
    if user:
        vod_history = handler.fetch_vod_history(user["streamer"]) # Names differ
        try:
            vod_ids = handler.user_input(vod_history)
            if vod_ids != None:
                for number_id in vod_ids:
                    url = "https:" + vod_history[number_id]["raw_url"]
                    handler.download_vod(url, user["streamer"])
            else:
                print("There's no VOD Available.")
        except Exception as error:
            print(f"Error: {error}")
        
############### OPT END ###############
########################### MAIN #################################

if __name__ == "__main__":
    try:
        ############### Handle OPTIONS ###############
        try:
            argv = sys.argv[1:]
            opts, args = getopt.getopt(argv, "hU:u:s:d:", ["help", "url=",
                                                   "user=","search=", "dir="])
        except getopt.GetoptError as err:
            print(f"ERROR: {err}")
            print(help_message)
            sys.exit(-1)

        # Check if nothing is passed AKA Opts is empty
        if not opts:
            print(help_message)
            sys.exit(0)
        ############# END Handle OPTIONS #############

        handler = PomfTVDownloader(DEFAULT_DIR)
        for opt, arg in opts:
            if opt in ["-d", "--dir"]:
                DEFAULT_DIR = arg
                handler = PomfTVDownloader(DEFAULT_DIR)
                    
        for opt, arg in opts:
            if opt in ["-s", "--search"]:
                search_opt(arg, handler)
                sys.exit(0)
                            
            elif opt in ["-U", "--url"]:
                print(f"Downloading to: {DEFAULT_DIR}")
                url_opt(arg, handler)
                sys.exit(0)
                            
            elif opt in ["-u", "--user"]:
                print(f"Downloading to: {DEFAULT_DIR}")
                user_opt(arg, handler)
                sys.exit(0)
                            
            elif opt in ["--h", "-h", "--help"]:
                print(help_message)
                sys.exit(0)
    except KeyboardInterrupt:
        print("\nExiting")