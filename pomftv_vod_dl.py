from yt_dlp import YoutubeDL
import sys
import requests as req

# Append user after each
URL_VOD = "https://pomf.tv/api/history/getuserhistory.php?user="
URL_FETCH_USER = "https://pomf.tv/api/streams/getinfo.php?data=streamdata&stream="

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

# Download vod using YoutubeDL
def download_vod(url: str):
    try:
        with YoutubeDL() as ydl:
            ydl.download(url)
    except Exception:
        pass # YoutubeDL will handle that




# Main script, might change to a separated file
if __name__ == "__main__":
    try:
        user = fetch_user_info(str(input("Stream username: "))) 
        print("Wait a second...")

        if user:
            json_data = fetch_vod_history(user)

            print("Available VODs:")
            for key, value in json_data.items():
                if key != 'result':
                    print(f"ID: {key}") 
                    print(f"Date: {value['date']}")
                    print(f"Stream Title: {value['stream_title']}\n")

            vod_id = str(input("Enter a VOD ID: "))
            if vod_id is not None:
                try:
                    url = "https:" + json_data[vod_id]["raw_url"]
                    download_vod(url)
                
                except Exception:
                    print("Invalid ID")

    except KeyboardInterrupt:
        print("\nExiting...")
