import requests
import os

def download_latin_font():
    url = "https://github.com/googlefonts/noto-fonts/raw/main/hinted/ttf/NotoSans/NotoSans-Regular.ttf"
    print(f"Downloading font from {url}...")
    try:
        r = requests.get(url, allow_redirects=True)
        r.raise_for_status()
        with open("NotoSans-Regular.ttf", "wb") as f:
            f.write(r.content)
        print("Latin Font downloaded successfully.")
    except Exception as e:
        print(f"Failed to download font: {e}")

if __name__ == "__main__":
    download_latin_font()
