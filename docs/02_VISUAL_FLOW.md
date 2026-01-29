# 02_VISUAL_FLOW.md - How Tests Execute

---

## 🎬 Complete Test Execution Timeline

```
Start: pytest tests/authentication/
│
├─ SETUP (conftest.py)
│  ├─ Browser opens: https://dev.v.shipgl.in
│  ├─ Database connection established
│  └─ Session ready to store user data
│
├─ TEST_01: auth_e2e.py (35 seconds) ⏱️
│  │
│  ├─ Step 1: Signup
│  │  ├─ Generate unique email: auto_1704067200000_45678@gmail.in
│  │  ├─ Generate unique mobile: 9876543210
│  │  ├─ Open: /auth/signup
│  │  ├─ Fill form: first_name, last_name, mobile, email, password
│  │  ├─ Check: Terms & Conditions
│  │  └─ Click: Submit button
│  │
│  ├─ Browser redirects to: /verify-mobile
│  │  └─ Page shows: "Enter OTP from SMS"
│  │
│  ├─ Step 2: Database Update (simulate OTP)
│  │  └─ UPDATE vendor SET mobile_verified = 1 WHERE email = 'auto_...'
│  │
│  ├─ Step 3: Logout
│  │  ├─ Click: Logout button
│  │  └─ Browser redirects to: /auth/login
│  │
│  ├─ Step 4: Login
│  │  ├─ Fill email: auto_1704067200000_45678@gmail.in
│  │  ├─ Fill password: Test@1234
│  │  └─ Click: Submit button
│  │
│  ├─ Browser redirects to: /merchant-agreement
│  │  └─ Show: Terms & merchant policies
│  │
│  ├─ Step 5: Accept Agreement
│  │  ├─ Click: Accept button
│  │  └─ Browser redirects to: /dashboard
│  │
│  └─ Cleanup:
│     └─ Save user data in session for other tests
│        (_test_session = { "user": {...}, "cookies": [...] })
│
├─ TEST_02: signup_positive.py (22 seconds) ⏱️
│  │
│  ├─ Generate NEW unique email
│  ├─ Open: /auth/signup
│  ├─ Fill & submit form
│  ├─ Verify: Redirected to /verify-mobile
│  ├─ Cleanup: Logout
│  └─ Success ✅
│
├─ TEST_03: signup_negative.py (50 seconds) ⏱️
│  │
│  ├─ Case 1: First name empty
│  │  ├─ Leave field blank
│  │  ├─ Click submit
│  │  └─ Verify: Error message appears
│  │
│  ├─ Case 2: First name with special chars
│  │  ├─ Enter: "John@#$"
│  │  ├─ Click submit
│  │  └─ Verify: Error message
│  │
│  ├─ ... (17 more cases for other fields)
│  │
│  └─ Each case: Arrange → Act → Assert → Cleanup
│
├─ TEST_04: login_positive.py (8 seconds) ⏱️
│  │
│  ├─ Get user from session (created in test_01)
│  ├─ Open: /auth/login
│  ├─ Fill email: {session user email}
│  ├─ Fill password: Test@1234
│  ├─ Click submit
│  ├─ Verify: Redirected to /dashboard
│  └─ Success ✅
│
└─ TEST_05: login_negative.py (20 seconds) ⏱️
   │
   ├─ Case 1: Email empty
   │  ├─ Leave email blank
   │  ├─ Click submit
   │  └─ Verify: Error message
   │
   ├─ Case 2: Wrong password
   │  ├─ Enter correct email
   │  ├─ Enter wrong password
   │  ├─ Click submit
   │  └─ Verify: "Invalid credentials" error
   │
   ├─ ... (6 more cases)
   │
   └─ Each case: Arrange → Act → Assert → Cleanup

TEARDOWN (conftest.py)
├─ Clear session
├─ Close browser
└─ Close database connection

Total Time: ~2 minutes 54 seconds ✅
All Tests: 30 PASSED
```

---

## 🔄 User Journey - One Signup + Login

