"""
SWD80PS - Final Practical Assessment: Vulnerable Flask App
==========================================================
This app contains 12 deliberate security vulnerabilities.
Your task: Find and fix ALL of them.

Run with:  python app.py
Then open: http://127.0.0.1:5000
"""
from flask import Flask, request, render_template_string, redirect, url_for, session, jsonify
import os
import sqlite3
import hashlib
from datetime import datetime

import challenge_config as cfg

app = Flask(__name__)
app.secret_key = cfg.SECRET_KEY
app.config["SESSION_COOKIE_NAME"] = cfg.SESSION_COOKIE_NAME
app.config["UPLOAD_FOLDER"] = cfg.UPLOAD_DIR

os.makedirs(cfg.UPLOAD_DIR, exist_ok=True)

# ── Simulated Database ─────────────────────────────────────
def get_db():
    conn = sqlite3.connect(":memory:")
    conn.execute("CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, username TEXT, password TEXT)")
    conn.execute("CREATE TABLE IF NOT EXISTS marks (id INTEGER PRIMARY KEY, student TEXT, subject TEXT, mark INTEGER)")
    for uname, pwd in cfg.USERS_DB.items():
        conn.execute("INSERT INTO users (username, password) VALUES (?, ?)", (uname, pwd))
    conn.execute("INSERT INTO marks (student, subject, mark) VALUES (?, ?, ?)", ("Alice", "SWD80PS", 85))
    conn.execute("INSERT INTO marks (student, subject, mark) VALUES (?, ?, ?)", ("Bob", "SWD80PS", 72))
    conn.execute("INSERT INTO marks (student, subject, mark) VALUES (?, ?, ?)", ("Charlie", "SWD80PS", 91))
    conn.commit()
    return conn


# ── Routes ─────────────────────────────────────────────────

@app.route("/")
def index():
    return render_template_string(INDEX_HTML)


# VULN 1: No input validation on form fields
# VULN 2: XSS - Direct DOM output via innerHTML
@app.route("/feedback", methods=["GET", "POST"])
def feedback():
    result = ""
    if request.method == "POST":
        name = request.form.get("name", "")
        message = request.form.get("message", "")
        # VULN 1: No validation on name or message fields
        # VULN 2: Unsanitized user input rendered as HTML
        result = f"Feedback from {name}: {message}"
    html = FEEDBACK_HTML.replace("{result}", result)
    return render_template_string(html)


# VULN 5: SQL Injection in search
# VULN 11: Error messages expose stack traces
@app.route("/search", methods=["GET", "POST"])
def search():
    results = []
    query = ""
    if request.method == "POST":
        query = request.form.get("q", "")
        conn = get_db()
        # VULN 5: String interpolation - SQL Injection vulnerability
        sql = f"SELECT * FROM users WHERE username LIKE '%{query}%'"
        try:
            results = conn.execute(sql).fetchall()
        except Exception as e:
            # VULN 11: Full stack trace exposed to user
            results = [("ERROR", str(e), "")]
        conn.close()

    rows_html = ""
    for row in results:
        rows_html += f"<tr><td>{row[0]}</td><td>{row[1]}</td><td>{row[2]}</td></tr>"
    html = SEARCH_HTML.replace("{query}", query).replace("{rows}", rows_html)
    return render_template_string(html)


# VULN 3: Plaintext password storage
# VULN 6: Weak auth - no real password check
# VULN 11: User enumeration in error message
# VULN 12: Missing rate limiting
@app.route("/login", methods=["GET", "POST"])
def login():
    message = ""
    if request.method == "POST":
        username = request.form.get("username", "")
        password = request.form.get("password", "")

        conn = get_db()
        # VULN 5: SQL Injection also here
        row = conn.execute(
            f"SELECT * FROM users WHERE username = '{username}'"
        ).fetchone()
        conn.close()

        if row:
            # VULN 6: Accepts any password if user exists!
            session["user"] = username
            session["role"] = "user"
            message = f"Logged in as {username}"
        else:
            # VULN 11: User enumeration - tells attacker if user exists
            message = "User not found"
        # VULN 12: No rate limiting - unlimited login attempts

    html = LOGIN_HTML.replace("{message}", message)
    return render_template_string(html)


# VULN 9: No session timeout / insecure session
@app.route("/profile")
def profile():
    if "user" not in session:
        return redirect(url_for("login"))

    # VULN 9: No session expiry or validation
    username = session["user"]
    html = PROFILE_HTML.replace("{username}", username)
    return render_template_string(html)


