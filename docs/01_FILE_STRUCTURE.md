# 01_FILE_STRUCTURE.md - What Each File Does

---

## 📁 Project Structure (Complete Map)

```
Full-Stack-Test-Automation-Framework/
│
├── configs/                          ← Configuration files
│   ├── settings.py                   ← Database, base URL, passwords
│   └── test_accounts.json            ← Test user data
│
├── src/                              ← Main application code
│   ├── __init__.py
│   │
│   ├── core/                         ← Base classes
│   │   └── base_page.py              ← Parent class for all page objects
│   │
│   ├── pages/                        ← WHERE to interact (Selectors)
│   │   ├── authentication/
│   │   │   ├── login_page.py         ← Login form (email, password fields)
│   │   │   ├── signup_page.py        ← Signup form (name, email, password fields)
│   │   │   ├── mobile_verification_page.py  ← Mobile OTP page
│   │   │   └── legal_consent_modal.py       ← Terms & conditions modal
│   │   │
│   │   ├── dashboard/
│   │   │   └── dashboard_page.py     ← Dashboard page after login
│   │   │
│   │   └── orders/
│   │       ├── order_list_page.py    ← List of all orders
│   │       └── order_add/
│   │           ├── shipment_information_page.py
│   │           ├── consignee_details_page.py
│   │           ├── select_shipping_partner_page.py
│   │           └── order_payment_page.py
│   │
│   ├── locators/                     ← CSS/XPath selectors
│   │   ├── authentication_locators.py    ← Selectors for login/signup/mobile verify
│   │   ├── orders_locators.py            ← Selectors for order pages
│   │   └── multibox_locators.py
│   │
│   ├── flows/                        ← HOW to interact (Sequences/Orchestration)
│   │   └── authentication_flow.py    ← Multi-step signup/login/logout sequence
│   │
│   └── utils/                        ← Helper functions
│       ├── db.py                     ← Database operations
│       └── session.py                ← Test user session & cookies
│
├── tests/                            ← All test files
│   ├── conftest.py                   ← pytest fixtures (browser, database)
│   │
│   └── authentication/               ← Authentication tests
│       ├── test_01_auth_e2e.py       ← Complete signup → verify → logout → login flow
│       ├── test_02_signup_positive.py    ← Valid signup tests
│       ├── test_03_signup_negative.py    ← Invalid signup tests (validation)
│       ├── test_04_login_positive.py     ← Valid login tests
│       └── test_05_login_negative.py     ← Invalid login tests (validation)
│
├── docs/                             ← Documentation
│   └── This folder with all .md files
│
├── pytest.ini                        ← pytest configuration
├── pyproject.toml                    ← Project metadata
├── requirements.txt                  ← Python package dependencies
└── README.md                         ← Root level info
```

---

## 🔧 File-by-File Explanation

### **configs/settings.py** 📋
```
PURPOSE: Store all configuration in one place

CONTAINS:
- DATABASE_CONFIG: MySQL connection (host, user, password, database)
- BASE_URL: https://dev.v.shipgl.in
- HARD_PASSWORD: Test@1234 (used in all tests)
- LOG_LEVEL: INFO

USAGE:
  from configs.settings import DATABASE_CONFIG, BASE_URL
  
  db_connection = mysql.connector.connect(**DATABASE_CONFIG)
  self.sb.open(BASE_URL)
```

---

### **src/core/base_page.py** 🏗️
```
PURPOSE: Parent class for all page objects

PROVIDES:
- self.sb = SeleniumBase browser instance
- self.base_url = website URL
- Common methods:
  - wait_for_element(selector) → Waits max 10 seconds
  - is_element_present(selector) → True/False
  - click(selector)
  - type(selector, text)

EXAMPLE USAGE:
  class LoginPage(BasePage):
      def login(self, email, password):
          self.type(self.EMAIL, email)
          self.type(self.PASSWORD, password)
          self.click(self.SUBMIT_BUTTON)
```

