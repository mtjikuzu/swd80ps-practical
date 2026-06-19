# SWD80PS — Final Practical Assessment

## Secure Software and Web Development (NQF Level 8)

---

### Task Overview

You have been given a **Flask web application** that contains **12 deliberate security vulnerabilities**. Your task is to:

1. **Identify** all 12 vulnerabilities by exploring the running application
2. **Fix** the code to make it secure
3. **Verify** your fixes pass the test suite
4. **Submit** your completed work

---

### Getting Started

#### Option A: GitHub Codespaces (Recommended — No Installation Needed)
1. Go to your assigned private repository on GitHub (URL provided by your lecturer)
2. Click the green **"Code"** button → **"Codespaces"** tab → **"Create codespace on main"**
3. Wait 1–2 minutes for the environment to build
4. In the terminal, run: `pip install flask && python app.py`
5. Open the app at `http://127.0.0.1:5000`

#### Option B: Local Setup
```bash
pip install flask
python app.py
```

---

### Step 1: Configure Your Student ID

1. Open **`challenge_config.py`** in the file explorer
2. Set `STUDENT_ID = X` where X is the unique ID your lecturer provided
3. Save the file (Ctrl+S)

---

### Step 2: Explore the Application

Run the app and visit each route:

| Route | Function |
|-------|----------|
| `/feedback` | Submit feedback (name + message) |
| `/search` | Search user database |
| `/login` | User login |
| `/profile` | User profile (requires login) |
| `/upload` | File upload |
| `/admin` | Admin panel |
| `/update_mark` | Update student marks (POST) |

Identify the 12 security vulnerabilities spread across these routes. Look for:
- Unsafe handling of user input
- Missing security controls
- Weak authentication and session management
- Insecure file handling
- Poor error handling

---

### Step 3: Fix the Vulnerabilities

Edit **`app.py`** to fix each vulnerability. The source code has comments marking each vulnerable area with `# VULN N:`.

**The 12 vulnerability types to fix (in any order):**

| # | Vulnerability Type | Related Route(s) |
|:-:|-------------------|:----------------:|
| 1 | Input validation | `/feedback` |
| 2 | Cross-Site Scripting (XSS) | `/feedback` |
| 3 | Password storage | `/login` |
| 4 | CSRF protection | `/update_mark` |
| 5 | SQL injection | `/search`, `/login` |
| 6 | Authentication logic | `/login` |
| 7 | Security headers | All routes |
| 8 | Hardcoded credentials | `/admin` |
| 9 | Session management | `/profile` |
| 10 | File upload security | `/upload` |
| 11 | Error handling | `/search`, `/login` |
| 12 | Rate limiting | `/login` |

---

### Step 4: Test Your Fixes

```bash
python tests/test_fixes.py
```

All 12 checks must show **[PASS]** before submitting.

---

### Step 5: Submit Your Work

**You do not need to zip or upload files.** Your lecturer already has access to your private repository.

1. **Commit and push** your final code to your private GitHub repository:
```bash
git add -A
git commit -m "Fixed all 12 vulnerabilities"
git push
```

2. **Take a screenshot** of the terminal showing `12/12 passed`

3. **Go to the Moodle course page** → **Final Practical Assessment** dropbox and submit:
   - Your **GitHub repository URL** (e.g., `https://github.com/mtjikuzu/swd80ps-practical-student-XX`)
   - Upload your **screenshot** showing all tests passing

That's it — your lecturer will clone your repo to grade your code.

---

### Assessment Rubric (50 Marks)

| Criteria | Marks |
|----------|:-----:|
| All 12 vulnerabilities correctly identified and fixed | 30 |
| Code quality and use of secure coding best practices | 10 |
| Test suite screenshot (evidence of testing) | 5 |
| Documentation, commit messages, and presentation | 5 |
| **Total** | **50** |

---

### Academic Integrity

- This is an **individual assessment**
- Do **not** share your `challenge_config.py` file or `STUDENT_ID`
- Your code will be checked for plagiarism
- Using AI to generate the complete solution without understanding the code is not acceptable
