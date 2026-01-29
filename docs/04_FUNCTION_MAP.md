# 04_FUNCTION_MAP.md - Which Function Calls Which & What Data Flows

---

## 🗺️ Complete Function Call Map

```
TEST FILE
  ↓
  test_01_auth_e2e.py::test_auth_flow()
  │
  ├─ CALL: create_fresh_test_user()
  │  ├─ FROM: src/utils/session.py
  │  ├─ DOES: Generate unique email, mobile, password
  │  ├─ INPUT: None
  │  └─ OUTPUT: Dict with:
  │             {
  │                 "email": "auto_1704067200000_45678@gmail.in",
  │                 "mobile": "9876543210",
  │                 "password": "Test@1234",
  │                 "first_name": "John",
  │                 "last_name": "Doe"
  │             }
  │
  ├─ CALL: create_test_session(user)
  │  ├─ FROM: src/utils/session.py
  │  ├─ DOES: Stores user data in global _test_session
  │  ├─ INPUT: user dict (email, mobile, password, names)
  │  ├─ OUTPUT: None (modifies global state)
  │  └─ RESULT: _test_session["user"] = user
  │
  ├─ CALL: SignupPage(browser, base_url)
  │  ├─ FROM: src/pages/authentication/signup_page.py
  │  ├─ DOES: Creates page object for signup interaction
  │  ├─ INPUT: browser (SeleniumBase), base_url (string)
  │  ├─ OUTPUT: SignupPage instance with methods:
  │             - signup(first_name, last_name, mobile, email, password)
  │  └─ USES: SignupPageLocators from src/locators/authentication_locators.py
  │
  ├─ CALL: signup_page.signup(first_name, last_name, mobile, email, password)
  │  ├─ DOES: Fill form fields and click submit
  │  ├─ INPUT: first_name, last_name, mobile, email, password (strings)
  │  ├─ STEPS:
  │  │  ├─ self.type(self.FIRST_NAME, first_name)
  │  │  │  └─ CALL: browser.type(selector, text)
  │  │  │     └─ Types text into field matching selector
  │  │  ├─ self.type(self.LAST_NAME, last_name)
  │  │  ├─ self.type(self.MOBILE, mobile)
  │  │  ├─ self.type(self.EMAIL, email)
  │  │  ├─ self.type(self.PASSWORD, password)
  │  │  ├─ self.type(self.CONFIRM_PASSWORD, password)
  │  │  ├─ self.click(self.TERMS_CHECKBOX)
  │  │  │  └─ CALL: browser.click(selector)
  │  │  │     └─ Clicks element matching selector
  │  │  └─ self.click(self.SUBMIT_BUTTON)
  │  └─ OUTPUT: None (modified browser state - submitted form)
  │
  ├─ BROWSER: Submits form to server
  │  └─ Server: INSERT INTO vendor (email, password, ..., mobile_verified=0)
  │
  ├─ BROWSER: Waits for page redirect
  │  └─ CALL: self.wait_for_element(selector)
  │     └─ Waits up to 10 seconds for element to appear
  │
  ├─ CALL: update_mobile_verified(email)
  │  ├─ FROM: src/utils/db.py
  │  ├─ DOES: Updates database to simulate OTP verification
  │  ├─ INPUT: email (string)
  │  ├─ EXECUTION:
  │  │  ├─ CALL: get_db_connection()
  │  │  │  ├─ FROM: src/utils/db.py
  │  │  │  ├─ USES: DATABASE_CONFIG from configs/settings.py
  │  │  │  ├─ DATABASE_CONFIG = {
  │  │  │  │     "host": "3.6.16.231",
  │  │  │  │     "user": "shipgl_user",
  │  │  │  │     "password": "****",
  │  │  │  │     "database": "staging"
  │  │  │  │  }
  │  │  │  └─ OUTPUT: Connection object
  │  │  │
  │  │  ├─ Execute SQL query:
  │  │  │  │ UPDATE vendor
  │  │  │  │ SET mobile_verified = 1
  │  │  │  │ WHERE email = 'auto_1704067200000_45678@gmail.in'
  │  │  │  │
  │  │  │  └─ RESULT: 1 row updated
  │  │  │
  │  │  └─ CALL: connection.close()
  │  │
  │  ├─ OUTPUT: Number of rows updated (usually 1)
  │  └─ DATABASE CHANGE: mobile_verified changed 0 → 1
  │
  ├─ CALL: LoginPage(browser, base_url)
  │  ├─ FROM: src/pages/authentication/login_page.py
  │  ├─ DOES: Creates page object for login interaction
  │  └─ OUTPUT: LoginPage instance with method:
  │             - login(email, password)
  │
  ├─ CALL: login_page.login(email, password)
  │  ├─ DOES: Fill login form and submit
  │  ├─ INPUT: email, password (strings)
  │  ├─ STEPS:
  │  │  ├─ self.type(self.EMAIL, email)
  │  │  ├─ self.type(self.PASSWORD, password)
  │  │  └─ self.click(self.SUBMIT_BUTTON)
  │  └─ OUTPUT: None (submitted form)
  │
  ├─ BROWSER: Submits login form
  │  └─ SERVER CHECKS:
  │     ├─ SELECT * FROM vendor WHERE email = ?
  │     │  └─ Result: User exists ✅
  │     ├─ Check password hash match
  │     │  └─ Result: Correct password ✅
  │     ├─ Check: mobile_verified = 1
  │     │  └─ Result: mobile_verified = 1 ✅
  │     └─ Create session cookie and redirect
  │
  ├─ BROWSER: Redirects to merchant agreement page
  │  └─ Merchant agreement modal shown
  │
  ├─ CALL: accept_merchant_agreement()
  │  ├─ FROM: test_01_auth_e2e.py (defined in the test)
  │  ├─ DOES: Click agree checkbox and continue button
  │  └─ OUTPUT: None (clicked buttons)
  │
  ├─ BROWSER: Redirects to dashboard
  │  └─ Dashboard page shown (success!)
  │
  └─ CLEANUP: (NOT deleting vendor - keeping for verification)
     └─ # delete_vendor(email) is COMMENTED OUT
```

