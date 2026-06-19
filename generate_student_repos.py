#!/usr/bin/env python3
"""
SWD80PS - Generate Unique Student Repositories
================================================
Creates private repos with unique challenge configurations.

Usage:
    python generate_student_repos.py
"""
import os
import shutil
import subprocess
import sys
import csv
import hashlib
import random

GITHUB_USER = "mtjikuzu"
TEMPLATE_REPO = f"{GITHUB_USER}/swd80ps-practical"
NUM_STUDENTS = 14
WORK_DIR = "/tmp/swd80ps-student-repos"
OUTPUT_CSV = "student_access.csv"

STUDENTS = [
    "ANDREAS ANGULA ABNER",
    "JOSEPH NDAKUMA AMAPINDI",
    "JOHANNES NIILENGE DEMETIRIUS",
    "ELIZABETH TSHALONGO EFRAIM",
    "HILJA NDIWENI KAKONGA",
    "ENGELBERTH JOSEPH HAIRWA KANDJEKE",
    "SUAMA NANGOMBE MASHUNA",
    "TOINI POPYENINAWA MUNDANDALA",
    "ROSINA JN NENKONO",
    "SALOMO DHIGININA NTINDA",
    "TULELA NDAKOLA SHIPANGA",
    "ABED-NEGO TUHAFENI SHISHIVENI",
    "BIANCA BENE SIMATAA",
    "CHARLES SIVEREGI",
]


def run(cmd, check=True):
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if check and result.returncode != 0:
        print(f"ERROR: {cmd}\n{result.stderr}")
        sys.exit(1)
    return result.stdout.strip()


def generate_config(student_id, student_name):
    """Generate a static, unique challenge_config.py for a given student."""
    rng = random.Random(student_id)

    admin_user = f"admin_{rng.randint(100, 999)}"
    admin_pass_hash = hashlib.md5(f"admin_pass_{student_id}".encode()).hexdigest()[:16]
    user_user = f"user_{rng.randint(100, 999)}"
    user_pass_hash = hashlib.md5(f"user_pass_{student_id}".encode()).hexdigest()[:16]
    secret_key = hashlib.sha256(f"swd80ps_secret_{student_id}".encode()).hexdigest()[:32]
    session_cookie = f"swd80ps_session_{rng.randint(1000, 9999)}"
    student_extra = f"student_{rng.randint(10, 99)}"
    student_extra_pass = hashlib.md5(b"abc123").hexdigest()[:8]
    temp_user = f"temp_{rng.randint(10, 99)}"
    search_term = rng.choice(["admin", "student", "user", "test"])
    feedback_name = rng.choice(["Alice", "Bob", "Charlie", "Diana"])
    secret_flag = hashlib.md5(f"final_flag_{student_id}".encode()).hexdigest()

    return f'''"""
=================================================================
SWD80PS - Final Practical Assessment - Student ID {student_id}
Student: {student_name}
=================================================================
IMPORTANT: Do NOT share this file. Set STUDENT_ID below.
=================================================================
"""

# CHANGE THIS IF RE-ASSIGNED
STUDENT_ID = {student_id}

# Pre-computed unique credentials (do not share)
ADMIN_USERNAME = "{admin_user}"
ADMIN_PASSWORD_HASH = "{admin_pass_hash}"
USER_USERNAME = "{user_user}"
USER_PASSWORD_HASH = "{user_pass_hash}"
SECRET_KEY = "{secret_key}"
SESSION_COOKIE_NAME = "{session_cookie}"
SESSION_TIMEOUT_MINUTES = 60
UPLOAD_DIR = "uploads"
ALLOWED_EXTENSIONS = {{"png", "jpg", "jpeg", "gif", "pdf"}}

USERS_DB = {{
    "{admin_user}": "{admin_pass_hash}",
    "{user_user}": "{user_pass_hash}",
    "{student_extra}": "{student_extra_pass}",
    "{temp_user}": "password",
}}

EXPECTED_VALUES = {{
    "search_term": "{search_term}",
    "feedback_name": "{feedback_name}",
    "target_user": "{user_user}",
    "secret_flag": "{secret_flag}",
}}

print(f"[CONFIG] Loaded challenge for Student ID {{STUDENT_ID}}: {{ADMIN_USERNAME}}")
'''


def main():
    print("=" * 60)
    print("SWD80PS - Generating Unique Student Repositories")
    print("=" * 60)

    status = run("gh auth status 2>&1", check=False)
    if "Logged in" not in status:
        print("Please run 'gh auth login' first.")
        sys.exit(1)
    print(f"[OK] GitHub authenticated as {GITHUB_USER}")

    template_check = run(f"gh repo view {TEMPLATE_REPO} 2>&1", check=False)
    if "not found" in template_check.lower():
        print(f"\nTemplate repo {TEMPLATE_REPO} not found!")
        print("Push the template first:")
        print(f"  cd /home/mtjikuzu/swd80ps-practical && git remote add origin git@github.com:{TEMPLATE_REPO}.git && git push -u origin main")
        print(f"  gh repo edit {TEMPLATE_REPO} --template")
        sys.exit(1)
    print(f"[OK] Template repo: {TEMPLATE_REPO}")

    if os.path.exists(WORK_DIR):
        shutil.rmtree(WORK_DIR)
    os.makedirs(WORK_DIR)

    rows = []

    for sid in range(1, NUM_STUDENTS + 1):
        student_name = STUDENTS[sid - 1]
        repo_name = f"swd80ps-practical-student-{sid:02d}"
        full_repo = f"{GITHUB_USER}/{repo_name}"

        print(f"\n[{sid}/{NUM_STUDENTS}] {student_name}")

        result = run(f"gh repo create {full_repo} --private --template {TEMPLATE_REPO}", check=False)
        if "already exists" in result.lower():
            print(f"  Repo exists.")
        else:
            print(f"  Created: {full_repo}")

        repo_dir = os.path.join(WORK_DIR, repo_name)
        run(f"git clone git@github.com:{full_repo}.git {repo_dir}")
        print(f"  Cloned")

        config_content = generate_config(sid, student_name)
        with open(os.path.join(repo_dir, "challenge_config.py"), "w") as f:
            f.write(config_content)

        run(f"git -C {repo_dir} add challenge_config.py")
        run(f'git -C {repo_dir} commit -m "Set unique config for student ID {sid}"')
        run(f"git -C {repo_dir} push origin main")
        print(f"  Pushed")

        rows.append({
            "student_id": sid,
            "name": student_name,
            "repo_url": f"https://github.com/{full_repo}",
        })

    csv_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), OUTPUT_CSV)
    with open(csv_path, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["student_id", "name", "repo_url"])
        writer.writeheader()
        writer.writerows(rows)

    print(f"\n{'=' * 60}")
    print(f"Done! {NUM_STUDENTS} unique repos created.")
    print(f"CSV: {csv_path}")
    print(f"\nAdd students as collaborators:")
    print(f"  gh api repos/{GITHUB_USER}/swd80ps-practical-student-01/collaborators/USERNAME -X PUT")
    print(f"{'=' * 60}")


if __name__ == "__main__":
    main()
