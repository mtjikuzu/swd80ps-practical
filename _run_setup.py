#!/usr/bin/env python3
"""Create all 14 student repos with unique configs."""
import os, shutil, subprocess, csv, hashlib, random

GH_USER = "mtjikuzu"
TEMPLATE = f"{GH_USER}/swd80ps-practical"
NUM = 14
WORK = "/tmp/swd80ps-student-repos"
OUT = "student_access.csv"

STUDENTS = [
    "ANDREAS ANGULA ABNER", "JOSEPH NDAKUMA AMAPINDI",
    "JOHANNES NIILENGE DEMETIRIUS", "ELIZABETH TSHALONGO EFRAIM",
    "HILJA NDIWENI KAKONGA", "ENGELBERTH JOSEPH HAIRWA KANDJEKE",
    "SUAMA NANGOMBE MASHUNA", "TOINI POPYENINAWA MUNDANDALA",
    "ROSINA JN NENKONO", "SALOMO DHIGININA NTINDA",
    "TULELA NDAKOLA SHIPANGA", "ABED-NEGO TUHAFENI SHISHIVENI",
    "BIANCA BENE SIMATAA", "CHARLES SIVEREGI",
]

def rc(cmd):
    r = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=60)
    if r.returncode != 0:
        raise RuntimeError(f"CMD: {cmd[:60]}... ERR: {r.stderr[:200]}")
    return r.stdout.strip()

def gen(sid, name):
    rng = random.Random(sid)
    au = f"admin_{rng.randint(100, 999)}"
    aph = hashlib.md5(f"admin_pass_{sid}".encode()).hexdigest()[:16]
    uu = f"user_{rng.randint(100, 999)}"
    uph = hashlib.md5(f"user_pass_{sid}".encode()).hexdigest()[:16]
    sk = hashlib.sha256(f"swd80ps_secret_{sid}".encode()).hexdigest()[:32]
    sc = f"swd80ps_session_{rng.randint(1000, 9999)}"
    se = f"student_{rng.randint(10, 99)}"
    sep = hashlib.md5(b"abc123").hexdigest()[:8]
    tu = f"temp_{rng.randint(10, 99)}"
    st = rng.choice(["admin", "student", "user", "test"])
    fb = rng.choice(["Alice", "Bob", "Charlie", "Diana"])
    sf = hashlib.md5(f"final_flag_{sid}".encode()).hexdigest()

    lines = [
        "# SWD80PS Student ID " + str(sid) + ": " + name,
        "# Do NOT share this file.",
        "",
        "STUDENT_ID = " + str(sid),
        "",
        'ADMIN_USER = "' + au + '"',
        'ADMIN_PW = "' + aph + '"',
        'NORMAL_USER = "' + uu + '"',
        'NORMAL_PW = "' + uph + '"',
        'APP_SECRET = "' + sk + '"',
        'COOKIE_NAME = "' + sc + '"',
        'TIMEOUT = 60',
        'UPLOADS = "uploads"',
        'ALLOWED = {"png", "jpg", "jpeg", "gif", "pdf"}',
        "",
        "USERS = {",
        '    "' + au + '": "' + aph + '",',
        '    "' + uu + '": "' + uph + '",',
        '    "' + se + '": "' + sep + '",',
        '    "' + tu + '": "password",',
        "}",
        "",
        "EXPECTED = {",
        '    "q": "' + st + '",',
        '    "fb_name": "' + fb + '",',
        '    "user": "' + uu + '",',
        '    "flag": "' + sf + '",',
        "}",
        "",
        'print("[OK] Student ID", STUDENT_ID)',
    ]
    return "\n".join(lines)

def main():
    token = subprocess.run("gh auth token", shell=True, capture_output=True, text=True).stdout.strip()
    if not token:
        print("No gh token found")
        return
    remote = "https://" + GH_USER + ":" + token + "@github.com"

    if os.path.exists(WORK):
        shutil.rmtree(WORK)
    os.makedirs(WORK, exist_ok=True)

    r = subprocess.run(
        "gh repo list " + GH_USER + " --visibility private --limit 50 --json name -q '.[].name'",
        shell=True, capture_output=True, text=True
    )
    existing = set(line.strip() for line in r.stdout.strip().split("\n") if line.strip())

    rows = []
    for sid in range(1, NUM + 1):
        name = STUDENTS[sid - 1]
        rn = "swd80ps-practical-student-" + str(sid).zfill(2)
        fr = GH_USER + "/" + rn
        rd = os.path.join(WORK, rn)

        print("[" + str(sid) + "/" + str(NUM) + "] " + name, flush=True)

        if rn not in existing:
            rc("gh repo create " + fr + " --private --template " + TEMPLATE)
            print("  Created", flush=True)
        else:
            print("  Exists", flush=True)

        if os.path.exists(rd):
            shutil.rmtree(rd)
        rc("git clone " + remote + "/" + fr + ".git " + rd)
        print("  Cloned", flush=True)

        cfg = gen(sid, name)
        with open(os.path.join(rd, "challenge_config.py"), "w") as f:
            f.write(cfg)

        status = subprocess.run("git -C " + rd + " diff --name-only", shell=True, capture_output=True, text=True)
        if status.stdout.strip():
            rc("git -C " + rd + " add challenge_config.py")
            rc('git -C ' + rd + ' commit -m "Set unique config for student ID ' + str(sid) + '"')
            rc("git -C " + rd + " push origin main")
            print("  Pushed", flush=True)
        else:
            print("  Up-to-date", flush=True)

        rows.append({"student_id": sid, "name": name, "repo_url": "https://github.com/" + fr})

    with open(OUT, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=["student_id", "name", "repo_url"])
        w.writeheader()
        w.writerows(rows)

    print("\n=== DONE! " + str(NUM) + " repos ===")
    print("CSV: " + OUT)

if __name__ == "__main__":
    main()
