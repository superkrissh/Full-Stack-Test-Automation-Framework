# 🔄 COMPLETE FLOW EXPLANATION - Folder by Folder

**What happens BEFORE, DURING, and AFTER each step with DATA flowing between folders**

---

## 📊 STARTING POINT: Before Any Test Runs

### Initial State:

```
YOUR COMPUTER
├─ Browser: CLOSED ❌
├─ Database: CONNECTED (waiting)
└─ Python Variables: EMPTY
```

---

## 🚀 STEP 0: Pytest Starts (conftest.py runs)

### What Happens:

```
USER TYPES:
  pytest tests/authentication/

                    ↓

PYTHON LOADS conftest.py
  
  conftest.py reads from:
  ├─ configs/settings.py
  │  └─ Gets: DATABASE_CONFIG
  │     └─ host: 3.6.16.231
  │     └─ user: shipgl_user
  │     └─ password: ****
  │     └─ database: staging
  │
  └─ Starts SeleniumBase Browser
     └─ Opens: https://dev.v.shipgl.in

                    ↓

STATE NOW:
├─ Browser: OPEN ✅
├─ Database: CONNECTED ✅
├─ Page shown: Login page
└─ Ready for tests
```

---

## 🧪 TEST_01 EXECUTION: Complete Flow

### Timeline with Folder Interactions:

