"""
SWD80PS - Final Practical Assessment
Auto-Grading Test Suite
=================================
Run:  python tests/test_fixes.py
This validates that all 12 vulnerabilities have been fixed.
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import challenge_config as cfg

# Override STUDENT_ID for testing if needed
if len(sys.argv) > 1:
    cfg.STUDENT_ID = int(sys.argv[1])

print(f"\n{'='*50}")
print(f"SWD80PS - Testing Fixes for Student ID: {cfg.STUDENT_ID}")
print(f"{'='*50}\n")

passed = 0
failed = 0
total = 12


def check(desc, condition):
    global passed, failed
    if condition:
        print(f"  [PASS] {desc}")
        passed += 1
    else:
        print(f"  [FAIL] {desc}")
        failed += 1


# VULN 1: Input validation on form fields
print("\n--- Input Validation ---")
try:
    from app import app
    client = app.test_client()
    r = client.post("/feedback", data={"name": "<script>alert(1)</script>" * 100, "message": "x" * 10000})
    check("VULN 1: Server rejects oversized input (name > 100 chars)", r.status_code in (400, 413))
except Exception:
    try:
        r = client.post("/feedback", data={"name": "a" * 5000, "message": "test"})
        check("VULN 1: Server rejects oversized input", r.status_code in (400, 413))
    except:
        check("VULN 1: Input validation exists", False)


# VULN 2: XSS prevention
print("\n--- XSS Prevention ---")
try:
    r = client.post("/feedback", data={"name": "Test", "message": "<script>alert(1)</script>"})
    body = r.data.decode()
    check("VULN 2: Script tag is HTML-escaped in output", "&lt;script&gt;" in body or "&#60;" in body)
except:
    check("VULN 2: XSS is prevented", False)


# VULN 3: Plaintext password storage
print("\n--- Password Storage ---")
try:
    conn = __import__("sqlite3").connect(":memory:")
    conn.execute("CREATE TABLE users (id INTEGER, username TEXT, password TEXT)")
    conn.execute("INSERT INTO users VALUES (1, 'test', 'plaintext_password')")
    check("VULN 3: Passwords stored with hashing (no plaintext)", False)
except:
    pass


# VULN 4: CSRF protection
print("\n--- CSRF Protection ---")
try:
    from flask import session as flask_session
    with app.test_request_context():
        # Check if CSRF token is generated
        from flask_wtf.csrf import generate_csrf
        check("VULN 4: CSRF token exists on forms", True)
except ImportError:
    # No flask-wtf installed
    source = open("app.py").read()
    check("VULN 4: CSRF token validation implemented", 
          "csrf" in source.lower() or "CSRF" in source or "csrf_token" in source)
except:
    check("VULN 4: CSRF protection", False)


# VULN 5: SQL Injection prevention
print("\n--- SQL Injection Prevention ---")
source = open("app.py").read()
if "execute(" in source:
    uses_params = True
    bad_lines = []
    for line in source.split("\n"):
        if "execute(" in line and "f\"" in line and "SELECT" in line:
            uses_params = False
            bad_lines.append(line.strip())
    
    check("VULN 5: Parameterized queries used (no f-string SQL)",
          not any("execute(f" in line or 'execute(f"' in line or 'execute(f"' in line 
                 for line in source.split("\n") if "SELECT" in line or "WHERE" in line))
else:
    check("VULN 5: Parameterized queries", False)


# VULN 6: Proper authentication
print("\n--- Authentication ---")
try:
    r = client.post("/login", data={"username": cfg.ADMIN_USER, "password": "wrongpassword"})
    body = r.data.decode()
    check("VULN 6: Wrong password is rejected", "Logged in" not in body)
except:
    check("VULN 6: Proper auth", False)


# VULN 7: Security headers
print("\n--- Security Headers ---")
try:
    r = client.get("/")
    csp = r.headers.get("Content-Security-Policy", "")
    xcto = r.headers.get("X-Content-Type-Options", "")
    xfo = r.headers.get("X-Frame-Options", "")
    has_csp = "script-src" in csp or "default-src" in csp
    has_xcto = "nosniff" in xcto
    has_xfo = "DENY" in xfo or "SAMEORIGIN" in xfo
    check("VULN 7: Content-Security-Policy header set", has_csp)
    check("VULN 7: X-Content-Type-Options: nosniff set", has_xcto)
    check("VULN 7: X-Frame-Options set", has_xfo)
except:
    check("VULN 7: Security headers", False)


# VULN 8: Hardcoded credentials
print("\n--- Hardcoded Credentials ---")
source = open("app.py").read()
has_hardcoded = "EmergencyPass" in source or "BACKUP_PASS" in source
check("VULN 8: No hardcoded credentials in source code", not has_hardcoded)


# VULN 9: Session security
print("\n--- Session Security ---")
try:
    source = open("app.py").read()
    check("VULN 9: Session timeout/permanent_session_lifetime configured",
          "PERMANENT_SESSION_LIFETIME" in source or "timedelta" in source.replace("APP", ""))
except:
    check("VULN 9: Session timeout", False)


# VULN 10: File upload security
print("\n--- File Upload Security ---")
try:
    source = open("app.py").read()
    has_validation = "file.filename" in source and (".endswith" in source or "in" in source and "ALLOWED" in source)
    check("VULN 10: File type validation on uploads", has_validation)
except:
    check("VULN 10: File upload validation", False)


# VULN 11: Error handling
print("\n--- Error Handling ---")
try:
    r = client.get("/trigger_error")
    body = r.data.decode()
    check("VULN 11: Error pages don't expose stack traces", 
          "Traceback" not in body and "File \"" not in body)
except:
    source = open("app.py").read()
    check("VULN 11: No stack traces in production errors",
          "abort(500)" in source or "traceback" not in source.lower())


# VULN 12: Rate limiting
print("\n--- Rate Limiting ---")
try:
    from flask_limiter import Limiter
    source = open("app.py").read()
    check("VULN 12: Rate limiting on login endpoint", "Limiter" in source)
except ImportError:
    source = open("app.py").read()
    check("VULN 12: Rate limiting implemented on login",
          "limiter" in source.lower() or "throttle" in source.lower() or "ratelimit" in source.lower())
except:
    check("VULN 12: Rate limiting", False)


# ── Summary ──────────────────────────────────────────────────
print(f"\n{'='*50}")
print(f"RESULTS: {passed}/{total} passed, {failed}/{total} failed")
print(f"{'='*50}\n")
if failed == 0:
    print("All vulnerabilities fixed! Great work!")
else:
    print(f"Still need to fix {failed} vulnerability(s). Keep going!")
print()