---

## 🔄 Function Dependency Graph

```
test_01_auth_e2e()
├─ create_fresh_test_user()
│  └─ [No dependencies - generates data]
│
├─ create_test_session()
│  └─ Depends on: create_fresh_test_user() output
│
├─ SignupPage()
│  └─ Depends on: BasePage (parent class)
│     └─ BasePage imports:
│        ├─ SeleniumBase (browser framework)
│        └─ SignupPageLocators (selectors)
│
├─ signup_page.signup()
│  └─ Depends on: SignupPage instance
│
├─ update_mobile_verified()
│  └─ Depends on: get_db_connection()
│     └─ Depends on: DATABASE_CONFIG from configs/settings.py
│
├─ LoginPage()
│  └─ Depends on: BasePage
│
├─ login_page.login()
│  └─ Depends on: LoginPage instance
│
└─ accept_merchant_agreement()
   └─ Browser actions (no Python function call)
```

---

## 📊 Data Flow Through Functions

### Flow 1: User Creation

```
create_fresh_test_user() outputs:
┌──────────────────────────────────────┐
│ user = {                             │
│   "email": "auto_xxx@gmail.in",      │
│   "mobile": "9876543210",            │
│   "password": "Test@1234",           │
│   "first_name": "John",              │
│   "last_name": "Doe"                 │
│ }                                    │
└──────────────────────────────────────┘
         ↓ passed to
create_test_session(user)
         ↓ stores in
_test_session["user"] = user
         ↓ can be retrieved by
get_test_user() → returns same dict
```

### Flow 2: Signup Form → Database

```
signup_page.signup(
    first_name="John",
    last_name="Doe",
    mobile="9876543210",
    email="auto_xxx@gmail.in",
    password="Test@1234"
)
    ↓ calls browser.type() for each field
    ↓ calls browser.click() for submit
         ↓
    Browser sends POST request to:
    https://dev.v.shipgl.in/auth/signup
         ↓
    Server executes:
    INSERT INTO vendor (
        firstname='John',
        lastname='Doe',
        mobile='9876543210',
        email='auto_xxx@gmail.in',
        password=hash('Test@1234'),
        mobile_verified=0
    )
         ↓
    User created in database ✅
```