# VULN 8: Hardcoded credentials in source
@app.route("/admin")
def admin():
    BACKUP_USER = "emergency_admin"     # VULN 8: Hardcoded in source
    BACKUP_PASS = "EmergencyPass123!"    # VULN 8: Hardcoded in source

    if "user" not in session:
        return redirect(url_for("login"))

    # VULN 6: sesion role not properly enforced for admin
    if session.get("role") != "admin":
        return "<h3>Admin access required</h3>"

    return "<h3>Welcome to Admin Panel</h3>"


# VULN 10: Unsafe file upload
@app.route("/upload", methods=["GET", "POST"])
def upload():
    message = ""
    if request.method == "POST":
        file = request.files.get("file")
        if file:
            # VULN 10: No type validation, no size limit, no content check
            filename = file.filename
            file.save(os.path.join(app.config["UPLOAD_FOLDER"], filename))
            message = f"File '{filename}' uploaded successfully"
    html = UPLOAD_HTML.replace("{message}", message)
    return render_template_string(html)


# VULN 4: Missing CSRF token
@app.route("/update_mark", methods=["POST"])
def update_mark():
    if "user" not in session:
        return jsonify({"error": "Not logged in"}), 401
    # VULN 4: No CSRF token validation
    student = request.form.get("student", "")
    mark = request.form.get("mark", "")
    conn = get_db()
    conn.execute("UPDATE marks SET mark = ? WHERE student = ?", (mark, student))
    conn.commit()
    conn.close()
    return jsonify({"status": f"Mark for {student} updated to {mark}"})


# VULN 7: Missing security headers
@app.after_request
def add_security_headers(response):
    # VULN 7: Missing CSP, X-Content-Type-Options, X-Frame-Options
    return response


# ── HTML Templates ──────────────────────────────────────────

INDEX_HTML = """<!DOCTYPE html>
<html>
<head><title>Secure Software App</title></head>
<body>
<h1>Welcome to the Student Portal</h1>
<nav>
<a href="/feedback">Feedback</a> | <a href="/search">Search</a> |
<a href="/login">Login</a> | <a href="/profile">Profile</a> |
<a href="/upload">Upload</a> | <a href="/admin">Admin</a>
</nav>
<p>Web application with several security features needing improvement.</p>
</body>
</html>"""

FEEDBACK_HTML = """<!DOCTYPE html>
<html>
<head><title>Feedback</title></head>
<body>
<h1>Submit Feedback</h1>
<form method="POST">
<input name="name" placeholder="Your name"><br>
<textarea name="message" placeholder="Your feedback"></textarea><br>
<button type="submit">Submit</button>
</form>
<hr>
<div id="output">{result}</div>
<script>
document.getElementById("output").innerHTML = "{result}";
</script>
</body>
</html>"""

SEARCH_HTML = """<!DOCTYPE html>
<html>
<head><title>Search Users</title></head>
<body>
<h1>Search Users</h1>
<form method="POST">
<input name="q" placeholder="Search username" value="{query}">
<button type="submit">Search</button>
</form>
<table border="1"><tr><th>ID</th><th>Username</th><th>Password</th></tr>{rows}</table>
</body>
</html>"""

LOGIN_HTML = """<!DOCTYPE html>
<html>
<head><title>Login</title></head>
<body>
<h1>Login</h1>
<form method="POST">
<input name="username" placeholder="Username"><br>
<input name="password" type="password" placeholder="Password"><br>
<button type="submit">Log in</button>
</form>
<p>{message}</p>
</body>
</html>"""

PROFILE_HTML = """<!DOCTYPE html>
<html>
<head><title>Profile</title></head>
<body>
<h1>User Profile</h1>
<p>Username: {username}</p>
<p><a href="/admin">Admin Panel</a></p>
</body>
</html>"""

UPLOAD_HTML = """<!DOCTYPE html>
<html>
<head><title>File Upload</title></head>
<body>
<h1>Upload File</h1>
<form method="POST" enctype="multipart/form-data">
<input type="file" name="file"><br>
<button type="submit">Upload</button>
</form>
<p>{message}</p>
</body>
</html>"""


if __name__ == "__main__":
    print("=" * 50)
    print(f"SWD80PS - Student ID: {cfg.STUDENT_ID}")
    print(f"Open: http://127.0.0.1:5000")
    print("=" * 50)
    app.run(debug=True, host="127.0.0.1", port=5000)
