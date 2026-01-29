# 🚀 Full-Stack Test Automation Framework

## Welcome! Start Here 👋

This document will help you understand **how the entire testing framework works** in the **easiest way possible**.

---

## 📚 What to Read (In Order):

1. **This file** (00_START_HERE.md) - Overview
2. **01_FILE_STRUCTURE.md** - Shows folder structure & what each file does
3. **02_VISUAL_FLOW.md** - Diagrams showing how tests flow
4. **03_HOW_TESTS_RUN.md** - Step-by-step execution explained
5. **04_FUNCTION_MAP.md** - Which function calls which & passes what values

---

## 🎯 What This Framework Does

```
Simple Goal: Test authentication and orders automatically

Step 1: Create a test account ✅
Step 2: Login with that account ✅
Step 3: Verify everything works ✅
Step 4: Save the login session ✅
Step 5: Reuse same session for other tests ✅
```

---

## 🏗️ High-Level Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    TEST RUNNER (pytest)                     │
│                                                             │
│  Starts: pytest tests/authentication/                      │
│  Runs: test_01, test_02, test_03, test_04, test_05         │
└─────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────┐
│              BROWSER LAYER (SeleniumBase)                   │
│                                                             │
│  Opens: https://dev.v.shipgl.in                            │
│  Fills forms, clicks buttons, waits for pages              │
│  Stores: session cookies automatically                     │
└─────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────┐
│            PAGE OBJECTS (What to interact with)            │
│                                                             │
│  SignupPage     - signup form selectors                    │
│  LoginPage      - login form selectors                     │
│  OrdersPage     - orders page selectors                    │
└─────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────┐
│             FLOWS (How to interact - sequences)            │
│                                                             │
│  AuthenticationFlow:                                       │
│    - step_1_signup(user)                                   │
│    - step_2_verify_mobile()                                │
│    - step_3_logout()                                       │
│    - step_4_login(email, password)                         │
└─────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────┐
│          UTILITIES (Database, Session, Config)             │
│                                                             │
│  db.py       - Update/delete database records              │
│  session.py  - Store test user data & cookies              │
│  settings.py - Database credentials, passwords             │
└─────────────────────────────────────────────────────────────┘
```

---

## 🔄 Simple Example Flow

```
Test Starts:
│
├─ Browser opens: https://dev.v.shipgl.in/auth/signup
│
├─ SignupPage object gives us form selectors
│
├─ AuthenticationFlow tells us WHAT to fill:
│  ├─ first_name: "John"
│  ├─ last_name: "Doe"
│  ├─ email: "auto_xxx@gmail.in"
│  └─ password: "Test@1234"
│
├─ Browser fills each field and clicks Submit
│
├─ Page redirects to: /verify-mobile
│
├─ Database is updated: mobile_verified = 1
│
├─ Browser navigates to login page
│
├─ Login with same email + password
│
├─ Cookies are saved in session
│
└─ Test completes ✅
```

---

## 📁 Folder Organization

```
Full-Stack-Test-Automation-Framework/
│
├── configs/              ← Configuration (DB creds, passwords)
│   └── settings.py       ← Database & base URL config
│
├── src/                  ← Main code
│   ├── core/
│   │   └── base_page.py  ← Parent class for all page objects
│   ├── pages/            ← Where to interact (selectors)
│   │   └── authentication/
│   │       ├── signup_page.py
│   │       ├── login_page.py
│   │       └── mobile_verification_page.py
│   ├── flows/            ← How to interact (sequences)
│   │   └── authentication_flow.py
│   ├── locators/         ← CSS/XPath selectors
│   │   └── authentication_locators.py
│   └── utils/            ← Helper functions
│       ├── db.py         ← Database operations
│       └── session.py    ← Session & user data
│
├── tests/                ← All test files
│   └── authentication/
│       ├── test_01_auth_e2e.py      ← E2E flow
│       ├── test_02_signup_positive.py
│       ├── test_03_signup_negative.py
│       ├── test_04_login_positive.py
│       └── test_05_login_negative.py
│
└── docs/                 ← Documentation (this folder)
    ├── 00_START_HERE.md              ← You are here
    ├── 01_FILE_STRUCTURE.md          ← What each file does
    ├── 02_VISUAL_FLOW.md             ← Flow diagrams
    ├── 03_HOW_TESTS_RUN.md           ← Step-by-step execution
    └── 04_FUNCTION_MAP.md            ← Function calls & values
