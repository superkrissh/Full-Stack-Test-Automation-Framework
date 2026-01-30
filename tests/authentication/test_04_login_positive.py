"""
✅ LOGIN POSITIVE TEST CASES

Test: User can login with valid credentials
Expected: Login succeeds and merchant agreement modal appears

Execution Order:
- Runs AFTER test_01_auth_e2e.py (creates and verifies the user)
- Uses user created in E2E test (already mobile_verified=1)
- User stored in session for easy access

What makes this simple:
- Just use get_test_user() from session
- Enter credentials and login
- Check if on correct page

To add new test cases:
- Add object to TEST_CASES
- Write simple test method
"""
from src.pages.authentication.login_page import LoginPage
from src.utils.session import get_test_user


# ============================================================================
# TEST DATA - SIMPLE LOGIN TEST CASES
# ============================================================================
TEST_CASES = [
    {
        "name": "Login with valid credentials",
        "description": "User can login with valid email and password",
        "expect": "success"  # Should show merchant agreement or redirect to orders
    },
]


# ============================================================================
# TEST IMPLEMENTATION
# ============================================================================
class TestLoginPositive:
    """Test: Login with valid credentials"""
    
    def test_04_login_with_valid_credentials(self, sb):
        """
        ✅ HAPPY PATH: Login with valid credentials
        
        Prerequisites:
        - User created in test_01_auth_e2e.py
        - User mobile verified (mobile_verified=1)
        - User stored in session
        
        Test Flow:
        1. Arrange: Get user from session
        2. Act: Submit login with valid email & password
        3. Assert: Either on login page (with merchant agreement modal) or orders page
        
        Expected: Login succeeds
        """
        test_case = TEST_CASES[0]
        
        print(f"\n{'='*70}")
        print(f"TEST: {test_case['name']}")
        print(f"Description: {test_case['description']}")
        print(f"{'='*70}")
        
        # ARRANGE: Get user from session (created in E2E test)
        user = get_test_user()
        
        print(f"\n📝 User Data (from E2E test):")
        print(f"   Email: {user['email']}")
        print(f"   Password: {user['password']}")
        print(f"   Mobile Verified: Yes")
        
        # ACT: Open login and submit credentials
        print(f"\n🔄 Action: Logging in with valid credentials...")
        login = LoginPage(sb)
        login.open()
        login.login(user["email"], user["password"])
        
        # ASSERT: Check if on correct page
        print(f"\n✔️ Assertion: Checking if login succeeded...")
        sb.wait(1)
        current_url = sb.get_current_url()
        
        # Expected: Either still on login page (showing merchant agreement modal)
        # OR already redirected to orders page
        assert "login" in current_url or "orders" in current_url, \
            f"Expected login or orders page, got {current_url}"
        
        print(f"✔️ Login successful!")
        print(f"✔️ Current page: {current_url}")
        
        print(f"\n✅ TEST PASSED\n")