```
TEST_01 STARTS
│
├─ STEP 1: Generate Test User
│  
│  Python Code Runs:
│    from src.utils.session import create_fresh_test_user
│
│  FILE ACCESSED:
│    src/utils/session.py
│    
│    INSIDE session.py:
│    ├─ import time → Gets current milliseconds (1704067200000)
│    ├─ import random → Gets random number (45678)
│    └─ Creates email: auto_1704067200000_45678@gmail.in
│    
│  DATA CREATED (in Python memory):
│    user = {
│        "email": "auto_1704067200000_45678@gmail.in",
│        "password": "Test@1234",
│        "mobile": "9876543210",
│        "first_name": "John",
│        "last_name": "Doe"
│    }
│
│  ✅ User data CREATED in PYTHON MEMORY
│
├─ STEP 2: Store User in Session
│
│  Python Code Runs:
│    from src.utils.session import create_test_session
│    create_test_session(user)
│
│  FILE ACCESSED:
│    src/utils/session.py
│    
│    INSIDE session.py:
│    global _test_session = {}  ← Empty dictionary
│    _test_session["user"] = user  ← Add user
│    
│  DATA STORED (in PYTHON MEMORY):
│    _test_session = {
│        "user": {
│            "email": "auto_1704067200000_45678@gmail.in",
│            "password": "Test@1234",
│            ...
│        }
│    }
│
│  ✅ User data STORED in SESSION (global memory)
│  ✅ Other tests can now use: get_test_user()
│
├─ STEP 3: Open Signup Page in Browser
│
│  Python Code Runs:
│    browser.open("https://dev.v.shipgl.in/auth/signup")
│
│  BROWSER BEHAVIOR:
│    ├─ Current page: Login
│    └─ Navigates to: Signup page
│
│  PAGE SHOWN:
│    ┌─────────────────────────┐
│    │ Create Account          │
│    │ First Name: [____]      │
│    │ Last Name:  [____]      │
│    │ Mobile:     [____]      │
│    │ Email:      [____]      │
│    │ Password:   [____]      │
│    │ [Sign Up]               │
│    └─────────────────────────┘
│
│  ✅ Browser now showing SIGNUP PAGE
│
├─ STEP 4: Fill Form & Get Selectors
│
│  Python Code Runs:
│    from src.pages.authentication.signup_page import SignupPage
│    signup_page = SignupPage(browser, base_url)
│
│  FILES ACCESSED (in order):
│  
│    1️⃣ src/pages/authentication/signup_page.py
│       CLASS: SignupPage(BasePage)
│       
│       INSIDE signup_page.py:
│       ├─ Inherits from: src/core/base_page.py
│       ├─ Gets selectors from: src/locators/authentication_locators.py
│       │  └─ FIRST_NAME = "input[name='firstName']"
│       │  └─ EMAIL = "input[name='email']"
│       │  └─ PASSWORD = "input[name='password']"
│       │  └─ SUBMIT = "button[type='submit']"
│       │
│       └─ Methods available:
│           └─ signup(first_name, last_name, mobile, email, password)
│    
│    2️⃣ src/core/base_page.py
│       PROVIDES:
│       ├─ self.sb = SeleniumBase browser
│       ├─ self.base_url = "https://dev.v.shipgl.in"
│       └─ Common methods:
│           ├─ type(selector, text)
│           └─ click(selector)
│    
│    3️⃣ src/locators/authentication_locators.py
│       CONTAINS:
│       ├─ SignupPageLocators.FIRST_NAME = "input[name='firstName']"
│       ├─ SignupPageLocators.EMAIL = "input[name='email']"
│       └─ All other field selectors
│
│  DATA STORED (in Python memory):
│    signup_page = SignupPage(browser, base_url)
│    └─ signup_page.FIRST_NAME = "input[name='firstName']"
│    └─ signup_page.EMAIL = "input[name='email']"
│    └─ etc...
│
│  ✅ SignupPage object CREATED with selectors loaded
│
├─ STEP 5: Fill Form Fields & Submit
│
│  Python Code Runs:
│    signup_page.signup(
│        first_name="John",
│        last_name="Doe",
│        mobile="9876543210",
│        email="auto_1704067200000_45678@gmail.in",
│        password="Test@1234"
│    )
│
│  INSIDE signup_page.signup() METHOD:
│  ├─ self.type(self.FIRST_NAME, "John")
│  │  └─ Browser finds: input[name='firstName']
│  │  └─ Browser types: "John"
│  │  └─ Form field now shows: "John"
│  │
│  ├─ self.type(self.LAST_NAME, "Doe")
│  │  └─ Browser finds: input[name='lastName']
│  │  └─ Browser types: "Doe"
│  │
│  ├─ self.type(self.MOBILE, "9876543210")
│  │  └─ Browser finds: input[name='mobile']
│  │  └─ Browser types: "9876543210"
│  │
│  ├─ self.type(self.EMAIL, "auto_1704067200000_45678@gmail.in")
│  │  └─ Browser finds: input[name='email']
│  │  └─ Browser types: "auto_1704067200000_45678@gmail.in"
│  │
│  ├─ self.type(self.PASSWORD, "Test@1234")
│  │  └─ Browser finds: input[name='password']
│  │  └─ Browser types: "Test@1234"
│  │
│  ├─ self.click(self.TERMS_CHECKBOX)
│  │  └─ Browser finds: input[type='checkbox']
│  │  └─ Browser clicks: checkbox checked ✓
│  │
│  └─ self.click(self.SUBMIT_BUTTON)
│     └─ Browser finds: button[type='submit']
│     └─ Browser clicks: Submit button
│
│  BROWSER BEHAVIOR:
│    ├─ Form now filled with all data
│    ├─ Submit button clicked
│    └─ Browser sends POST request to server:
│       POST https://dev.v.shipgl.in/auth/signup
│       DATA SENT: {
│           firstName: "John",
│           lastName: "Doe",
│           mobile: "9876543210",
│           email: "auto_1704067200000_45678@gmail.in",
│           password: "Test@1234"
│       }
│
│  ✅ FORM SUBMITTED to SERVER
│
├─ STEP 6: Server Creates User in Database
│
│  SERVER BEHAVIOR (not Python code):
│    └─ Receives POST data
│    └─ Validates data
│    └─ Executes SQL:
│       
│       INSERT INTO vendor (
│           firstname,
│           lastname,
│           mobile,
│           email,
│           password,
│           mobile_verified
│       ) VALUES (
│           "John",
│           "Doe",
│           "9876543210",
│           "auto_1704067200000_45678@gmail.in",
│           hash("Test@1234"),
│           0  ← NOT VERIFIED YET
│       )
│
│  DATABASE NOW CONTAINS:
│    vendor table:
│    ┌──────────────────────────────────────────────────┐
│    │ vendor_id │ firstname │ lastname │ mobile_verified│
│    ├───────────┼───────────┼──────────┼────────────────┤
│    │ 123       │ John      │ Doe      │ 0 (NOT VERIFIED)
│    └──────────────────────────────────────────────────┘
│
│  ✅ USER CREATED in DATABASE (mobile_verified = 0)
│
├─ STEP 7: Browser Waits & Redirects
│
│  BROWSER BEHAVIOR:
│    ├─ Server responds: "Success"
│    ├─ Browser redirects to: /verify-mobile
│    └─ Page shown:
│       ┌─────────────────────────┐
│       │ Verify Your Mobile      │
│       │ OTP sent to 98765...0   │
│       │ Enter OTP: [____]       │
│       │ [Verify]                │
│       └─────────────────────────┘
│
│  ✅ PAGE REDIRECTED to mobile verify
│
├─ STEP 8: Update Database (Simulate OTP)
│
│  Python Code Runs:
│    from src.utils.db import update_mobile_verified
│    update_mobile_verified(email)
│
│  FILE ACCESSED:
│    src/utils/db.py
│    
│    INSIDE db.py:
│    ├─ get_db_connection()
│    │  └─ Reads from: configs/settings.py
│    │     └─ Gets DATABASE_CONFIG
│    │     └─ Connects to: 3.6.16.231:3306
│    │
│    ├─ Execute SQL:
│    │  UPDATE vendor
│    │  SET mobile_verified = 1
│    │  WHERE email = 'auto_1704067200000_45678@gmail.in'
│    │
│    └─ Returns: Number of rows updated (1)
│
│  DATABASE CHANGES:
│    vendor table:
│    ┌──────────────────────────────────────────────────┐
│    │ vendor_id │ firstname │ lastname │ mobile_verified│
│    ├───────────┼───────────┼──────────┼────────────────┤
│    │ 123       │ John      │ Doe      │ 1 (VERIFIED) ✅
│    └──────────────────────────────────────────────────┘
│
│  ✅ DATABASE UPDATED (mobile_verified = 0 → 1)
│
├─ STEP 9: Logout
│
│  Python Code Runs:
│    browser.click("logout button selector")
│
│  BROWSER BEHAVIOR:
│    ├─ Browser clicks logout button
│    ├─ Server clears session cookie
│    ├─ Browser redirected to: /auth/login
│    └─ Page shown: Login page (fresh, not logged in)
│
│  ✅ LOGGED OUT successfully
│
├─ STEP 10: Login Again
│
│  Python Code Runs:
│    from src.pages.authentication.login_page import LoginPage
│    login_page = LoginPage(browser, base_url)
│    login_page.login(
│        email="auto_1704067200000_45678@gmail.in",
│        password="Test@1234"
│    )
│
│  FILES ACCESSED:
│    1️⃣ src/pages/authentication/login_page.py
│       ├─ Inherits from: src/core/base_page.py
│       ├─ Gets selectors from: src/locators/authentication_locators.py
│       │  └─ LOGIN_EMAIL = "input[name='email']"
│       │  └─ LOGIN_PASSWORD = "input[name='password']"
│       │  └─ SUBMIT = "button[type='submit']"
│       │
│       └─ Methods:
│           └─ login(email, password)
│    
│    2️⃣ src/core/base_page.py (parent class)
│    3️⃣ src/locators/authentication_locators.py (selectors)
│
│  INSIDE login_page.login() METHOD:
│    ├─ self.type(self.EMAIL, "auto_1704067200000_45678@gmail.in")
│    ├─ self.type(self.PASSWORD, "Test@1234")
│    └─ self.click(self.SUBMIT_BUTTON)
│
│  BROWSER BEHAVIOR:
│    ├─ Form filled with credentials
│    ├─ Submit clicked
│    └─ POST request sent to server:
│       POST https://dev.v.shipgl.in/auth/login
│       DATA SENT: {
│           email: "auto_1704067200000_45678@gmail.in",
│           password: "Test@1234"
│       }
│
│  ✅ LOGIN FORM SUBMITTED
│
├─ STEP 11: Server Validates Login
│
│  SERVER BEHAVIOR (not Python code):
│    ├─ Receives login data
│    ├─ Executes SQL:
│    │  SELECT * FROM vendor
│    │  WHERE email = 'auto_1704067200000_45678@gmail.in'
│    │
│    ├─ Checks:
│    │  ├─ Email exists? YES ✅
│    │  ├─ Password correct? YES ✅
│    │  ├─ mobile_verified = 1? YES ✅ (We updated it!)
│    │
│    └─ Creates session cookie
│
│  BROWSER RECEIVES:
│    ├─ Set-Cookie header
│    ├─ Browser stores cookie automatically
│    └─ Browser redirected to: /merchant-agreement
│
│  ✅ LOGIN SUCCESSFUL
│
├─ STEP 12: Accept Merchant Agreement
│
│  Python Code Runs:
│    browser.click("agree checkbox")
│    browser.click("continue button")
│
│  BROWSER BEHAVIOR:
│    ├─ Checkbox clicked (checked ✓)
│    ├─ Continue button clicked
│    └─ Browser redirected to: /dashboard
│
│  ✅ MERCHANT AGREEMENT ACCEPTED
│
├─ STEP 13: Save Session with Cookies
│
│  Python Code Runs:
│    create_test_session(user)  ← Already called, but now:
│
│  INSIDE session.py:
│    _test_session = {
│        "user": {
│            "email": "auto_1704067200000_45678@gmail.in",
│            "password": "Test@1234",
│            "mobile": "9876543210",
│            "first_name": "John",
│            "last_name": "Doe"
│        },
│        "browser_cookies": [
│            {
│                "name": "sessionId",
│                "value": "abc123xyz",
│                "domain": "dev.v.shipgl.in",
│                "path": "/"
│            }
│        ]
│    }
│
│  STORED IN PYTHON MEMORY:
│    ✅ User data (email, password, mobile, names)
│    ✅ Browser cookies (session ID, domain, path)
│
│  ✅ SESSION SAVED (can be used by test_04)
│
└─ TEST_01 COMPLETE ✅
```

