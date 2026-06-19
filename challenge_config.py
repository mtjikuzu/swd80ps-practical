"""
=================================================================
SWD80PS - Final Practical Assessment
Per-Student Challenge Configuration
=================================================================
Each student receives a UNIQUE version of this file.

IMPORTANT: Do NOT share your config with anyone. This file
determines which specific values your challenge uses.

HOW TO USE:
1. Open this file
2. Set STUDENT_ID to the ID your lecturer gave you
3. The app will load your unique challenge parameters
4. Fix all vulnerabilities in app.py
5. Run the tests to verify your fixes
=================================================================
"""

# ─── CHANGE THIS TO YOUR ASSIGNED STUDENT ID ───────────────────
# Your lecturer will provide this. Valid range: 1-14
STUDENT_ID = 0  # ← CHANGE THIS
# ────────────────────────────────────────────────────────────────

# DO NOT EDIT ANYTHING BELOW THIS LINE
import hashlib
import random

random.seed(STUDENT_ID)
_rng = random.Random(STUDENT_ID)

# Unique credentials per student
ADMIN_USERNAME = f"admin_{_rng.randint(100, 999)}"
ADMIN_PASSWORD_HASH = hashlib.md5(f"admin_pass_{STUDENT_ID}".encode()).hexdigest()[:16]
USER_USERNAME = f"user_{_rng.randint(100, 999)}"
USER_PASSWORD_HASH = hashlib.md5(f"user_pass_{STUDENT_ID}".encode()).hexdigest()[:16]

# Unique app parameters
SECRET_KEY = hashlib.sha256(f"swd80ps_secret_{STUDENT_ID}".encode()).hexdigest()[:32]
SESSION_COOKIE_NAME = f"swd80ps_session_{_rng.randint(1000, 9999)}"
SESSION_TIMEOUT_MINUTES = 60  # should be 15-30
UPLOAD_DIR = "uploads"
ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "gif", "pdf"}

# Simulated user database (plaintext passwords - VULNERABILITY 3)
USERS_DB = {
    ADMIN_USERNAME: ADMIN_PASSWORD_HASH,
    USER_USERNAME: USER_PASSWORD_HASH,
    f"student_{_rng.randint(10, 99)}": hashlib.md5(b"abc123").hexdigest()[:8],
    f"temp_{_rng.randint(10, 99)}": "password",
}

# Test expectations
EXPECTED_VALUES = {
    "search_term": _rng.choice(["admin", "student", "user", "test"]),
    "feedback_name": _rng.choice(["Alice", "Bob", "Charlie", "Diana"]),
    "target_user": USER_USERNAME,
    "secret_flag": hashlib.md5(f"final_flag_{STUDENT_ID}".encode()).hexdigest(),
}

print(f"[CONFIG] Loaded challenge for Student ID {STUDENT_ID}")
print(f"[CONFIG] Keep this file private!")
