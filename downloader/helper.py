# script untuk membantu mendapatkan file audio dari songs_list. Dataset tidak menyediakan file audio secara langsung dikarenakan hak cipta. Sehingga harus dilakukan crawling secara manual.

import os
import glob
import subprocess 
from multiprocessing import Pool, cpu_count


# config
URL_FILE = "clean_links.txt"
AUDIO_OUTPUT_DIR = "audio_raw"

os.makedirs(AUDIO_OUTPUT_DIR, exist_ok=True)


def download_audio(url):
    id_video = url.split("v=")[-1]
    
    output_path = f"{AUDIO_OUTPUT_DIR}/{id_video}.wav"
    
    if os.path.exists(output_path):
        print(f"[SKIPPED] {id_video}.wav has existed ")
        return 
    
    print(f"[Downloading...] {url}") 
    
    cmd = [
        "yt-dlp",
        "-f", "bestaudio",
        "--extract-audio",
        "--audio-format", "wav",
        "-o", f"{AUDIO_OUTPUT_DIR}/%(id)s.%(ext)s",
        url
    ] 
    
    # error handling
    try:
        subprocess.run(cmd, check=True)
    except Exception as e:
        print(f"[ERROR] Fail to download: {url}")


def load_urls():
    print("=== Reading cleaned URL file ===")

    if not os.path.exists(URL_FILE):
        print(f"[ERROR] {URL_FILE} file doesn't exist")
        return []

    with open(URL_FILE, "r") as f:
        urls = [line.strip() for line in f if line.strip()]

    print(f"Total URLs Loaded: {len(urls)}")
    return urls

def download_all(urls):
    print("Start downloading raw audio")

    workers = max(cpu_count() - 1, 1)
    print(f"Workers: {workers}")

    with Pool(workers) as p:
        p.map(download_audio, urls)

    print("Download finished.")
    
    