---

## 📂 Data Journey Summary (TEST_01):

```
STEP 1: Generate User
  Location: Python memory
  Data: user dict

           ↓ STEP 2: Store in Session
  Location: src/utils/session.py (global _test_session)
  Data: user dict in session

           ↓ STEP 3-5: Fill Form & Submit
  Location: Browser (HTML form)
  Data: first_name, last_name, mobile, email, password

           ↓ STEP 6: Create User
  Location: Database (vendor table)
  Data: INSERT vendor record (mobile_verified = 0)

           ↓ STEP 8: Update Mobile Verified
  Location: Database (vendor table)
  Data: UPDATE mobile_verified = 1

           ↓ STEP 10-11: Login
  Location: Browser → Server checks Database
  Data: email, password validation

           ↓ STEP 12: Store Session Cookies
  Location: Browser (cookies) + Python memory (session)
  Data: sessionId cookie, user data

✅ FINAL STATE:
  ├─ User in database: mobile_verified = 1
  ├─ Session in Python: user data + cookies
  └─ Browser: Logged in with cookies
```

---

## 🎬 TEST_02 EXECUTION: (Quick Overview)

```
TEST_02 STARTS (test_02_signup_positive.py)

├─ STEP 1: Generate NEW Test User
│  Location: src/utils/session.py::create_fresh_test_user()
│  Data: New email, mobile, password
│  └─ auto_1704067200050_11111@gmail.in (DIFFERENT from test_01)
│
├─ STEP 2: Signup (Same as test_01)
│  ├─ Navigate to signup page
│  ├─ Fill form (use new user data)
│  ├─ Submit form
│  └─ Browser redirects to mobile verify
│
├─ STEP 3: Verify Signup (Check if redirect happened)
│  └─ Assert: URL contains "/verify-mobile"
│
├─ STEP 4: Cleanup
│  Location: src/utils/db.py::delete_vendor()
│  Data: DELETE user from database
│  └─ User deleted (cleanup for this test)
│
└─ TEST_02 COMPLETE ✅

IMPORTANT:
  ❌ Test_02 does NOT update mobile_verified
  ❌ Test_02 does NOT login
  ❌ Test_02 creates & deletes its own user (isolated)
  ✅ Test_01's user still in database (not deleted)
```

