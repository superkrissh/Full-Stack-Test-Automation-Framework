"""
❌ LOGIN NEGATIVE TEST CASES (Form Validation)

8 validation test cases for login form
Tests invalid credentials

✅ OPTIMIZATION:
- Opens page ONCE at start
- Tests ALL 8 cases on same page
- Refreshes between cases (not reopens browser)
- NO browser reopening = FAST
"""
from src.pages.authentication.login_page import LoginPage


# ============================================================================
# TEST DATA - 8 LOGIN VALIDATION TEST CASES
# ============================================================================

# Email validation (3 cases)
EMAIL_CASES = [
    {"email": "", "password": "Test@1234", "description": "Empty field"},
    {"email": "invalidemail", "password": "Test@1234", "description": "Invalid format (no @ symbol)"},
    {"email": "nonexistent@gmail.com", "password": "Test@1234", "description": "Valid format but user doesn't exist"},
]

# Password validation (3 cases)
PASSWORD_CASES = [
    {"email": "test@example.com", "password": "", "description": "Empty field"},
    {"email": "test@example.com", "password": "WrongPassword123", "description": "Incorrect password"},
    {"email": "test@example.com", "password": "Pass1", "description": "Too short"},
]

# Both fields invalid (2 cases)
BOTH_INVALID_CASES = [
    {"email": "", "password": "", "description": "Both fields empty"},
    {"email": "invalidemail", "password": "short", "description": "Both fields invalid"},
]

# Combine all cases in order
ALL_TEST_CASES = []
for case in EMAIL_CASES:
    ALL_TEST_CASES.append(("email", case))
for case in PASSWORD_CASES:
    ALL_TEST_CASES.append(("password", case))
for case in BOTH_INVALID_CASES:
    ALL_TEST_CASES.append(("both", case))


# ============================================================================
# TEST IMPLEMENTATION
# ============================================================================
class TestLoginNegative:
    """Login form validation - 8 test cases on ONE page
    
    ✅ SINGLE TEST METHOD
    ✅ Opens page ONCE
    ✅ Tests all 8 cases with refresh between each
    ✅ No browser reopening = FAST
    """
    
    def test_05_all_login_validations(self, sb):
        """❌ Test all 8 login validation cases on same page with refresh between
        
        Note: Browser is already at login page from previous test (test_03)
        If not, navigate there first. Then just refresh between test cases.
        """
        login = LoginPage(sb)
        
        # Check if we're already on login page from previous test
        current_url = sb.get_current_url()
        if "login" not in current_url:
            login.open()  # Open only if not already on login page
        else:
            print("  (Browser already at login page from previous test)")
        
        passed = 0
        failed = 0
        
        for i, (field_name, case) in enumerate(ALL_TEST_CASES):
            # ✅ Refresh for next case (except first if we just opened)
            if i > 0 or "login" not in sb.get_current_url():
                login.refresh_form()
            
            # Login with invalid data
            login.login(case["email"], case["password"])
            
            # Verify form stayed on login (validation rejected)
            current_url = sb.get_current_url()
            if "login" in current_url:
                passed += 1
                print(f"  ✓ Case {i+1:2d}/8: {field_name.upper():8s} - {case['description']}")
            else:
                failed += 1
                print(f"  ✗ Case {i+1:2d}/8: {field_name.upper():8s} - {case['description']}")
                print(f"    ERROR: Expected login page, got {current_url}")
                assert False, f"Form should stay on login, but got {current_url}"
        
        print(f"\n✅ SUCCESS: All 8 validation cases passed!")
        print(f"   Passed: {passed}/8 | Failed: {failed}/8")
        print(f"   (No browser reopening - single page load with refreshes)")


