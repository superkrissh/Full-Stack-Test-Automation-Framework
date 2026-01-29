# 03_HOW_TESTS_RUN.md - Step-by-Step Execution Guide

---

## 🚀 Running Tests Command

```bash
# Run ALL authentication tests
./venv/bin/python -m pytest tests/authentication/ -v

# Run ONE specific test
./venv/bin/python -m pytest tests/authentication/test_01_auth_e2e.py -v

# Run with more details
./venv/bin/python -m pytest tests/authentication/ -vv -s
```

---

## 📖 What Happens Step by Step

### STEP 0: Python Loads Everything

```
1. pytest reads: pytest.ini
   └─ Sets testing options

2. pytest reads: conftest.py
   └─ Defines fixtures (browser setup, database connection)

3. pytest reads all test files:
   ├─ test_01_auth_e2e.py
   ├─ test_02_signup_positive.py
   ├─ test_03_signup_negative.py
   ├─ test_04_login_positive.py
   └─ test_05_login_negative.py

4. pytest analyzes tests:
   ├─ test_01: 1 test function
   ├─ test_02: 1 test function
   ├─ test_03: 19 test cases (parametrized) = 19 individual tests
   ├─ test_04: 1 test function
   └─ test_05: 8 test cases (parametrized) = 8 individual tests
   
   TOTAL: 1 + 1 + 19 + 1 + 8 = 30 tests
```

---

### STEP 1: Setup - conftest.py Runs

```python
# conftest.py - Runs ONCE at the beginning

@pytest.fixture(scope="session")
def sb():
    """Browser fixture - scope='session' means opened ONCE"""
    
    # ACTION 1: Initialize SeleniumBase
    sb = SB()
    
    # ACTION 2: Open website
    sb.open("https://dev.v.shipgl.in")
    
    # ACTION 3: Print version info
    print("Browser opened, ready for tests")
    
    # Yield browser to all tests (they all use SAME browser)
    yield sb
    
    # AFTER ALL TESTS: Close browser
    sb.quit()
    print("Browser closed")

# RESULT:
# ✅ One browser instance created
# ✅ Browser stays open through all 30 tests
# ✅ Browser closed after all tests finish
```

---

### STEP 2: TEST_01 Runs - Complete Auth Flow

```python
# tests/authentication/test_01_auth_e2e.py

def test_auth_flow(sb):
    """Complete signup → verify → logout → login flow"""
    
    # ======================
    # PART 1: ARRANGE (Setup)
    # ======================
    print("Starting test_01...")
    
    # Generate fresh unique user
    user = create_fresh_test_user()
    print(f"Created user: {user['email']}")
    # OUTPUT: Created user: auto_1704067200000_45678@gmail.in
    
    # Store user data for other tests
    create_test_session(user)
    # Now other tests can use: get_test_user()
    
    # Get database connection
    email = user['email']
    
    # ======================
    # PART 2: ACT (Execute)
    # ======================
    
    # SECTION A: Signup
    print("Opening signup page...")
    sb.open("https://dev.v.shipgl.in/auth/signup")
    
    # Create SignupPage object
    signup_page = SignupPage(sb, "https://dev.v.shipgl.in")
    
    # Call signup method - it does:
    # - Type first_name field
    # - Type last_name field
    # - Type mobile field
    # - Type email field
    # - Type password field
    # - Type confirm password
    # - Check terms checkbox
    # - Click Submit button
    signup_page.signup(
        first_name=user['first_name'],  # "John"
        last_name=user['last_name'],    # "Doe"
        mobile=user['mobile'],           # "9876543210"
        email=user['email'],             # "auto_xxx@gmail.in"
        password=user['password']        # "Test@1234"
    )
    print("Signup form submitted")
    
    # Wait for page redirect
    sb.wait_for_element("selector for mobile verify page")
    print("Redirected to mobile verify page")
    
    # SECTION B: Mobile Verification
    print("Updating database to simulate OTP verification...")
    rows_updated = update_mobile_verified(email)
    print(f"Updated {rows_updated} row(s)")
    # DATABASE: UPDATE vendor SET mobile_verified = 1 WHERE email = "auto_xxx@gmail.in"
    
    # SECTION C: Logout
    print("Logging out...")
    sb.click("logout button selector")
    sb.wait_for_element("login page selector")
    print("Successfully logged out")
    
    # SECTION D: Login Again
    print("Logging back in...")
    sb.open("https://dev.v.shipgl.in/auth/login")
    
    login_page = LoginPage(sb, "https://dev.v.shipgl.in")
    login_page.login(
        email=email,             # "auto_xxx@gmail.in"
        password=user['password']  # "Test@1234"
    )
    print("Login form submitted")
    
    # Wait for redirect
    sb.wait_for_element("merchant agreement page selector")
    print("Redirected to merchant agreement")
    
    # SECTION E: Accept Merchant Agreement
    print("Accepting merchant agreement...")
    sb.click("agree checkbox")
    sb.click("continue button")
    sb.wait_for_element("dashboard selector")
    print("Redirected to dashboard")
    
    # ======================
    # PART 3: ASSERT (Verify)
    # ======================
    
    # Check 1: Are we on dashboard?
    assert sb.is_element_visible("dashboard header")
    print("✅ Assertion 1 passed: Dashboard visible")
    
    # Check 2: Does database record exist?
    assert user_exists(email)
    print("✅ Assertion 2 passed: User exists in database")
    
    # Check 3: Is mobile_verified = 1?
    # (Not directly checked in test, but we updated it)
    
    # ======================
    # PART 4: CLEANUP
    # ======================
    
    print("Test 1 complete, NOT deleting user (keeping for verification)")
    # Note: delete_vendor(email) is COMMENTED OUT
    # User stays in database with mobile_verified = 1
    
    # Session now contains:
    # _test_session = {
    #     "user": {...},
    #     "browser_cookies": [...]
    # }

# RESULT: ✅ PASSED (35 seconds)
```