---

## 🎬 TEST_04 EXECUTION: Uses Test_01's User

```
TEST_04 STARTS (test_04_login_positive.py)

├─ STEP 1: Get User from Session
│  Location: src/utils/session.py::get_test_user()
│  Data: Retrieves stored user dict:
│  └─ {
│       email: "auto_1704067200000_45678@gmail.in",
│       password: "Test@1234",
│       ...
│     }
│
│  ✅ USES SAME USER from TEST_01 (not creating new one)
│
├─ STEP 2: Login with Stored User
│  ├─ Navigate to login page
│  ├─ Fill email: "auto_1704067200000_45678@gmail.in" (from session)
│  ├─ Fill password: "Test@1234" (from session)
│  ├─ Submit form
│  └─ Server validates against database:
│     ├─ Email: auto_1704067200000_45678@gmail.in ✅ EXISTS (from test_01)
│     ├─ Password: Test@1234 ✅ CORRECT
│     ├─ mobile_verified = 1 ✅ YES (updated in test_01)
│
├─ STEP 3: Verify Login Success
│  └─ Assert: Dashboard visible
│
└─ TEST_04 COMPLETE ✅

DEPENDENCY:
  ⚠️  Test_04 DEPENDS on Test_01's execution
  ✅ Test_04 REUSES Test_01's user
  ✅ This is why tests must run in order: test_01 → test_04
```

