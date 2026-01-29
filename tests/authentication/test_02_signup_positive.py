"""
✅ SIGNUP POSITIVE TEST CASES

Simple test data objects - each object is ONE test case
Easy to add new test cases - just add object to TEST_CASES list

Every test:
- Creates FRESH email (auto_[timestamp]_[random]@gmail.in)
- Creates FRESH mobile (9XXXXXXXXX)
- Uses strong password (Test@1234)
- Tests that user can signup with valid data
"""
from src.pages.authentication.signup_page import SignupPage
from src.utils.session import create_fresh_test_user


# ============================================================================
# TEST DATA - EACH OBJECT IS ONE TEST CASE
# ============================================================================
TEST_CASES = [
    {
        "name": "Valid signup with all fields filled",
        "description": "User can signup with valid first name, last name, mobile, email, password",
        "expect": "success"  # Should redirect to mobile verification page
    },
]


# ============================================================================
# TEST IMPLEMENTATION
# ============================================================================
class TestSignupPositive:
    """Test: Valid signup form submission"""
    
    def test_02_signup_with_valid_data(self, sb):
        """
        ✅ HAPPY PATH: User can signup with valid data
        
        Test Case: Valid signup with all fields filled
        
        Flow:
        1. Arrange: Create fresh user with unique email & mobile
        2. Act: Submit signup form with valid data
        3. Assert: Redirected to mobile verification page
        """
        # Get test case data
        test_case = TEST_CASES[0]
        
        print(f"\n{'='*70}")
        print(f"TEST: {test_case['name']}")
        print(f"Description: {test_case['description']}")
        print(f"{'='*70}")
        
        # ARRANGE: Create fresh user with unique data
        user = create_fresh_test_user()
        signup = SignupPage(sb)
        
        print(f"\n📝 User Data:")
        print(f"   Email: {user['email']}")
        print(f"   Mobile: {user['mobile']}")
        print(f"   Password: {user['password']}")
        
        # ACT: Open signup and submit form
        print(f"\n🔄 Action: Opening signup page and submitting form...")
        signup.open()
        signup.submit(user)
        
        # ASSERT: Verify redirect to mobile verification page
        print(f"\n✔️ Assertion: Checking if redirected to mobile verification page...")
        sb.wait(1)
        current_url = sb.get_current_url()
        
        assert "verify-mobile" in current_url, \
            f"Expected verify-mobile page, got {current_url}"
        
        # CLEANUP: Logout to clean state for next tests
        print(f"\n🔐 Cleanup: Logging out...")
        sb.open("https://dev.v.shipgl.in/logout")
        sb.wait(1)
        sb.open("https://dev.v.shipgl.in/auth/signup")
        sb.wait(1)
        
        print(f"\n✅ TEST PASSED\n")
