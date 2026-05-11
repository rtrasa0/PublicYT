import os, sys, time, re, requests, json
from datetime import datetime

URL = os.environ['CURRENT_URL']
IDX = int(os.environ['CURRENT_INDEX'])
FMT = os.environ['INPUT_FORMAT']
QUAL = os.environ['INPUT_QUALITY']
is_audio = (FMT == 'mp3')

if is_audio:
    valid = ['64kbps','128kbps','192kbps','320kbps']
    if QUAL not in valid: QUAL = '192kbps'
else:
    valid = ['144p','240p','360p','480p','720p','1080p','1440p','2160p']
    if QUAL not in valid: QUAL = '720p'

payload = {
    "url": URL,
    "os": "linux",
    "output": {"type": "audio" if is_audio else "video", "format": FMT}
}
if is_audio:
    payload["audio"] = {"bitrate": QUAL}
else:
    payload["output"]["quality"] = QUAL

s = requests.Session()
s.headers.update({"User-Agent": "Mozilla/5.0"})
s.get("https://media.ytmp3.gg/")
resp = s.post("https://hub.ytconvert.org/api/download", json=payload, timeout=30)
resp.raise_for_status()
data = resp.json()

status_url = data['statusUrl']
title = data.get('title', 'video')

dl_url = None
for _ in range(150):
    time.sleep(2)
    r = s.get(status_url, timeout=20)
    st = r.json()
    if st.get('status') == 'completed':
        dl_url = st.get('downloadUrl')
        break
    if st.get('status') == 'failed':
        print(f"::error::Video {IDX} failed")
        sys.exit(1)
if not dl_url:
    print(f"::error::Video {IDX} no download link")
    sys.exit(1)

video_id = re.search(r'(?:v=|youtu\.be/)([a-zA-Z0-9_-]{11})', URL)[1]
clean_title = re.sub(r'[^a-zA-Z0-9\-_()\[\]]', '_', title.replace(' ', '_'))
clean_title = re.sub(r'_+', '_', clean_title).strip('_')[:70] or video_id
filename = f"{clean_title}_{video_id}_{QUAL}.{FMT}"
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
if clean_title == video_id:
    folder = f"{video_id}_{timestamp}"
else:
    folder = f"{clean_title}_{video_id}_{timestamp}"
folder = re.sub(r'[^a-zA-Z0-9\-_()\[\]]', '_', folder)

info = {
    "url": URL, "dl_url": dl_url, "filename": filename,
    "title": title, "folder": folder, "index": IDX
}
with open(f"all_videos_info/video_{IDX}.json", "w") as f:
    json.dump(info, f)
