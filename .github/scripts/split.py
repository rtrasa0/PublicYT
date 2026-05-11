import json, os, subprocess
idx = int(os.environ['CURRENT_INDEX'])
thresh_mb = int(os.environ['MAX_PART_MB'])
if thresh_mb <= 0 or thresh_mb > 1900:
    thresh_mb = 1800
with open(f"all_videos_info/video_{idx}.json", "r") as f:
    info = json.load(f)
folder = info['folder']
filename = info['filename']
filepath = f"release_files/{folder}/{filename}"
size_bytes = os.path.getsize(filepath)
thresh_bytes = thresh_mb * 1024 * 1024
if size_bytes > thresh_bytes:
    os.chdir(f"release_files/{folder}")
    base = os.path.splitext(filename)[0]
    subprocess.run(["zip", "-r", "-s", f"{thresh_mb}m", f"{base}.zip", filename], check=True)
    os.remove(filename)
    print(f"Split {filename} into parts")
else:
    print(f"No split needed for {filename}")
