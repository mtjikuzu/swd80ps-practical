"""
SWD80PS - Final Practical Assessment
Contains 12 deliberate security vulnerabilities. Find and fix ALL.
Run: pip install flask && python app.py
"""
from flask import Flask, request, render_template_string, redirect, url_for, session, jsonify
import os, sqlite3

import challenge_config as cfg

app = Flask(__name__)
app.secret_key = cfg.SK
app.config["SESSION_COOKIE_NAME"] = cfg.CN
app.config["UPLOAD_FOLDER"] = cfg.UD
os.makedirs(cfg.UD, exist_ok=True)

def get_db():
    conn = sqlite3.connect(":memory:")
    conn.execute("CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, username TEXT, password TEXT)")
    conn.execute("CREATE TABLE IF NOT EXISTS marks (id INTEGER PRIMARY KEY, student TEXT, subject TEXT, mark INTEGER)")
    for uname, pwd in cfg.DB.items():
        conn.execute("INSERT INTO users (username, password) VALUES (?, ?)", (uname, pwd))
    for s in [("Alice", 85), ("Bob", 72), ("Charlie", 91)]:
        conn.execute("INSERT INTO marks (student, subject, mark) VALUES (?, ?, ?)", (s[0], "SWD80PS", s[1]))
    conn.commit()
    return conn

@app.route("/", strict_slashes=False)
def index():
    return render_template_string(INDEX_HTML)

# VULN 1: No input validation on form fields
# VULN 2: XSS via innerHTML
@app.route("/feedback", methods=["GET", "POST"], strict_slashes=False)
def feedback():
    result = ""
    if request.method == "POST":
        name = request.form.get("name", "")
        msg = request.form.get("message", "")
        result = f"Feedback from {name}: {msg}"
    html = FEEDBACK_HTML.replace("{result}", result)
    return render_template_string(html)

# VULN 5: SQL injection (string interpolation)
# VULN 11: Error trace exposure
@app.route("/search", methods=["GET", "POST"], strict_slashes=False)
def search():
    results = []
    query = ""
    if request.method == "POST":
        query = request.form.get("q", "")
        conn = get_db()
        try:
            results = conn.execute(f"SELECT * FROM users WHERE username LIKE '%{query}%'").fetchall()
        except Exception as e:
            results = [("ERROR", str(e), "")]
        conn.close()
    rows_html = "".join(f"<tr><td>{r[0]}</td><td>{r[1]}</td><td>{r[2]}</td></tr>" for r in results)
    html = SEARCH_HTML.replace("{query}", query).replace("{rows}", rows_html)
    return render_template_string(html)

# VULN 3: Plaintext passwords in DB
# VULN 6: No password verification
# VULN 11: User enumeration
# VULN 12: No rate limiting
@app.route("/login", methods=["GET", "POST"], strict_slashes=False)
def login():
    msg = ""
    if request.method == "POST":
        username = request.form.get("username", "")
        request.form.get("password", "")
        conn = get_db()
        row = conn.execute(f"SELECT * FROM users WHERE username = '{username}'").fetchone()
        conn.close()
        if row:
            session["user"] = username
            session["role"] = "user"
            msg = f"Logged in as {username}"
        else:
            msg = "User not found"
    return render_template_string(LOGIN_HTML.replace("{msg}", msg))

# VULN 9: No session timeout or validation
@app.route("/profile", strict_slashes=False)
def profile():
    if "user" not in session:
        return redirect(url_for("login"))
    return render_template_string(PROFILE_HTML.replace("{user}", session["user"]))

# VULN 8: Hardcoded backup credentials in source
@app.route("/admin", strict_slashes=False)
def admin():
    _ = "emergency_admin"
    _ = "EmergencyPass123!"
    if "user" not in session:
        return redirect(url_for("login"))
    if session.get("role") != "admin":
        return "<h3>Admin access required</h3>"
    return "<h3>Welcome to Admin Panel</h3>"

# VULN 10: Unsafe file upload (no validation)
@app.route("/upload", methods=["GET", "POST"], strict_slashes=False)
def upload():
    msg = ""
    if request.method == "POST":
        f = request.files.get("file")
        if f:
            f.save(os.path.join(app.config["UPLOAD_FOLDER"], f.filename))
            msg = f"File '{f.filename}' uploaded"
    return render_template_string(UPLOAD_HTML.replace("{msg}", msg))

# VULN 4: No CSRF protection
@app.route("/update_mark", methods=["POST"], strict_slashes=False)
def update_mark():
    if "user" not in session:
        return jsonify({"error": "Not logged in"}), 401
    s = request.form.get("student", "")
    m = request.form.get("mark", "")
    conn = get_db()
    conn.execute("UPDATE marks SET mark = ? WHERE student = ?", (m, s))
    conn.commit()
    conn.close()
    return jsonify({"status": f"Mark for {s} updated to {m}"})

# VULN 7: Missing security headers (CSP, XFO, XCTO)
@app.after_request
def add_security_headers(response):
    return response

INDEX_HTML = """<!DOCTYPE html><html><head><title>Student Portal</title></head><body>
<h1>Student Portal</h1>
<nav><a href="/feedback">Feedback</a> | <a href="/search">Search</a> | <a href="/login">Login</a> | <a href="/profile">Profile</a> | <a href="/upload">Upload</a> | <a href="/admin">Admin</a></nav></body></html>"""

FEEDBACK_HTML = """<!DOCTYPE html><html><head><title>Feedback</title></head><body>
<h1>Submit Feedback</h1>
<form method="POST"><input name="name"><br><textarea name="message"></textarea><br><button>Send</button></form>
<hr><div id="output">{result}</div>
<script>document.getElementById("output").innerHTML = "{result}";</script></body></html>"""

SEARCH_HTML = """<!DOCTYPE html><html><head><title>Search</title></head><body>
<h1>Search</h1><form method="POST"><input name="q" value="{query}"><button>Go</button></form>
<table border="1"><tr><th>ID</th><th>Name</th><th>Pass</th></tr>{rows}</table></body></html>"""

LOGIN_HTML = """<!DOCTYPE html><html><head><title>Login</title></head><body>
<h1>Login</h1><form method="POST"><input name="username"><br><input name="password" type="password"><br><button>Log in</button></form><p>{msg}</p></body></html>"""

PROFILE_HTML = """<!DOCTYPE html><html><head><title>Profile</title></head><body>
<h1>Profile</h1><p>User: {user}</p><p><a href="/admin">Admin Panel</a></p></body></html>"""

UPLOAD_HTML = """<!DOCTYPE html><html><head><title>Upload</title></head><body>
<h1>File Upload</h1><form method="POST" enctype="multipart/form-data"><input type="file" name="file"><br><button>Upload</button></form><p>{msg}</p></body></html>"""

if __name__ == "__main__":
    print(f"SWD80PS - Student ID: {cfg.STUDENT_ID}")
    print("Open: http://127.0.0.1:5000")
    app.run(debug=True, host="0.0.0.0", port=5000)