---

### **src/pages/authentication/login_page.py** 🔐
```
PURPOSE: Represent the login form on the website

CLASS: LoginPage(BasePage)

SELECTORS (what to interact with):
  EMAIL = "input[name='email']"          ← Email input field
  PASSWORD = "input[name='password']"    ← Password input field
  SUBMIT = "button[type='submit']"       ← Submit button
  ERROR_MESSAGE = ".error"               ← Error message (shows if login fails)

METHODS (what to do):
  login(email, password)
    → Fills email field
    → Fills password field
    → Clicks submit button

EXAMPLE:
  page = LoginPage(sb, base_url)
  page.login("user@gmail.in", "Test@1234")
  page.wait_for_element(page.SUBMIT)  ← Wait until submit is clickable
```

---

### **src/pages/authentication/signup_page.py** 📝
```
PURPOSE: Represent the signup form on the website

CLASS: SignupPage(BasePage)

SELECTORS:
  FIRST_NAME = "input[name='firstName']"
  LAST_NAME = "input[name='lastName']"
  MOBILE = "input[name='mobile']"
  EMAIL = "input[name='email']"
  PASSWORD = "input[name='password']"
  CONFIRM_PASSWORD = "input[name='confirmPassword']"
  TERMS_CHECKBOX = "input[type='checkbox']"
  SUBMIT = "button[type='submit']"

METHODS:
  signup(first_name, last_name, mobile, email, password)
    → Fills all fields
    → Checks terms checkbox
    → Clicks submit button

EXAMPLE:
  page = SignupPage(sb, base_url)
  page.signup(
      first_name="John",
      last_name="Doe",
      mobile="9876543210",
      email="auto_123456@gmail.in",
      password="Test@1234"
  )
```

---

### **src/pages/authentication/mobile_verification_page.py** 📱
```
PURPOSE: Represent the mobile OTP verification page

CLASS: MobileVerificationPage(BasePage)

SELECTORS:
  OTP_FIELD = "input[name='otp']"
  VERIFY_BUTTON = "button[text='Verify']"
  RESEND_LINK = "a[text='Resend OTP']"

METHODS:
  verify_mobile()
    → This page auto-verifies (we update DB instead of entering OTP)
    → Just checks if mobile verify page appears
```

---

### **src/locators/authentication_locators.py** 🎯
```
PURPOSE: Store all CSS/XPath selectors in one place

CONTAINS:
  class LoginPageLocators:
      EMAIL = "input[name='email']"
      PASSWORD = "input[name='password']"
      ...

  class SignupPageLocators:
      FIRST_NAME = "input[name='firstName']"
      ...

USAGE:
  Instead of hardcoding selectors in page classes,
  import them from locators:
  
  from src.locators.authentication_locators import SignupPageLocators
  self.EMAIL = SignupPageLocators.EMAIL
```

---

### **src/flows/authentication_flow.py** 🔄
```
PURPOSE: Orchestrate multi-step authentication sequences

CLASS: AuthenticationFlow

METHODS:
  step_1_signup(user)
    → Navigate to signup page
    → Create SignupPage object
    → Call signup() with user data
    → Wait for redirect to mobile verify page

  step_2_verify_mobile()
    → Update database: mobile_verified = 1
    → Simulate OTP verification
    
  step_3_logout()
    → Click logout button
    → Wait for redirect to login page

  step_4_login(email, password)
    → Navigate to login page
    → Create LoginPage object
    → Call login() with credentials
    → Wait for redirect to dashboard

  step_5_merchant_agreement()
    → Fill merchant agreement form (if needed)

EXAMPLE:
  flow = AuthenticationFlow(sb)
  
  user = {
      "email": "auto_123456@gmail.in",
      "password": "Test@1234",
      "mobile": "9876543210"
  }
  
  flow.step_1_signup(user)  # Signup
  flow.step_2_verify_mobile()  # Verify OTP
  flow.step_3_logout()  # Logout
  flow.step_4_login(user["email"], user["password"])  # Login again
```