---

### STEP 3: TEST_02 Runs - Valid Signup

```python
# tests/authentication/test_02_signup_positive.py

def test_signup_positive(sb):
    """Test valid signup"""
    
    # ARRANGE
    user = create_fresh_test_user()
    # New unique user: auto_1704067200050_11111@gmail.in
    
    # ACT
    sb.open("https://dev.v.shipgl.in/auth/signup")
    signup_page = SignupPage(sb, "https://dev.v.shipgl.in")
    
    signup_page.signup(
        first_name=user['first_name'],
        last_name=user['last_name'],
        mobile=user['mobile'],
        email=user['email'],
        password=user['password']
    )
    
    # Wait for redirect to mobile verify
    sb.wait_for_element("mobile verify page selector")
    
    # ASSERT
    assert sb.is_element_visible("mobile verify page header")
    print("✅ Signup successful, redirected to mobile verify")
    
    # CLEANUP
    sb.click("logout button")
    # Clear database
    delete_vendor(user['email'])

# RESULT: ✅ PASSED (22 seconds)
```

---

### STEP 4: TEST_03 Runs - Signup Validation (19 cases)

```python
# tests/authentication/test_03_signup_negative.py

# Using @pytest.mark.parametrize, this runs 19 SEPARATE tests

# Example: FIRST_NAME validation cases
@pytest.mark.parametrize("test_data", [
    {
        "name": "empty_first_name",
        "first_name": "",  # Invalid!
        "last_name": "Doe",
        "mobile": "9876543210",
        "email": "auto_xxx@gmail.in",
        "password": "Test@1234",
        "expected_error": "First name is required"
    },
    {
        "name": "special_chars_first_name",
        "first_name": "John@#$",  # Invalid!
        "last_name": "Doe",
        ...
        "expected_error": "Special characters not allowed"
    },
    # ... 17 more cases for other fields
])
def test_signup_negative(sb, test_data):
    """Test invalid signup inputs"""
    
    # ARRANGE
    sb.open("https://dev.v.shipgl.in/auth/signup")
    signup_page = SignupPage(sb, "https://dev.v.shipgl.in")
    
    # ACT
    signup_page.signup(
        first_name=test_data["first_name"],  # May be invalid
        last_name=test_data["last_name"],
        mobile=test_data["mobile"],
        email=test_data["email"],
        password=test_data["password"]
    )
    
    # ASSERT
    # Check that error message appears (form did NOT submit)
    assert sb.is_element_visible("error message selector")
    error_text = sb.get_text("error message selector")
    assert test_data["expected_error"] in error_text
    print(f"✅ {test_data['name']}: Got expected error")
    
    # CLEANUP
    # Refresh page (form not submitted, nothing to clean)
    sb.refresh()

# pytest runs this 19 times, once for each test case
# Each case takes ~2-3 seconds
# Total: 19 × 2.5 ≈ 50 seconds

# RESULTS:
# test_signup_negative[empty_first_name] PASSED
# test_signup_negative[special_chars_first_name] PASSED
# test_signup_negative[first_name_too_long] PASSED
# ... (16 more)
# ✅ All 19 PASSED (50 seconds)
```

---

### STEP 5: TEST_04 Runs - Valid Login

