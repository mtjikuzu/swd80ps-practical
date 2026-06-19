# SWD80PS - Final Practical Assessment

## Secure Software and Web Development (NQF Level 8)

---

### 🎯 Task Overview

You have been given a **Flask web application** that contains **12 deliberate security vulnerabilities**. Your task is to:

1. **Identify** all 12 vulnerabilities
2. **Fix** the code to make it secure
3. **Verify** your fixes pass the test suite
4. **Submit** your completed work

---

### 🚀 Getting Started

#### Option A: GitHub Codespaces (Recommended)
1. Go to your assigned private repository on GitHub
2. Click the **"Code"** button → **"Open with Codespaces"**
3. Wait for the environment to build (1-2 minutes)
4. In the terminal, run: `pip install flask && python app.py`
5. Open the app at `http://127.0.0.1:5000`

#### Option B: Local Setup
```bash
# Install Python 3.8+ if not already installed
# Install Flask
pip install flask

# Run the app
python app.py
```

---

### 🔐 Step 1: Configure Your Challenge

1. Open **`challenge_config.py`**
2. Set your `STUDENT_ID` to the number your lecturer provided
3. Save the file

---

### 🔍 Step 2: Identify All 12 Vulnerabilities

Explore the app at `http://127.0.0.1:5000` and test each feature.
The 12 vulnerabilities span every route in the app.

| Route | Function |
|-------|----------|
| `/feedback` | Submit feedback (name + message) |
| `/search` | Search user database |
| `/login` | User login |
| `/profile` | User profile (requires login) |
| `/upload` | File upload |
| `/admin` | Admin panel |
| `/update_mark` | Update student marks (POST) |

---

### 🛠️ Step 3: Fix the Vulnerabilities

Edit **`app.py`** to fix each vulnerability. The source code has comments marking each vulnerable area with `# VULN N:`.

**What to fix (12 vulnerabilities):**

| # | Vulnerability | How to Fix |
|---|--------------|------------|
| 1 | No input validation | Add length/type/content validation on all inputs |
| 2 | XSS (innerHTML injection) | Use textContent or escape HTML output |
| 3 | Plaintext password storage | Hash passwords with a strong algorithm (bcrypt/sha256+salts) |
| 4 | Missing CSRF protection | Add CSRF tokens to forms and validate on server |
| 5 | SQL injection | Use parameterized queries (not f-strings) |
| 6 | Weak authentication | Verify passwords properly, enforce RBAC |
| 7 | Missing security headers | Add CSP, X-Content-Type-Options, X-Frame-Options |
| 8 | Hardcoded credentials | Move to config or environment variables |
| 9 | No session timeout | Set PERMANENT_SESSION_LIFETIME, check expiry |
| 10 | Unsafe file upload | Validate file type, size, and content |
| 11 | Error exposure | Use generic error pages, log details server-side |
| 12 | No rate limiting | Limit login attempts (max 5 per minute) |

---

### ✅ Step 4: Test Your Fixes

```bash
python tests/test_fixes.py
```

All 12 checks should show **[PASS]**. If any show **[FAIL]**, review and fix the corresponding vulnerability.

---

### 📤 Step 5: Submission

Submit your work according to your lecturer's instructions. You'll typically need to:

1. **Push** your final code to your private GitHub repository
2. OR **Zip** the entire project folder and upload to Moodle
3. Record a **short 2-minute video** walking through your fixes (optional but recommended)

---

### 📊 Assessment Rubric (50 Marks)

| Criteria | Marks |
|----------|:-----:|
| Correctly identify and fix all 12 vulnerabilities | 30 |
| Code quality and secure practices | 10 |
| Testing evidence (test suite output) | 5 |
| Documentation / commit messages | 5 |
| **Total** | **50** |

---

### ⚠️ Academic Integrity

- This is an **individual assessment**
- Do **not** share your `challenge_config.py` or `STUDENT_ID`
- Your code will be checked for plagiarism
- Using AI to generate the entire solution without understanding is not acceptable
