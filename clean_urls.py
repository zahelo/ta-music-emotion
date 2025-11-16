## Cleaning songs list from the dataset (remove space, remove comma and period, only accept http address)

import os
import glob

SONG_LIST_DIR = "datasets/songs_lists"

OUTPUT_CLEAN = "clean_links.txt"
OUTPUT_INVALID = "invalid_lines.txt"
OUTPUT_DUPLICATES = "duplicate_links.txt"

def clean_line(line):
    """
    Membersihkan 1 baris teks:
    - buang spasi
    - hapus koma+angka
    - hanya menerima http*
    """
    original = line.strip()

    if not original:
        return None, original

    # kalau mengandung koma ambil sebelum koma
    if "," in original:
        original_before_clean = original
        cleaned = original.split(",")[0]
    else:
        cleaned = original

    # validasi simple
    if not cleaned.startswith("http"):
        return None, original

    return cleaned, None  # None berarti valid

def read_all_urls():
    txt_files = sorted(glob.glob(f"{SONG_LIST_DIR}/*.txt"))
    all_lines = []

    for txt in txt_files:
        with open(txt, "r") as f:
            all_lines.extend([line.rstrip("\n") for line in f])

    return all_lines

def save_list(path, data):
    with open(path, "w") as f:
        for item in data:
            f.write(item + "\n")

def clean_urls():
    all_lines = read_all_urls()

    raw_count = len(all_lines)
    print(f"Raw total lines = {raw_count}")

    valid_urls = []
    invalid_lines = []

    for line in all_lines:
        cleaned, invalid = clean_line(line)
        if cleaned:
            valid_urls.append(cleaned)
        else:
            invalid_lines.append(invalid)

    # ambil duplikat
    seen = set()
    duplicates = []

    for url in valid_urls:
        if url in seen:
            duplicates.append(url)
        else:
            seen.add(url)

    # URL unik
    unique_urls = list(seen)

    print(f"Cleaned valid URLs = {len(valid_urls)}")
    print(f"Unique URLs after removing duplicates = {len(unique_urls)}")
    print(f"Invalid lines = {len(invalid_lines)}")
    print(f"Duplicate URLs = {len(duplicates)}")

    save_list(OUTPUT_CLEAN, unique_urls)
    save_list(OUTPUT_INVALID, [i for i in invalid_lines if i])
    save_list(OUTPUT_DUPLICATES, duplicates)

    return invalid_lines, duplicates, unique_urls

if __name__ == "__main__":
    invalid, dups, cleaned = clean_urls()

    print("\nINVALID LINES: ")
    for i in invalid:
        print(i)