---

### **src/utils/db.py** 🗄️
```
PURPOSE: Handle database operations (read/write/delete)

FUNCTIONS:

  get_db_connection()
    → Opens MySQL connection
    → Returns: Connection object

  user_exists(email)
    → Checks if user exists in 'vendor' table
    → Returns: True/False

  update_mobile_verified(email)
    → UPDATE vendor SET mobile_verified = 1 WHERE email = email
    → Simulates OTP verification
    → Returns: Number of rows updated

  delete_vendor(email)
    → DELETE FROM vendor WHERE email = email
    → Cleans up test user
    → Returns: Number of rows deleted

EXAMPLE:
  from src.utils.db import user_exists, update_mobile_verified
  
  if user_exists("auto_123456@gmail.in"):
      print("User already exists")
  else:
      print("User is new")
  
  rows_updated = update_mobile_verified("auto_123456@gmail.in")
  print(f"Updated {rows_updated} row(s)")
```

---

### **src/utils/session.py** 💾
```
PURPOSE: Store test user data and browser cookies across tests

GLOBAL VARIABLE:
  _test_session = {}  ← Stores data between tests

FUNCTIONS:

  create_fresh_test_user()
    → Generates unique email: auto_{timestamp}_{random}@gmail.in
    → Generates unique mobile: 9{9 random digits}
    → Generates password: Test@1234
    → Returns: Dictionary with email, mobile, password, first_name, last_name

  create_test_session(user_data)
    → Stores user data in _test_session["user"]
    → Also stores browser cookies for later use

  get_test_user()
    → Retrieves stored user data
    → Returns: Dictionary with email, mobile, password, etc.

  cleanup_test_session()
    → Clears _test_session after all tests

EXAMPLE:
  from src.utils.session import create_fresh_test_user, create_test_session
  
  # Generate unique user
  user = create_fresh_test_user()
  print(user["email"])  # auto_1704067200000_45678@gmail.in
  
  # Store for later use
  create_test_session(user)
  
  # Later, retrieve same user
  same_user = get_test_user()
  print(same_user["email"])  # Same as above
```

---

### **tests/conftest.py** 🔌
```
PURPOSE: Setup and teardown for all tests (pytest fixtures)

FIXTURES:

  @pytest.fixture(scope="session")
  def sb()
    → Initializes SeleniumBase browser (opens once)
    → Opens https://dev.v.shipgl.in
    → Yields browser to all tests
    → Closes browser after all tests (teardown)

  @pytest.fixture(autouse=True)
  def setup_teardown()
    → Runs before each test
    → Runs after each test
    → Used for cleanup between tests

EXAMPLE:
  def test_example(sb):
      # sb is the browser instance
      sb.open("https://...")
      sb.click("button")
      assert sb.is_text_visible("Success")
```

---

### **tests/authentication/test_01_auth_e2e.py** 🎯
```
PURPOSE: Complete end-to-end authentication flow

TEST FLOW:
  1. Generate fresh test user (unique email, mobile)
  2. Open signup page
  3. Fill form with user data
  4. Submit form
  5. Update database (mobile_verified = 1)
  6. Logout
  7. Login with same credentials
  8. Accept merchant agreement
  9. Verify we're on dashboard
  10. (Note: delete_vendor() commented out to keep user in DB)

DURATION: ~35 seconds

WHAT IT TESTS:
  ✅ Signup form works
  ✅ User created in database
  ✅ Database can be updated
  ✅ Login form works
  ✅ Logout works
  ✅ Session persists across logout/login

EXAMPLE OUTPUT:
  test_01_auth_e2e.py::test_auth_flow PASSED
```

---