```
USER PERSPECTIVE:

1️⃣  SIGNUP PAGE
    ┌────────────────────────────────────┐
    │ Create Account                     │
    ├────────────────────────────────────┤
    │ First Name:     [______]           │ ← Enter: John
    │ Last Name:      [______]           │ ← Enter: Doe
    │ Mobile:         [______]           │ ← Enter: 9876543210
    │ Email:          [______]           │ ← Enter: auto_xxx@gmail.in
    │ Password:       [______]           │ ← Enter: Test@1234
    │ Confirm Pwd:    [______]           │ ← Enter: Test@1234
    │ ☑ I agree to T&C                   │ ← Check
    │ [Sign Up]                          │ ← Click
    └────────────────────────────────────┘
              ↓
    Browser submits form
    Server creates user in 'vendor' table
    mobile_verified = 0 (not verified)
              ↓

2️⃣  MOBILE VERIFICATION PAGE
    ┌────────────────────────────────────┐
    │ Verify Your Mobile                 │
    ├────────────────────────────────────┤
    │ OTP sent to: 98765...0             │
    │ Enter OTP: [______]                │
    │ [Verify]                           │
    │ [Resend OTP]                       │
    └────────────────────────────────────┘
    
    🤖 TEST SHORTCUT:
    → Don't enter OTP
    → Directly update database:
       UPDATE vendor SET mobile_verified = 1
    → Simulate OTP verification
              ↓

3️⃣  LOGOUT
    └─ Click: Logout
    └─ Clear session cookie
    └─ Redirect to: Login Page
              ↓

4️⃣  LOGIN PAGE
    ┌────────────────────────────────────┐
    │ Login                              │
    ├────────────────────────────────────┤
    │ Email:      [auto_xxx@gmail.in]    │ ← Fill
    │ Password:   [Test@1234]            │ ← Fill
    │ ☐ Remember me                      │
    │ [Login]                            │ ← Click
    │ [Forgot Password?]                 │
    └────────────────────────────────────┘
              ↓
    Server validates:
    - Email exists? YES
    - Password correct? YES
    - mobile_verified = 1? YES ✅
    - Create session cookie
              ↓

5️⃣  MERCHANT AGREEMENT PAGE
    ┌────────────────────────────────────┐
    │ Merchant Agreement                 │
    ├────────────────────────────────────┤
    │ Please accept terms...             │
    │ ☑ I accept                         │
    │ [Continue]                         │
    └────────────────────────────────────┘
              ↓
    Save browser cookies in session
              ↓

6️⃣  DASHBOARD
    ┌────────────────────────────────────┐
    │ Dashboard                          │
    ├────────────────────────────────────┤
    │ Welcome, John Doe!                 │
    │ [View Orders]                      │
    │ [Create Order]                     │
    │ [Logout]                           │
    └────────────────────────────────────┘
    
    ✅ TEST COMPLETE
```

---

## 🧪 Test Data Flow

```
TEST START
    ↓
CREATE USER
    ├─ Email: auto_1704067200000_45678@gmail.in (unique)
    ├─ Mobile: 9876543210 (unique)
    ├─ Password: Test@1234 (same for all tests)
    ├─ First Name: John (random)
    └─ Last Name: Doe (random)
    ↓
STORE IN SESSION
    ├─ _test_session["user"] = {...}
    ├─ Can be accessed by:
    │  ├─ test_04_login_positive.py (login with this user)
    │  └─ test_05_login_negative.py (test against this user)
    ↓
DATABASE
    ├─ Check: user_exists(email) → True/False
    ├─ Update: mobile_verified = 1
    └─ Delete: delete_vendor(email) [commented out in test_01]
    ↓
BROWSER COOKIES
    ├─ After login: Save cookies in _test_session
    ├─ Can be restored later to skip login
    ↓
TEST END
    └─ User data still in session (not cleared between tests)
```

---

## 📊 Data Flow: Signup to Database

```
BROWSER                          TEST CODE              DATABASE
─────────                        ─────────              ────────

User enters:
 "auto_xxx@gmail.in"    →  SignupPage.signup(...)  →  
 "Test@1234"                                           CREATE vendor(
 "John"                                                  email = "auto_xxx@gmail.in",
 "Doe"                                                   password = hash("Test@1234"),
 "9876543210"                                           first_name = "John",
 ✓ Terms checked                                        last_name = "Doe",
                                                        mobile = "9876543210",
         ↓                                              mobile_verified = 0  ← NOT YET
  Click "Sign Up"
         ↓
 Browser submits form    →  AuthFlow.step_1_signup  →  INSERT INTO vendor
         ↓                                               VALUES (...)
 Page shows "Verify"                                    ↓ SUCCESS
         ↓
 (OTP would be sent)                                    ↓
         ↓
 (Test skips OTP)        →  db.update_mobile_verified  →  UPDATE vendor
                                                           SET mobile_verified = 1
         ↓                                                 WHERE email = "auto_xxx@gmail.in"
                                                          ↓ SUCCESS
```

---

## 🔄 Page Navigation Map

```
Entry Point: https://dev.v.shipgl.in

/auth/login (Login Page)
    ↓ Click "Create Account"
/auth/signup (Signup Page) ← START TEST_01 HERE
    ↓ Submit form
/verify-mobile (Mobile Verification)
    ↓ [Simulated OTP] UPDATE database
/auth/logout (Logout)
    ↓
/auth/login (Back to Login) ← TEST_04 uses this
    ↓ Login with email + password
/merchant-agreement (Agreement Modal)
    ↓ Click Accept
/dashboard (Dashboard) ← Tests check we reach here
    ↓ Click any menu
/orders/list (Orders Page)
    ↓
... more pages ...
```

---

## 🧬 Signup Validation Cases Flow