### Flow 3: Mobile Verification

```
update_mobile_verified(
    email="auto_xxx@gmail.in"
)
    ↓
    get_db_connection() → Connection object
         ↓
    cursor.execute(
        "UPDATE vendor SET mobile_verified = 1
         WHERE email = %s",
        (email,)
    )
         ↓
    Database executes:
    UPDATE vendor
    SET mobile_verified = 1
    WHERE email = 'auto_xxx@gmail.in'
         ↓
    mobile_verified: 0 → 1 ✅
    rows_affected: 1
         ↓
    returns: 1
```

### Flow 4: Login → Session

```
login_page.login(
    email="auto_xxx@gmail.in",
    password="Test@1234"
)
    ↓
    Browser sends POST request
         ↓
    Server checks:
    1. SELECT * FROM vendor
       WHERE email = 'auto_xxx@gmail.in'
       RESULT: User found ✅
    
    2. Compare password hash
       RESULT: Correct ✅
    
    3. Check mobile_verified
       RESULT: mobile_verified = 1 ✅
         ↓
    Server creates session cookie:
    Set-Cookie: sessionId=abc123xyz; Path=/
         ↓
    Browser stores cookie automatically
         ↓
    Browser redirected to /merchant-agreement
    
    Browser still has cookie - can make authenticated requests
```

---

## 📝 Function Signatures & Documentation

### session.py Functions

```python
def create_fresh_test_user() -> dict:
    """
    Generate a unique test user with random email and mobile.
    
    Returns:
        dict: {
            "email": "auto_{timestamp}_{random}@gmail.in",
            "mobile": "9{9 random digits}",
            "password": "Test@1234",
            "first_name": "John",
            "last_name": "Doe"
        }
    
    Example:
        user = create_fresh_test_user()
        # user["email"] = "auto_1704067200000_45678@gmail.in"
    """

def create_test_session(user: dict) -> None:
    """
    Store user data in session for other tests to access.
    
    Args:
        user (dict): User dictionary with email, password, etc.
    
    Returns:
        None (modifies global _test_session)
    
    Example:
        user = create_fresh_test_user()
        create_test_session(user)
        # Now other tests can call get_test_user()
    """

def get_test_user() -> dict:
    """
    Retrieve stored user from session.
    
    Returns:
        dict: Same user data stored by create_test_session()
    
    Example:
        user = get_test_user()
        # user["email"] = "auto_1704067200000_45678@gmail.in"
    """

def cleanup_test_session() -> None:
    """
    Clear session after all tests complete.
    
    Returns:
        None (clears global _test_session)
    """
```

### db.py Functions

```python
def get_db_connection() -> mysql.connector.MySQLConnection:
    """
    Create and return database connection.
    
    Returns:
        Connection: MySQL connection object
    
    Raises:
        mysql.connector.Error: If connection fails
    
    Example:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM vendor")
    """

def user_exists(email: str) -> bool:
    """
    Check if user exists in database.
    
    Args:
        email (str): User email to check
    
    Returns:
        bool: True if user exists, False otherwise
    
    Example:
        exists = user_exists("auto_xxx@gmail.in")
        if exists:
            print("User found")
    """

def update_mobile_verified(email: str) -> int:
    """
    Update vendor record to mark mobile as verified.
    
    Args:
        email (str): User email
    
    Returns:
        int: Number of rows updated (usually 0 or 1)
    
    Example:
        rows = update_mobile_verified("auto_xxx@gmail.in")
        print(f"Updated {rows} row(s)")
    
    SQL executed:
        UPDATE vendor SET mobile_verified = 1 WHERE email = %s
    """

def delete_vendor(email: str) -> int:
    """
    Delete vendor record (cleanup after tests).
    
    Args:
        email (str): User email
    
    Returns:
        int: Number of rows deleted (usually 0 or 1)
    
    Example:
        rows = delete_vendor("auto_xxx@gmail.in")
        print(f"Deleted {rows} row(s)")
    
    SQL executed:
        DELETE FROM vendor WHERE email = %s
    """
```

### Page Object Functions

