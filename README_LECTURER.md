# SWD80PS - Final Practical Assessment
## Lecturer Setup Guide

---

### 📋 Student List (14 students)

| # | Student Name | Email |
|---|-------------|-------|
| 1 | ANDREAS ANGULA ABNER | andreasabner@aol.com |
| 2 | JOSEPH NDAKUMA AMAPINDI | 260133361@campus.ium.edu.na |
| 3 | JOHANNES NIILENGE DEMETIRIUS | 202033759@campus.ium.edu.na |
| 4 | ELIZABETH TSHALONGO EFRAIM | 140058117@Campus.ium.edu.na |
| 5 | HILJA NDIWENI KAKONGA | hkakonga@gmail.com |
| 6 | ENGELBERTH JOSEPH HAIRWA KANDJEKE | 170055485@Campus.ium.edu.na |
| 7 | SUAMA NANGOMBE MASHUNA | 202116093@Campus.ium.edu.na |
| 8 | TOINI POPYENINAWA MUNDANDALA | 140054561@Campus.ium.edu.na |
| 9 | ROSINA JN NENKONO | 202171760@Campus.ium.edu.na |
| 10 | SALOMO DHIGININA NTINDA | 260136506@campus.ium.edu.na |
| 11 | TULELA NDAKOLA SHIPANGA | 260064254@Campus.ium.edu.na |
| 12 | ABED-NEGO TUHAFENI SHISHIVENI | 170057976@campus.ium.edu.na |
| 13 | BIANCA BENE SIMATAA | biancasimataa@gmail.com |
| 14 | CHARLES SIVEREGI | 260154849@campus.ium.edu.na |

---

### 🚀 Setup Instructions

#### Step 1: Create the Template Repository

```bash
# Create a public template repo on GitHub
gh repo create mtjikuzu/swd80ps-practical --public --template

# Clone and push the prepared files
cd /path/to/swd80ps-practical
git remote add origin https://github.com/mtjikuzu/swd80ps-practical.git
git add .
git commit -m "Initial commit: vulnerable Flask app for practical assessment"
git push -u origin main

# Mark as a template repo
gh repo edit mtjikuzu/swd80ps-practical --template
```

#### Step 2: Generate Unique Student Assignments

Run the seeding script to create per-student repos:

```bash
python generate_student_repos.py
```

This will:
- Create 14 private repos: `swd80ps-practical-student-01` through `swd80ps-practical-student-14`
- Clone the template
- Set a unique `STUDENT_ID` and `challenge_config.py` in each
- Push to GitHub
- Generate a `student_access.csv` file with repo URLs

#### Step 3: Add Students as Collaborators

```bash
# For each student, add them to their repo
gh api repos/mtjikuzu/swd80ps-practical-student-01/collaborators/STUDENT_GITHUB_USERNAME -X PUT
```

*Note: You'll need each student's GitHub username. Ask them to create an account if they don't have one.*

#### Step 4: Share Student IDs

Send each student:
1. Their unique **Student ID** (1-14)
2. Their **private repo URL**
3. The **README.md** instructions

---

### 📝 How the Uniqueness System Works

Each student gets the same **app.py** with all 12 vulnerabilities present. The uniqueness comes from:

| Element | How It Varies |
|---------|---------------|
| `challenge_config.py` | Unique admin usernames, passwords, cookie names |
| `STUDENT_ID` | Seed for all randomized values (1-14) |
| Login credentials | Each student has different valid usernames/passwords |
| Test expectations | The test suite validates unique values per student |
| Secret flag | Each student must produce a unique hash |

This ensures:
- **Same difficulty**: All 12 vulnerabilities are present for everyone
- **Different answers**: No two students have the same credentials or config
- **Cannot copy**: Even if they compare, the login values, cookie names, and expected test outputs differ

---

### 📊 Marking Rubric

| Criteria | Marks | How to Assess |
|----------|:-----:|---------------|
| Vulnerability identification (implied by fixes) | 30 | Run `python tests/test_fixes.py` — count passes |
| Code quality and secure practices | 10 | Review code: appropriate fixes, not bypasses |
| Testing evidence (test suite output) | 5 | Screenshot of test results |
| Documentation / commit messages | 5 | Meaningful commit messages, code comments |
| **Total** | **50** | |

**Pass threshold**: 24/50 (48%) = all 12 vulnerabilities identified

---

### 🔍 Anti-Plagiarism Checks

1. **Config comparison**: Run `diff` on `challenge_config.py` between students — they should all be different
2. **Commit history**: Check that students made incremental commits, not one massive upload
3. **Code similarity scan**: Use `difflib` to compare fixed `app.py` files — similar fixes but different values
4. **Video walkthrough** (optional): Ask students to record a 2-min phone video explaining 3 of their fixes

---

### 🧪 Testing a Student's Submission

```bash
# Clone their repo
git clone https://github.com/mtjikuzu/swd80ps-practical-student-XX.git
cd swd80ps-practical-student-XX

# Install and test
pip install flask
python tests/test_fixes.py

# Expected: 12/12 passed
```

---

### 📁 Repository Structure

```
swd80ps-practical/
├── app.py                      # Main Flask app (vulnerable)
├── challenge_config.py         # Per-student config
├── requirements.txt            # Python dependencies
├── README.md                   # Student instructions
├── tests/
│   └── test_fixes.py           # Auto-grading test suite
├── .devcontainer/
│   └── devcontainer.json       # Codespaces config
├── .gitignore
└── generate_student_repos.py   # Seeding script (lecturer only)
```