---

## 📊 Folder Interaction Summary

### Folders Accessed During TEST_01:

```
┌─────────────────────────────────────────────────────────┐
│ TEST_01_AUTH_E2E.PY (Test Runner)                       │
└──────────────┬──────────────────────────────────────────┘
               │
               ├──→ src/utils/session.py
               │    ├─ create_fresh_test_user()
               │    │  └─ Returns: user dict
               │    ├─ create_test_session(user)
               │    │  └─ Stores: _test_session["user"]
               │    └─ get_test_user()
               │       └─ Retrieves: stored user
               │
               ├──→ src/pages/authentication/signup_page.py
               │    ├─ Inherits from: src/core/base_page.py
               │    ├─ Uses: src/locators/authentication_locators.py
               │    └─ Method: signup(first_name, last_name, mobile, email, password)
               │
               ├──→ src/pages/authentication/login_page.py
               │    ├─ Inherits from: src/core/base_page.py
               │    ├─ Uses: src/locators/authentication_locators.py
               │    └─ Method: login(email, password)
               │
               ├──→ src/utils/db.py
               │    ├─ Uses: configs/settings.py (DATABASE_CONFIG)
               │    ├─ update_mobile_verified(email)
               │    │  └─ Connects to: MySQL database
               │    │  └─ Updates: vendor table
               │    └─ user_exists(email)
               │       └─ Queries: vendor table
               │
               ├──→ configs/settings.py
               │    ├─ DATABASE_CONFIG (MySQL credentials)
               │    ├─ BASE_URL ("https://dev.v.shipgl.in")
               │    └─ HARD_PASSWORD ("Test@1234")
               │
               ├──→ src/core/base_page.py
               │    ├─ Parent class for all page objects
               │    └─ Common methods: type(), click(), wait_for_element()
               │
               ├──→ src/locators/authentication_locators.py
               │    ├─ FIRST_NAME = "input[name='firstName']"
               │    ├─ EMAIL = "input[name='email']"
               │    ├─ PASSWORD = "input[name='password']"
               │    └─ All selector constants
               │
               └──→ Database (MySQL)
                    ├─ CREATE: vendor record
                    ├─ UPDATE: mobile_verified = 1
                    └─ SELECT: validate during login
```

