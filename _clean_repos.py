import subprocess, sys

GITHUB_USER = "mtjikuzu"

for i in range(1, 15):
    repo = f"swd80ps-practical-student-{i:02d}"
    full = f"{GITHUB_USER}/{repo}"
    r = subprocess.run(
        f"gh repo delete {full} --yes",
        shell=True, capture_output=True, text=True
    )
    print(f"{full}: {'deleted' if r.returncode == 0 else 'not found or error'}")

print("Done cleaning up repos")
