from downloader.helper import load_urls, download_all
from downloader.checker import check_all_urls


if __name__ == "__main__":
    print("Loading URLs...")
    urls = load_urls()

    print("Checking YouTube links...")
    alive_urls, dead_urls = check_all_urls(urls)

    print("\nDownloading only valid URLs...\n")
    download_all(alive_urls)
    
    print("All raw audio has been downloaded!\nFiles saved in: audio_raw/")
    