```python
# tests/authentication/test_04_login_positive.py

def test_login_positive(sb):
    """Test valid login using user from session"""
    
    # ARRANGE
    # Get user created in test_01 (from session)
    user = get_test_user()
    # OUTPUT: {
    #     "email": "auto_1704067200000_45678@gmail.in",
    #     "password": "Test@1234",
    #     ...
    # }
    
    # ACT
    sb.open("https://dev.v.shipgl.in/auth/login")
    login_page = LoginPage(sb, "https://dev.v.shipgl.in")
    
    login_page.login(
        email=user["email"],           # Uses SAME user from test_01
        password=user["password"]
    )
    
    # Browser submitted login
    # Server checks:
    # - Email exists? ✅ (created in test_01)
    # - Password correct? ✅ (Test@1234)
    # - mobile_verified = 1? ✅ (updated in test_01)
    # → Login successful!
    
    # Wait for redirect (may show merchant agreement or dashboard)
    sb.wait_for_element("dashboard or agreement selector")
    
    # ASSERT
    assert sb.is_element_visible("dashboard selector")
    print("✅ Login successful, dashboard visible")
    
    # CLEANUP
    # No cleanup - user stays in session for other tests

# RESULT: ✅ PASSED (8 seconds)
```

---

### STEP 6: TEST_05 Runs - Login Validation (8 cases)

```python
# tests/authentication/test_05_login_negative.py

# Using @pytest.mark.parametrize, this runs 8 SEPARATE tests

@pytest.mark.parametrize("test_data", [
    {
        "name": "empty_email",
        "email": "",  # Invalid!
        "password": "Test@1234",
        "expected_error": "Email is required"
    },
    {
        "name": "wrong_password",
        "email": "auto_1704067200000_45678@gmail.in",  # Valid
        "password": "WrongPassword123",  # Wrong!
        "expected_error": "Invalid credentials"
    },
    # ... 6 more cases
])
def test_login_negative(sb, test_data):
    """Test invalid login inputs"""
    
    # ARRANGE
    sb.open("https://dev.v.shipgl.in/auth/login")
    login_page = LoginPage(sb, "https://dev.v.shipgl.in")
    
    # ACT
    login_page.login(
        email=test_data["email"],      # May be invalid
        password=test_data["password"] # May be wrong
    )
    
    # ASSERT
    # Check that error message appears (login failed)
    assert sb.is_element_visible("error message selector")
    error_text = sb.get_text("error message selector")
    assert test_data["expected_error"] in error_text
    print(f"✅ {test_data['name']}: Got expected error")
    
    # CLEANUP
    # Refresh page (login failed, nothing to clean)
    sb.refresh()

# pytest runs this 8 times, once for each case
# RESULTS:
# test_login_negative[empty_email] PASSED
# test_login_negative[wrong_password] PASSED
# ... (6 more)
# ✅ All 8 PASSED (20 seconds)
```

---

### STEP 7: Teardown - conftest.py Cleanup

```python
# conftest.py - After ALL tests complete

# The sb fixture's cleanup code runs:

@pytest.fixture(scope="session")
def sb():
    sb = SB()
    sb.open("https://dev.v.shipgl.in")
    yield sb
    
    # ========== CLEANUP CODE RUNS HERE ==========
    print("All tests complete, closing browser...")
    
    # Close browser (all cookies, session data deleted)
    sb.quit()
    
    # Can optionally close database connection
    # connection.close()
    
    # Can optionally cleanup test users in database
    # (But we left users in for verification)
    
    print("Browser closed, resources freed")
    # ==========================================

# RESULT:
# ✅ Browser closed
# ✅ Database connection closed
# ✅ Resources cleaned up
```

---

## 🔍 Understanding Parametrize

### How pytest.mark.parametrize Works

```python
# EXAMPLE: test_03_signup_negative.py

# Define test cases
TEST_CASES = {
    "case_1": {
        "first_name": "",
        "error": "First name required"
    },
    "case_2": {
        "first_name": "John@",
        "error": "Special chars not allowed"
    },
    "case_3": {
        "first_name": "A" * 100,
        "error": "Too long"
    }
}

# Parametrize decorator tells pytest to run test_signup_negative
# ONCE for each case with the data filled in

@pytest.mark.parametrize(
    "case_name,case_data",
    TEST_CASES.items()  # This is: [("case_1", {...}), ("case_2", {...}), ...]
)
def test_signup_negative(sb, case_name, case_data):
    print(f"Running: {case_name}")
    print(f"Data: {case_data}")
    # Test code here
    
    # pytest will call this function 3 times:
    # 1. test_signup_negative[case_1]: case_name="case_1", case_data={...}
    # 2. test_signup_negative[case_2]: case_name="case_2", case_data={...}
    # 3. test_signup_negative[case_3]: case_name="case_3", case_data={...}

# OUTPUT:
# test_signup_negative[case_1] PASSED
# test_signup_negative[case_2] PASSED
# test_signup_negative[case_3] PASSED
```

