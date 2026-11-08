import json
import re

# Load beats.json
with open('beats.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# Strict regex matching: (genre) outtamnd ... - title bpm
pattern = re.compile(r'^\(.*\)\s+outtamnd.*?\s-\s.+?\s\d{2,3}$', re.IGNORECASE)

valid = []
for b in data:
    raw = b.get('title', '')
    if pattern.match(raw):
        # Extract BPM from the end
        bpm_match = re.search(r'\b(\d{2,3})\s*$', raw)
        bpm = bpm_match.group(1) if bpm_match else '140'
        
        # Extract genre from parentheses
        genre_match = re.match(r'^\((.*?)\)', raw)
        genre = genre_match.group(1) if genre_match else 'Trap'
        
        # Clean up title: remove genre tag, BPM, producer prefix, and hyphen
        t = re.sub(r'^\(.*?\)\s*', '', raw)
        t = re.sub(r'\b\d{2,3}\s*$', '', t).strip()
        if ' - ' in t:
            t = t.split(' - ')[-1].strip()
        t = re.sub(r'^outtamnd\s+', '', t, flags=re.IGNORECASE).strip()
        
        if t:
            b['title'] = t
            b['bpm'] = bpm
            b['genre'] = genre
            valid.append(b)

# Save back to beats.json
with open('beats.json', 'w', encoding='utf-8') as f:
    json.dump(valid, f, indent=2)

print(f"Success! Kept {len(valid)} strictly formatted beats, purged all unformatted entries.")