```python
class SignupPage(BasePage):
    """Represent signup form page"""
    
    def signup(
        self,
        first_name: str,
        last_name: str,
        mobile: str,
        email: str,
        password: str
    ) -> None:
        """
        Fill signup form and submit.
        
        Args:
            first_name (str): User's first name
            last_name (str): User's last name
            mobile (str): User's mobile number
            email (str): User's email
            password (str): User's password
        
        Returns:
            None (modifies browser state)
        
        Example:
            page = SignupPage(browser, "https://...")
            page.signup(
                first_name="John",
                last_name="Doe",
                mobile="9876543210",
                email="auto_xxx@gmail.in",
                password="Test@1234"
            )
        """

class LoginPage(BasePage):
    """Represent login form page"""
    
    def login(self, email: str, password: str) -> None:
        """
        Fill login form and submit.
        
        Args:
            email (str): User's email
            password (str): User's password
        
        Returns:
            None (modifies browser state)
        
        Example:
            page = LoginPage(browser, "https://...")
            page.login(
                email="auto_xxx@gmail.in",
                password="Test@1234"
            )
        """
```

---

## 🔗 Import Dependencies

```
test_01_auth_e2e.py imports:
├─ from src.utils.session import:
│  ├─ create_fresh_test_user
│  ├─ create_test_session
│  └─ get_test_user
│
├─ from src.pages.authentication.signup_page import SignupPage
│  └─ SignupPage imports:
│     ├─ from src.core.base_page import BasePage
│     │  └─ BasePage imports:
│     │     └─ from seleniumbase import SB
│     └─ from src.locators.authentication_locators import SignupPageLocators
│
├─ from src.pages.authentication.login_page import LoginPage
│  └─ LoginPage imports:
│     ├─ from src.core.base_page import BasePage
│     └─ from src.locators.authentication_locators import LoginPageLocators
│
├─ from src.utils.db import:
│  ├─ user_exists
│  ├─ update_mobile_verified
│  └─ delete_vendor
│  └─ These import:
│     └─ from configs.settings import DATABASE_CONFIG
│
└─ Standard library:
   ├─ import pytest
   └─ from selenium.webdriver.common.by import By
```

---

## 📈 Call Hierarchy

```
Level 1 (Test File):
  test_01_auth_e2e()

Level 2 (Utility Functions):
  ├─ create_fresh_test_user()
  ├─ create_test_session()
  ├─ user_exists()
  ├─ update_mobile_verified()
  └─ delete_vendor()

Level 2 (Page Objects):
  ├─ SignupPage()
  ├─ LoginPage()
  └─ MobileVerificationPage()

Level 3 (Page Object Methods):
  ├─ signup_page.signup(...)
  │  └─ browser.type(selector, text)
  │  └─ browser.click(selector)
  │
  └─ login_page.login(...)
     └─ browser.type(selector, text)
     └─ browser.click(selector)

Level 3 (Database Functions):
  ├─ get_db_connection()
  │  └─ mysql.connector.connect(**DATABASE_CONFIG)
  └─ cursor.execute(sql_query)

Level 4 (Selectors):
  └─ SignupPageLocators.FIRST_NAME (just constant strings)
  └─ LoginPageLocators.EMAIL (just constant strings)

Level 4 (Configuration):
  └─ DATABASE_CONFIG (just constant dict)
  └─ BASE_URL (just constant string)
```

---

## 🎯 Data Transformation Through Functions

```
Raw Data (Input)
    ↓
create_fresh_test_user()
    ↓
User Dict:
{
    "email": "auto_1704067200000_45678@gmail.in",
    "password": "Test@1234",
    "mobile": "9876543210",
    "first_name": "John",
    "last_name": "Doe"
}
    ↓
signup_page.signup(first_name, last_name, mobile, email, password)
    ↓
Browser Form Fill
    ↓
Form Submission (POST request)
    ↓
Server Processing
    ↓
Database INSERT
    ↓
User in Database:
{
    "vendor_id": 123,
    "firstname": "John",
    "lastname": "Doe",
    "mobile": "9876543210",
    "email": "auto_1704067200000_45678@gmail.in",
    "password": "hash(...)",
    "mobile_verified": 0
}
    ↓
update_mobile_verified("auto_1704067200000_45678@gmail.in")
    ↓
Database UPDATE
    ↓
User in Database (Updated):
{
    ...,
    "mobile_verified": 1  ← Changed
}
    ↓
login_page.login(email, password)
    ↓
Form Submission (POST request)
    ↓
Server Authentication
    ↓
Browser Session Cookie Stored
    ↓
User Logged In ✅
```

