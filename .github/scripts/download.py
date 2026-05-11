import json, os, urllib.request
idx = int(os.environ['CURRENT_INDEX'])
with open(f"all_videos_info/video_{idx}.json", "r") as f:
    info = json.load(f)
folder = info['folder']
filename = info['filename']
dl_url = info['dl_url']
os.makedirs(f"release_files/{folder}", exist_ok=True)
print(f"Downloading [{idx+1}]: {filename}")
urllib.request.urlretrieve(dl_url, f"release_files/{folder}/{filename}")
