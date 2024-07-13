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
        downloader = PomfTVDownloader(DOWNLOAD_PATH)

        user = downloader.get_correct_username(str(input("Stream username: ").strip()))
        print("Wait a second...")
        if user:
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

    except Exception as error:
        print(error)
    except KeyboardInterrupt:
        print("\nExiting...")