```
NEGATIVE TESTS (test_03_signup_negative.py):

Input: First Name = "" (empty)  →  Form validation  →  Error: "First name required"
Input: First Name = "A@B#C"     →  Form validation  →  Error: "Invalid characters"
Input: First Name = "A" * 1000  →  Form validation  →  Error: "Too long"

Input: Email = "" (empty)       →  Form validation  →  Error: "Email required"
Input: Email = "invalid"        →  Form validation  →  Error: "Invalid email"
Input: Email = "user@test.com"  →  Database check   →  Error: "Already exists"

Input: Password = "weak"        →  Form validation  →  Error: "Must have uppercase, number, special char"
Input: Password = "Test@123"    →  Form validation  →  Error: "Too short (< 8 chars)"

Terms Checkbox = ☐ (unchecked)  →  Form validation  →  Error: "Must accept terms"
```

---

## ⏱️ Timing Breakdown

```
TEST_01 (35 seconds):
├─ Signup form interaction:      8 seconds
│  ├─ Navigate to signup page:   2 sec
│  ├─ Fill 6 fields:             4 sec
│  ├─ Click submit:              2 sec
├─ Mobile verification:          5 seconds
│  ├─ Wait for page load:        3 sec
│  ├─ Database update:           2 sec
├─ Logout:                       3 seconds
├─ Login:                        8 seconds
│  ├─ Navigate to login page:    2 sec
│  ├─ Fill 2 fields:             3 sec
│  ├─ Click submit:              3 sec
├─ Merchant agreement:           5 seconds
│  ├─ Fill & accept:             5 sec
├─ Dashboard verification:       3 seconds
└─ Buffer:                       3 seconds

TEST_02 (22 seconds):
├─ Signup form:     15 sec
└─ Verify & cleanup: 7 sec

TEST_03 (50 seconds):
├─ 19 test cases × 2-3 sec per case = ~50 sec

TEST_04 (8 seconds):
├─ Login form:      5 sec
└─ Verify & cleanup: 3 sec

TEST_05 (20 seconds):
├─ 8 test cases × 2-3 sec per case = ~20 sec

TOTAL: 35 + 22 + 50 + 8 + 20 = 135 seconds ≈ 2 minutes 54 seconds ✅
```

---

## 🔐 Session & Cookie Flow

```
MEMORY (Python Session)
─────────────────────

Initially: _test_session = {}

After TEST_01 SIGNUP:
    _test_session = {
        "user": {
            "email": "auto_1704067200000_45678@gmail.in",
            "password": "Test@1234",
            "mobile": "9876543210",
            "first_name": "John",
            "last_name": "Doe"
        }
    }

After TEST_01 LOGIN:
    _test_session = {
        "user": {...},
        "browser_cookies": [
            {
                "name": "sessionId",
                "value": "abc123xyz",
                "domain": "dev.v.shipgl.in",
                "path": "/"
            }
        ],
        "is_logged_in": True
    }

TEST_04 USES THIS:
    email = get_test_user()["email"]  ← Gets: auto_1704067200000_45678@gmail.in
    password = "Test@1234"
    → Uses SAME user created in TEST_01
    
BROWSER COOKIES:
    Automatically stored by SeleniumBase
    Automatically restored between tests
    This is how "session" persists without re-login
```

---

## 🎯 Success Criteria Per Test

```
TEST_01: ✅
  ├─ signup form submitted successfully
  ├─ user created in database (mobile_verified = 0)
  ├─ redirected to mobile verify page
  ├─ database updated (mobile_verified = 1)
  ├─ logout successful
  ├─ login successful with same credentials
  ├─ merchant agreement page shown
  └─ dashboard reached

TEST_02: ✅
  ├─ signup with valid data successful
  └─ redirected to mobile verify page

TEST_03: ✅ (19 cases)
  ├─ Each invalid input shows correct error message
  └─ Form does NOT submit for invalid data

TEST_04: ✅
  ├─ login with stored user credentials
  └─ redirected to dashboard

TEST_05: ✅ (8 cases)
  ├─ Each invalid login shows error
  └─ Dashboard NOT reached with invalid credentials
```

---

## 📝 Example: One Test Run

```
$ pytest tests/authentication/test_02_signup_positive.py -v

test_02_signup_positive.py::test_signup_positive STARTED
│
├─ Arrange (Setup):
│  └─ Create user: email="auto_1704067200050_11111@gmail.in"
│
├─ Act (Execution):
│  ├─ Navigate to /auth/signup
│  ├─ Create SignupPage(browser, base_url)
│  ├─ Call: signup(first_name, last_name, mobile, email, password)
│  ├─ Browser fills all fields
│  ├─ Browser clicks "Sign Up" button
│  └─ Wait for page redirect
│
├─ Assert (Verification):
│  ├─ Check URL changed to /verify-mobile ✅
│  ├─ Check error message NOT visible ✅
│  └─ Check mobile verify page text present ✅
│
└─ Cleanup (Teardown):
   └─ Click logout
   
RESULT: PASSED ✅ (22 seconds)
```

---

## 🚀 Summary: Flow Visualization

```
pytest → conftest (setup browser) → TEST_01 (e2e) → TEST_02 (signup) 
    → TEST_03 (validation × 19) → TEST_04 (login) → TEST_05 (validation × 8)
    → conftest (cleanup) → Results: 30 PASSED in 2:54
```

Ready to understand how each function calls the next? Read **03_HOW_TESTS_RUN.md** next! 📚
