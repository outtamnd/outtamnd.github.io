import os
import re

audio_dir = 'audio'
# Strict format regex: (genre) outtamnd ... - title bpm
pattern = re.compile(r'^\(.*\)\s+outtamnd.*?\s-\s.+?\s\d{2,3}$', re.IGNORECASE)

if not os.path.exists(audio_dir):
    print(f"Error: '{audio_dir}' directory not found in project root.")
    exit()

deleted_count = 0
kept_count = 0

for f in os.listdir(audio_dir):
    ext = os.path.splitext(f)[1].lower()
    if ext in ['.mp3', '.wav', '.m4a', '.flac']:
        filename_without_ext = os.path.splitext(f)[0]
        if pattern.match(filename_without_ext):
            kept_count += 1
        else:
            file_path = os.path.join(audio_dir, f)
            os.remove(file_path)
            print(f"Deleted unformatted file: {f}")
            deleted_count += 1

print(f"\nCleanup complete! Kept {kept_count} formatted files, deleted {deleted_count} unformatted files.")