### **tests/authentication/test_02_signup_positive.py** ✅
```
PURPOSE: Test valid signup scenarios

WHAT IT TESTS:
  ✅ Valid signup with correct data
  ✅ User created in database

TEST STRUCTURE:
  TEST_CASES = {
      "valid_signup": {
          "data": {...},
          "expected": "redirect to mobile verify"
      }
  }

DURATION: ~22 seconds
```

---

### **tests/authentication/test_03_signup_negative.py** ❌
```
PURPOSE: Test signup form validation (19 error cases)

ORGANIZED BY:
  - FIRST_NAME_CASES: Empty, too long, special chars
  - LAST_NAME_CASES: Empty, too long, special chars
  - MOBILE_CASES: Invalid format, too short, too long
  - EMAIL_CASES: Invalid format, already exists
  - PASSWORD_CASES: Too weak, no uppercase, no number
  - TOC_CASES: Terms not checked

USES: @pytest.mark.parametrize
  → Runs each case separately
  → Shows which case failed (if any)

DURATION: ~50 seconds (19 test cases)
```

---

### **tests/authentication/test_04_login_positive.py** ✅
```
PURPOSE: Test valid login scenarios

WHAT IT TESTS:
  ✅ Login with correct email + password
  ✅ Redirects to dashboard
  ✅ Uses user from session (created in test_01)

TEST STRUCTURE:
  TEST_CASES = {
      "valid_login": {
          "email": "{user from session}",
          "password": "Test@1234",
          "expected": "redirect to dashboard"
      }
  }

DURATION: ~8 seconds
```

---

### **tests/authentication/test_05_login_negative.py** ❌
```
PURPOSE: Test login form validation (8 error cases)

ORGANIZED BY:
  - EMAIL_CASES: Empty, invalid format, wrong email
  - PASSWORD_CASES: Empty, wrong password
  - BOTH_INVALID_CASES: Both email and password wrong

USES: @pytest.mark.parametrize

DURATION: ~20 seconds
```

---

## 🔗 How Files Work Together

```
┌─────────────────────────────────────────────────────────┐
│ test_01_auth_e2e.py (test file)                         │
└──────────────────┬──────────────────────────────────────┘
                   │ imports
                   ↓
┌─────────────────────────────────────────────────────────┐
│ src/flows/authentication_flow.py                        │
│ (orchestrates steps: signup → verify → logout → login)  │
└──────────────────┬──────────────────────────────────────┘
                   │ uses
                   ↓
     ┌─────────────────────────────────────┐
     │                                     │
     ↓                                     ↓
src/pages/                          src/utils/
authentication/                     ├─ session.py (store user)
├─ signup_page.py                   └─ db.py (verify in DB)
├─ login_page.py
└─ mobile_verification_page.py

     ↓ get selectors from
     
src/locators/
└─ authentication_locators.py

     ↓ inherit from

src/core/
└─ base_page.py (common methods)
```

---

## 📊 File Sizes & Complexity

```
Simple (< 100 lines):
  ✅ mobile_verification_page.py
  ✅ session.py
  ✅ settings.py

Medium (100-300 lines):
  ✅ signup_page.py
  ✅ login_page.py
  ✅ authentication_locators.py
  ✅ db.py

Complex (300+ lines):
  ✅ authentication_flow.py (~200 lines but orchestrates many steps)
  ✅ test files (parametrized with multiple cases)
```

---

## 🎯 Summary

**Page Objects** (WHERE to interact)
- Define form fields, buttons, etc.
- One file per page

**Flows** (HOW to interact)
- Multi-step sequences
- Use page objects to perform actions

**Locators** (WHAT selectors to use)
- Store CSS/XPath in one place
- Used by page objects

**Utils** (Helper functions)
- Database: Create, update, delete
- Session: Remember user data & cookies

**Tests** (RUN the flows)
- Import flows
- Pass test data
- Assert expected results

Ready to see how they work together? Read **02_VISUAL_FLOW.md** next! 📚
