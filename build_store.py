import difflib
import json
import os
import re

print("Running 100% Coverage Fuzzy BPM Matcher...")

if os.path.exists("beats.json"):
  with open("beats.json", "r", encoding="utf-8") as f:
    beats = json.load(f)
else:
  print("Error: beats.json not found!")
  exit()

local_beats_path = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "beats")
)
local_files_bpms = []

if os.path.exists(local_beats_path):
  print(f"Reading local files from: {local_beats_path}")
  for filename in os.listdir(local_beats_path):
    if filename.lower().endswith((".mp3", ".wav", ".zip", ".m4a", ".flac")):
      match = re.search(
          r'(\d{2,3})\s*\.(?:mp3|wav|zip|m4a|flac)$', filename, re.IGNORECASE
      )
      if not match:
        match = re.search(r'(\d{2,3})', filename)

      if match:
        bpm = match.group(1)
        clean_fn = re.sub(r'\(.*?\)', '', filename.lower())
        clean_fn = re.sub(r'[^a-z0-9]', '', clean_fn)
        local_files_bpms.append((clean_fn, bpm))
else:
  print("WARNING: Local beats folder not found!")

matched_count = 0
clean_filenames = [item[0] for item in local_files_bpms]

for beat in beats:
  raw_title = beat.get("title", "").lower()
  beat_clean = re.sub(r'[^a-z0-9]', '', raw_title)

  found_bpm = "140"

  if clean_filenames:
    matches = difflib.get_close_matches(
        beat_clean, clean_filenames, n=1, cutoff=0.05
    )
    if matches:
      best_match = matches[0]
      for cf, bpm in local_files_bpms:
        if cf == best_match:
          found_bpm = bpm
          matched_count += 1
          break

  beat["bpm"] = found_bpm

with open("beats.json", "w", encoding="utf-8") as f:
  json.dump(beats, f, indent=2)

print(
    f"--- DONE: Assigned BPMs to all {len(beats)} tracks ({matched_count}"
    f" matched)! ---"
)