---

## 🔄 Data Flow Diagram (Complete Journey)

```
PYTHON MEMORY                    BROWSER                      DATABASE
───────────────                  ───────                      ────────

User Dict ─────────────→ [Fill Form Fields] ───→ Submit ────→ vendor table
  ↓                               ↓                              ↓
Session                    [Signup Page HTML]          INSERT vendor()
_test_session                     ↓                              ↓
{                          [Mobile Verify Page]         User created
  "user": {...},                                    (mobile_verified=0)
  "cookies": [...]        ← ← ← ← ← ← ← ← ← ← ← ← ← ← ← ← ← ← 
}                                 ↓                              ↓
                          [Login Page HTML]      UPDATE mobile_verified=1
                                 ↓                              ↓
                          [Login Form Submit]                 Validated
                                 ↓                         (mobile_verified=1)
                          [Dashboard Page]                      ↓
                                 ↓                         Login successful
                          Store Cookies ────────→ Session in session.py
                                                        {
                                                         "user": {...},
                                                         "cookies": [...]
                                                        }
```

---

## 📝 What Each Folder Does (Summary)

```
configs/
├─ settings.py
│  └─ CONTAINS: Database credentials, base URL, passwords
│  └─ USED BY: db.py, conftest.py, all page objects
│  └─ DATA: DATABASE_CONFIG, BASE_URL, HARD_PASSWORD

src/core/
├─ base_page.py
│  └─ CONTAINS: Parent class for all pages
│  └─ PROVIDES: type(), click(), wait_for_element() methods
│  └─ USED BY: All page objects (SignupPage, LoginPage, etc.)

src/pages/authentication/
├─ signup_page.py
│  └─ CONTAINS: Form field selectors, signup() method
│  └─ DOES: Fills form & submits signup
│  └─ USES: Selectors from locators/
│
├─ login_page.py
│  └─ CONTAINS: Form field selectors, login() method
│  └─ DOES: Fills form & submits login
│  └─ USES: Selectors from locators/
│
└─ mobile_verification_page.py
   └─ CONTAINS: Mobile verification page selectors
   └─ DOES: Checks if mobile verify page appears

src/locators/
├─ authentication_locators.py
│  └─ CONTAINS: All CSS/XPath selectors
│  └─ USED BY: Page objects to find form fields
│  └─ DATA: EMAIL="input[name='email']", etc.

src/flows/
├─ authentication_flow.py
│  └─ CONTAINS: Multi-step flows (signup→verify→logout→login)
│  └─ ORCHESTRATES: Uses multiple page objects in sequence
│  └─ DOES: step_1_signup(), step_2_verify(), step_3_logout(), step_4_login()

src/utils/
├─ session.py
│  └─ CONTAINS: Global _test_session dictionary
│  └─ STORES: User data, cookies, logged-in state
│  └─ PROVIDES: create_fresh_test_user(), create_test_session(), get_test_user()
│
├─ db.py
│  └─ CONTAINS: Database functions
│  └─ DOES: get_db_connection(), user_exists(), update_mobile_verified(), delete_vendor()
│  └─ USES: configs/settings.py for DB credentials
│
└─ settings.py
   └─ (In configs folder - sees above)

tests/authentication/
├─ conftest.py
│  └─ SETUP: Opens browser, database connection
│  └─ TEARDOWN: Closes browser, cleans up
│  └─ PROVIDES: Browser fixture for all tests
│
├─ test_01_auth_e2e.py
│  └─ DOES: Complete signup→verify→logout→login flow
│  └─ CREATES: User in database
│  └─ STORES: User data + cookies in session
│
├─ test_02_signup_positive.py
│  └─ DOES: Test valid signup
│  └─ CREATES: New user (isolated, for this test)
│  └─ CLEANS: Deletes user after test
│
└─ test_04_login_positive.py
   └─ DOES: Test login with existing user
   └─ USES: User from session (created by test_01)
   └─ DEPENDS: Requires test_01 to run first
```

