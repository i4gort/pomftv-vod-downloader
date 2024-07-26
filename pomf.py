from sys import argv
from pathlib import Path
from modules import PomfTVDownloader

##################################################################
#                       CONFIGURATION (?)                        #
##################################################################
# Creates a folder from wherever the script is called
# Beware it creates a folder with username inputted
DOWNLOAD_PATH = Path("./PomfTV") 
##################################################################

if __name__ == "__main__":
    try:
        # Initialize
        downloader = PomfTVDownloader(DOWNLOAD_PATH)

        # Check if there's an argument to use as the username, else prompt it
        if len(argv) != 1:
            user = downloader.get_correct_username(argv[1])
        else:
            user = downloader.get_correct_username(str(input("Stream username: ").strip()))


        # Check if user exists
        if user:
            # Pass the whole vod history into json_data and try to download for each selected ID
            print("Wait a second...")
            json_data = downloader.fetch_vod_history(user)
            try:
                vod_id = downloader.user_input(json_data)
                if vod_id:
                    for number_id in vod_id:
                        url = "https:" + json_data[number_id]["raw_url"]
                        downloader.download_vod(url, user)
                else:
                    print("There's no VOD available.")

            except Exception as e:
                print(f"Error: {e}")

    except KeyboardInterrupt:
        print("\nExiting...")
