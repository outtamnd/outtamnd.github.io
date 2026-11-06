
import os, subprocess
files = sorted([os.path.join('audio', f) for f in os.listdir('audio') if f.endswith('.mp3')])
chunk_size = 10
for i in range(0, len(files), chunk_size):
    chunk = files[i:i+chunk_size]
    print(f'Pushing micro-chunk {i//chunk_size + 1}...')
    subprocess.run(['git', 'add'] + chunk)
    subprocess.run(['git', 'commit', '-m', f'Add audio micro-chunk {i//chunk_size + 1}'])
    subprocess.run(['git', 'push', 'origin', 'main'])