---

## 🔬 Example: Trace One Function Call

```
STARTING POINT: test_01_auth_e2e()
│
├─ Line 15: user = create_fresh_test_user()
│
│  ↓ ENTERS: session.py::create_fresh_test_user()
│  │
│  ├─ import time
│  │  └─ timestamp = int(time.time() * 1000)  # 1704067200000
│  │
│  ├─ import random
│  │  └─ random_suffix = random.randint(10000, 99999)  # 45678
│  │
│  ├─ Email construction
│  │  └─ f"auto_{timestamp}_{random_suffix}@gmail.in"
│  │  └─ = "auto_1704067200000_45678@gmail.in"
│  │
│  ├─ Mobile construction
│  │  └─ "9" + "".join([str(random.randint(0, 9)) for _ in range(9)])
│  │  └─ = "9876543210"
│  │
│  ├─ Names
│  │  ├─ first_name = "John"
│  │  └─ last_name = "Doe"
│  │
│  ├─ Password
│  │  └─ password = "Test@1234"
│  │
│  └─ Return dict
│     └─ {
│           "email": "auto_1704067200000_45678@gmail.in",
│           "password": "Test@1234",
│           "mobile": "9876543210",
│           "first_name": "John",
│           "last_name": "Doe"
│        }
│  ↑ EXITS: create_fresh_test_user()
│
├─ user = {...} (now has the dict)
│
├─ Line 16: create_test_session(user)
│
│  ↓ ENTERS: session.py::create_test_session(user)
│  │
│  ├─ global _test_session
│  │  └─ _test_session = {}  (initially empty)
│  │
│  ├─ _test_session["user"] = user
│  │  └─ _test_session = {
│  │       "user": {
│  │           "email": "auto_1704067200000_45678@gmail.in",
│  │           ...
│  │       }
│  │    }
│  │
│  └─ return None
│  ↑ EXITS: create_test_session()
│
└─ Continue with signup...
```

---

## 🎓 Summary: Function Relationships

```
Test File calls:
  ├─ Utility functions
  │  ├─ create_fresh_test_user() → Returns user dict
  │  ├─ create_test_session() → Stores user dict
  │  ├─ user_exists() → Checks database
  │  ├─ update_mobile_verified() → Updates database
  │  └─ delete_vendor() → Deletes from database
  │
  ├─ Page Objects
  │  ├─ SignupPage(browser, base_url) → Returns page object
  │  │  └─ page.signup(data) → Interacts with browser
  │  │
  │  └─ LoginPage(browser, base_url) → Returns page object
  │     └─ page.login(data) → Interacts with browser
  │
  └─ Browser methods (from SeleniumBase)
     ├─ browser.type(selector, text) → Types into field
     ├─ browser.click(selector) → Clicks button
     ├─ browser.wait_for_element(selector) → Waits for page
     └─ browser.open(url) → Navigates to page

Data flows:
  User dict → Passed to signup_page.signup() → Browser interaction
  User dict → Stored in session → Retrieved by other tests
  User dict → Passed to login_page.login() → Browser interaction
  Email → Passed to update_mobile_verified() → Database update
```

All functions work together to:
1. **Create test data** (user dict)
2. **Store test data** (session)
3. **Interact with browser** (page objects)
4. **Interact with database** (db functions)
5. **Verify results** (assertions)

---

This completes the comprehensive documentation! You now understand:
- ✅ What each file does (01_FILE_STRUCTURE.md)
- ✅ How tests execute visually (02_VISUAL_FLOW.md)
- ✅ Step-by-step execution (03_HOW_TESTS_RUN.md)
- ✅ Function calls and data flow (04_FUNCTION_MAP.md)

Ready to run the tests! 🚀