```

---

## 🎓 Key Concepts

### 1️⃣ **Page Objects**
```
What is it? A class that contains:
- Form field selectors (CSS/XPath)
- Methods to fill fields
- Methods to click buttons

Example:
  class LoginPage:
      EMAIL = "input[name='email']"
      PASSWORD = "input[name='password']"
      
      def login(self, email, password):
          self.sb.type(self.EMAIL, email)
          self.sb.type(self.PASSWORD, password)
          self.sb.click(self.SUBMIT)
```

### 2️⃣ **Flows**
```
What is it? Orchestrates multiple page interactions

Example:
  class AuthenticationFlow:
      def signup(self, user):
          # Use SignupPage
          # Fill fields with user data
          # Click submit
      
      def login(self, email, password):
          # Use LoginPage
          # Fill credentials
          # Click submit
```

### 3️⃣ **Session Management**
```
What is it? Remembers user data & browser cookies

First test (auth):
  ✅ Create account
  ✅ Login
  ✅ Save cookies in _test_session

Second test (orders):
  ✅ Check: is_logged_in()?
  ✅ YES → Use existing cookies (no login needed)
  ✅ NO → Run auth test first
```

### 4️⃣ **Database Operations**
```
What is it? Direct MySQL queries

Example:
  # After signup, user created with mobile_verified = 0
  # Simulate OTP verification:
  update_mobile_verified(email)  # Sets mobile_verified = 1
```

---

## 🚀 Quick Start

### Run All Tests:
```bash
./venv/bin/python -m pytest tests/authentication/ -v
```

### Run Single Test:
```bash
./venv/bin/python -m pytest tests/authentication/test_01_auth_e2e.py -v
```

### Expected Output:
```
test_01_auth_e2e.py PASSED
test_02_signup_positive.py PASSED
test_03_signup_negative.py PASSED
test_04_login_positive.py PASSED
test_05_login_negative.py PASSED

======================== 30 passed in 2:54 ========================
```

---

## 📖 Next Steps

Read the docs in order:
1. **01_FILE_STRUCTURE.md** - Understand file organization
2. **02_VISUAL_FLOW.md** - See visual flow diagrams
3. **03_HOW_TESTS_RUN.md** - Follow step-by-step execution
4. **04_FUNCTION_MAP.md** - See function calls & data flow

---

## ❓ Quick FAQ

**Q: How does it know which email to use?**
```
A: session.py generates unique email:
   auto_{timestamp}_{random}@gmail.in
   
   Example: auto_1704067200000_45678@gmail.in
```

**Q: How does login work if no OTP is sent?**
```
A: After signup, the test updates database:
   UPDATE vendor SET mobile_verified = 1
   
   This simulates user entering OTP - makes login possible
```

**Q: How does session persist between tests?**
```
A: Global dictionary in session.py:
   _test_session = {
       "user": {...},
       "browser_cookies": [...]
   }
```

**Q: Can I run orders test without auth test?**
```
A: No - need to run auth test first to create session
   Tests must run in order: test_01 → test_02 → test_03...
```

---

## 🎯 Summary

This framework:
- ✅ Automates signup & login testing
- ✅ Creates unique test accounts each time
- ✅ Reuses browser session across tests
- ✅ Verifies everything works end-to-end
- ✅ Takes ~3 minutes to run all 30 tests

Ready to dive deeper? Read **01_FILE_STRUCTURE.md** next! 📚
