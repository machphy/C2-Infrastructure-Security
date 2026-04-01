import os
import time

# file jisme changes karne hain
file_name = "new.txt"

for i in range(1, 110):
    # file me change add karo
    with open(file_name, "a") as f:
        f.write(f"Commit number {i}\n")

    # git add + commit
    os.system("git add .")
    os.system(f'git commit -m "Auto commit {i}"')

    print(f"Commit {i} done")

    time.sleep(1)  # optional delay