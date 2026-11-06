import os, subprocess
for d in os.listdir("audio"):
    p = os.path.join("audio", d)
    if os.path.isdir(p):
        print("Pushing folder:", d)
        subprocess.run(["git", "add", p])
        subprocess.run(["git", "commit", "-m", f"Add audio folder {d}"])
        subprocess.run(["git", "push", "origin", "main"])
