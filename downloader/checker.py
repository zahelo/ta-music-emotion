import os
import subprocess

LOG_DIR = "logs"
os.makedirs(LOG_DIR, exist_ok=True)

def is_youtube_link_alive(url):
    """Return True jika link bisa diakses, False jika mati"""
    try:
        cmd = [
            "yt-dlp",
            "--skip-download",
            "--quiet",
            url
        ]
        result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return result.returncode == 0
    except Exception:
        return False
    
def check_all_urls(urls):
    alive = []
    dead = []

    print("=== Checking YouTube links ===")
  
    for url in urls:
        if is_youtube_link_alive(url):
            print(f"[OK]   {url}")
            alive.append(url)
        else:
            print(f"[DEAD] {url}")
            dead.append(url)

    save_logs(alive, dead)
    show_summary(alive, dead)

    return alive, dead

def save_logs(valid, dead):
    valid_path = os.path.join(LOG_DIR, "valid_links.txt")
    dead_path = os.path.join(LOG_DIR, "dead_links.txt")

    with open(valid_path, "w") as f:
        for url in valid:
            f.write(url + "\n")

    with open(dead_path, "w") as f:
        for url in dead:
            f.write(url + "\n")

    print(f"\nSaved valid links to   : {valid_path}")
    print(f"Saved dead links to    : {dead_path}")

def show_summary(alive, dead):
    print("\n=== SUMMARY ===")
    print(f"Valid links   : {len(alive)}")
    print(f"Dead links    : {len(dead)}")
    print(f"Logs saved in  : {LOG_DIR}/")
