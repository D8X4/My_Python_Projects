import json
import subprocess
import os
import sys

# put files with song names in INPUT_FILE
INPUT_FILE = "music.txt"
OUTPUT_DIR = "music"
FAILED_FILE = "failed.txt"

def download_song(title, artist, index, total):
    query = f"{artist} {title} audio"
    print(f"\n[{index}/{total}] Downloading: {title} — {artist}")
    print(f"    Searching: ytsearch:{query}")

    cmd = [
        "yt-dlp",
        f"ytsearch1:{query}",
        "-x",
        "--audio-format", "mp3",
        "--audio-quality", "0",
        "--embed-thumbnail",
        "--embed-metadata",
        "--cookies-from-browser", "firefox",
        # Use Deno to solve the signature challenges
        "--js-runtime", "deno",
        # Fetch the latest solvers from GitHub automatically
        "--remote-components", "ejs:github",
        "--user-agent", "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:124.0) Gecko/20100101 Firefox/124.0",
        "--parse-metadata", f":{title}:%(title)s",
        "-o", f"{OUTPUT_DIR}/%(artist)s - %(title)s.%(ext)s",
        "--no-playlist",
        "--quiet",
        "--progress"
    ]

    result = subprocess.run(cmd)

    if result.returncode == 0:
        print(f"    [+] Done!")
        return True
    else:
        print(f"    [!] Failed: {title} — {artist}")
        return False

def main():
    # Load songs
    if not os.path.exists(INPUT_FILE):
        print(f"[!] {INPUT_FILE} not found — run scraper.py first")
        sys.exit(1)

    with open(INPUT_FILE) as f:
        songs = json.load(f)

    total = len(songs)
    print(f"[*] Loaded {total} songs from {INPUT_FILE}")
    print(f"[*] Saving to ./{OUTPUT_DIR}/\n")

    # Make output dir
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    failed = []

    for i, song in enumerate(songs, start=1):
        title = song.get("title", "").strip()
        artist = song.get("artist", "").strip()

        if not title:
            continue

        success = download_song(title, artist, i, total)
        if not success:
            failed.append(f"{artist} - {title}")

    # Summary
    print(f"\n{'='*40}")
    print(f"[+] Finished! {total - len(failed)}/{total} songs downloaded")
    print(f"[*] Files saved to ./{OUTPUT_DIR}/")

    if failed:
        print(f"\n[!] {len(failed)} songs failed:")
        for f in failed:
            print(f"    - {f}")
        with open(FAILED_FILE, "w") as fh:
            fh.write("\n".join(failed))
        print(f"[*] Failed list saved to {FAILED_FILE}")

main()
