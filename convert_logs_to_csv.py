import pandas as pd
import os

# Read valid links
with open('logs/valid_links.txt', 'r') as f:
    valid_links = [line.strip() for line in f.readlines()]

# Read dead links
with open('logs/dead_links.txt', 'r') as f:
    dead_links = [line.strip() for line in f.readlines()]

# Create DataFrames
valid_df = pd.DataFrame({
    'url': valid_links,
    'status': 'valid',
    'video_id': [url.split('v=')[1] for url in valid_links]
})

dead_df = pd.DataFrame({
    'url': dead_links,
    'status': 'dead',
    'video_id': [url.split('v=')[1] for url in dead_links]
})

# Combine and save
all_links_df = pd.concat([valid_df, dead_df], ignore_index=True)
all_links_df.to_csv('logs/download_results.csv', index=False)

print(f"Converted {len(valid_links)} valid and {len(dead_links)} dead links to CSV")
print("Saved as: logs/download_results.csv")