---

## 🎯 The Simple Truth

```
BEFORE TEST_01:
  ├─ Browser: OPEN
  ├─ Database: EMPTY (no test users)
  └─ Session: EMPTY

DURING TEST_01:
  ├─ Python creates unique user
  ├─ Stores user in session (Python memory)
  ├─ Browser fills form with user data
  ├─ Server creates user in database
  ├─ Test updates database (mobile_verified=1)
  ├─ Test logs out then logs in
  ├─ Browser now has session cookies

AFTER TEST_01:
  ├─ User in database: EXISTS with mobile_verified=1 ✅
  ├─ User data in session: STORED in _test_session ✅
  ├─ Browser cookies: STORED automatically ✅
  └─ Ready for test_04 to reuse this user

DURING TEST_04:
  ├─ Gets user from session (test_01's user)
  ├─ Uses SAME email & password
  ├─ Database check finds user (mobile_verified=1) ✅
  ├─ Login successful
  └─ Tests pass ✅
```

---

## 🚨 Important Points

```
1. FOLDER INTERACTION:
   Each folder has specific job:
   ├─ configs/ = Settings & credentials
   ├─ src/pages/ = What to click/fill (selectors)
   ├─ src/locators/ = Where to find elements (CSS/XPath)
   ├─ src/flows/ = How to do multi-step actions
   ├─ src/utils/ = Helper functions (DB, session)
   └─ tests/ = Run the actual tests

2. DATA FLOW:
   Python → Browser → Form → Server → Database
            ↓
   Browser Cookies ← Session Saved ← Python Memory

3. FOLDER COMMUNICATION:
   test_01 imports: session, pages, locators, db
   pages imports: core, locators
   db imports: configs/settings
   session imports: nothing (just Python)

4. DATA STORAGE LOCATIONS:
   ├─ Python Memory: User dict, session
   ├─ Browser: Form fields, cookies
   ├─ Database: vendor table record
   └─ Session File: Browser cookies (stored for reuse)

5. WHY TESTS MUST RUN IN ORDER:
   test_01 creates user + saves in session
   test_04 needs user from session
   If test_04 runs BEFORE test_01:
   ├─ get_test_user() returns NONE
   ├─ Login test fails
   └─ Error!
```

---

## ✅ Summary For Your Team

Show them this simple flow:

```
TEST STARTS:
│
├─ Python creates unique user (auto_xxx@gmail.in)
├─ Stores it in memory (session.py global)
│
├─ Browser opens signup page
├─ Fills form with user data
├─ Submits form to server
│
├─ Server creates user in database
├─ Test updates database (simulates OTP)
│
├─ Browser logs out
├─ Browser logs in with same email/password
├─ Database validates all checks pass
│
├─ Browser now has session cookie
├─ Stores everything in session (Python memory)
│
└─ TEST COMPLETE
   ├─ User in database ✅
   ├─ User in session ✅
   └─ Cookies saved ✅

NEXT TEST (test_04):
│
├─ Gets user from session (test_01's user)
├─ Uses same email & password
├─ Login works because mobile_verified=1 ✅
│
└─ TEST PASSES ✅
```

---

**This is the complete data journey! Every folder interaction, every data transformation, everything explained simply.** 🚀
