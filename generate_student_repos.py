#!/usr/bin/env python3
"""
Generate unique student repos from the template.

Usage: python generate_student_repos.py
Requires: gh CLI authenticated
"""
import os, shutil, subprocess, csv, hashlib, random

GH_USER = "mtjikuzu"
TEMPLATE = f"{GH_USER}/swd80ps-practical"
NUM = 14
WORK_DIR = "/tmp/swd80ps-student-repos"
OUTPUT = "student_access.csv"

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
        raise RuntimeError(f"CMD: {cmd[:60]} ERR: {r.stderr[:200]}")
    return r.stdout.strip()

def make_cfg(sid, name):
    rng = random.Random(sid)
    au = "admin_" + str(rng.randint(100, 999))
    aph = hashlib.md5(("apw_" + str(sid)).encode()).hexdigest()[:16]
    uu = "user_" + str(rng.randint(100, 999))
    uph = hashlib.md5(("upw_" + str(sid)).encode()).hexdigest()[:16]
    sk = hashlib.sha256(("sk_" + str(sid)).encode()).hexdigest()[:32]
    sc = "sess_" + str(rng.randint(1000, 9999))
    se = "stu_" + str(rng.randint(10, 99))
    sep = hashlib.md5(b"x").hexdigest()[:8]
    tu = "tmp_" + str(rng.randint(10, 99))
    st = rng.choice(["admin", "student", "user", "test"])
    fb = rng.choice(["Alice", "Bob", "Charlie", "Diana"])
    sf = hashlib.md5(("flag_" + str(sid)).encode()).hexdigest()
    return "\n".join([
        "# SWD80PS Student " + str(sid) + ": " + name,
        "# Keep private.",
        "",
        "STUDENT_ID = " + str(sid),
        "",
        'AU = "' + au + '"',
        'AP = "' + aph + '"',
        'NU = "' + uu + '"',
        'NP = "' + uph + '"',
        'SK = "' + sk + '"',
        'CN = "' + sc + '"',
        'TO = 60',
        'UD = "uploads"',
        'AL = {"png", "jpg", "jpeg", "gif", "pdf"}',
        "",
        "DB = {",
        '    "' + au + '": "' + aph + '",',
        '    "' + uu + '": "' + uph + '",',
        '    "' + se + '": "' + sep + '",',
        '    "' + tu + '": "password",',
        "}",
        "",
        "EX = {",
        '    "q": "' + st + '",',
        '    "fb": "' + fb + '",',
        '    "u": "' + uu + '",',
        '    "f": "' + sf + '",',
        "}",
        "",
        'print("[OK] ID", STUDENT_ID)',
    ])

def main():
    tok = subprocess.run("gh auth token", shell=True, capture_output=True, text=True).stdout.strip()
    if not tok:
        print("No gh token")
        return
    rm = "https://" + GH_USER + ":" + tok + "@github.com"

    if os.path.exists(WORK_DIR):
        shutil.rmtree(WORK_DIR)
    os.makedirs(WORK_DIR, exist_ok=True)

    r = subprocess.run("gh repo list " + GH_USER + " --visibility private --limit 50 --json name -q '.[].name'", shell=True, capture_output=True, text=True)
    existing = set(l.strip() for l in r.stdout.strip().split("\n") if l.strip())

    rows = []
    for sid in range(1, NUM + 1):
        name = STUDENTS[sid - 1]
        rn = "swd80ps-practical-student-" + str(sid).zfill(2)
        fr = GH_USER + "/" + rn
        rd = os.path.join(WORK_DIR, rn)
        print("[" + str(sid) + "/" + str(NUM) + "] " + name, flush=True)

        if rn not in existing:
            rc("gh repo create " + fr + " --private --template " + TEMPLATE)
            print("  Created", flush=True)
        else:
            print("  Exists", flush=True)

        if os.path.exists(rd):
            shutil.rmtree(rd)
        rc("git clone " + rm + "/" + fr + ".git " + rd)
        print("  Cloned", flush=True)

        with open(os.path.join(rd, "challenge_config.py"), "w") as f:
            f.write(make_cfg(sid, name))

        diff = subprocess.run("git -C " + rd + " diff --name-only", shell=True, capture_output=True, text=True)
        if diff.stdout.strip():
            rc("git -C " + rd + " add challenge_config.py")
            rc('git -C ' + rd + ' commit -m "Config for student ' + str(sid) + '"')
            rc("git -C " + rd + " push origin main")
            print("  Pushed", flush=True)
        else:
            print("  OK", flush=True)

        rows.append({"id": sid, "name": name, "url": "https://github.com/" + fr})

    with open(OUTPUT, "w", newline="") as f:
        csv.DictWriter(f, fieldnames=["id", "name", "url"]).writeheader()
        csv.DictWriter(f, fieldnames=["id", "name", "url"]).writerows(rows)
    print("\nDone. CSV: " + OUTPUT)

if __name__ == "__main__":
    main()