---

## 📊 Test Execution Timeline

```
START (Time 0:00)
│
├─ SETUP (conftest.py fixture)
│  └─ Open browser: https://dev.v.shipgl.in
│  └─ ⏱️ Takes ~2 seconds
│
├─ TEST_01: test_01_auth_e2e.py::test_auth_flow
│  └─ ⏱️ 35 seconds
│  └─ Time: 0:02 → 0:37
│
├─ TEST_02: test_02_signup_positive.py::test_signup_positive
│  └─ ⏱️ 22 seconds
│  └─ Time: 0:37 → 0:59
│
├─ TEST_03: test_03_signup_negative.py::test_signup_negative (19 cases)
│  ├─ test_signup_negative[case_1] ⏱️ 2 sec (0:59 → 1:01)
│  ├─ test_signup_negative[case_2] ⏱️ 2 sec (1:01 → 1:03)
│  ├─ ... (17 more cases)
│  └─ Total: ⏱️ 50 seconds
│  └─ Time: 0:59 → 1:49
│
├─ TEST_04: test_04_login_positive.py::test_login_positive
│  └─ ⏱️ 8 seconds
│  └─ Time: 1:49 → 1:57
│
├─ TEST_05: test_05_login_negative.py::test_login_negative (8 cases)
│  ├─ test_login_negative[case_1] ⏱️ 2 sec
│  ├─ test_login_negative[case_2] ⏱️ 2 sec
│  ├─ ... (6 more cases)
│  └─ Total: ⏱️ 20 seconds
│  └─ Time: 1:57 → 2:17
│
├─ TEARDOWN (conftest.py fixture cleanup)
│  └─ Close browser
│  └─ ⏱️ Takes ~30 seconds
│  └─ Time: 2:17 → 2:47
│
├─ Generate Report
│  └─ ⏱️ Takes ~7 seconds
│  └─ Time: 2:47 → 2:54
│
END (Time 2:54)

═══════════════════════════════════════════
   30 passed in 2 minutes 54 seconds ✅
═══════════════════════════════════════════
```

---

## 📝 Test Output Explanation

```bash
$ pytest tests/authentication/ -v

======================== test session starts ==========================

platform darwin -- Python 3.14.0, pytest-9.0.2, pluggy-1.1.1
rootdir: /Users/.../Full-Stack-Test-Automation-Framework
plugins: ...
configfile: pytest.ini

collected 30 items

tests/authentication/test_01_auth_e2e.py::test_auth_flow PASSED       [ 3%]
  ↑ Test file                            ↑ Result    ↑ Progress
  
tests/authentication/test_02_signup_positive.py::test_signup_positive PASSED   [ 10%]

tests/authentication/test_03_signup_negative.py::test_signup_negative[case_1] PASSED  [ 17%]
  ↑ [case_1] shows which parametrized case ran
  
tests/authentication/test_03_signup_negative.py::test_signup_negative[case_2] PASSED  [ 20%]
... (17 more cases)
tests/authentication/test_03_signup_negative.py::test_signup_negative[case_19] PASSED [ 70%]

tests/authentication/test_04_login_positive.py::test_login_positive PASSED     [ 74%]

tests/authentication/test_05_login_negative.py::test_login_negative[case_1] PASSED   [ 81%]
... (7 more cases)
tests/authentication/test_05_login_negative.py::test_login_negative[case_8] PASSED   [100%]

======================== 30 passed in 2m54s ===========================
  ↑ All tests passed!    ↑ Total time
```

---

## 🎯 Key Points to Remember

1. **Browser opens ONCE** (scope="session")
   - All 30 tests use SAME browser
   - Saves time (don't open/close browser 30 times)

2. **Session persists between tests**
   - test_01 creates user
   - test_04 uses SAME user from session
   - This is why tests must run in order

3. **Parametrize multiplies tests**
   - test_03 with 19 cases = 19 individual pytest tests
   - test_05 with 8 cases = 8 individual pytest tests
   - Each runs separately

4. **Each test cleans itself**
   - Most tests delete their test user in cleanup
   - test_01 does NOT delete (we keep it for verification)

5. **Total time is ~3 minutes**
   - Not 30 × 5 seconds = 150 seconds
   - Because browser reuse saves 60-90 seconds
   - Because we don't wait for page loads between tests

---

## 💡 Summary

```
Pytest loads → Opens browser ONCE → Runs all 30 tests sequentially 
→ Each test reuses SAME browser → Browser has session cookies 
→ Tests share user data via session.py → All tests pass ✅ 
→ Browser closes → Tests complete in 2:54
```

Ready to see how functions call each other? Read **04_FUNCTION_MAP.md** next! 📚
