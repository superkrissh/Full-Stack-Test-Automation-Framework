"""
❌ SIGNUP NEGATIVE TEST CASES (Form Validation)

19 validation test cases for signup form
Tests invalid data in each field

✅ OPTIMIZATION: 
- Opens page ONCE at start
- Tests ALL 19 cases on same page
- Refreshes between cases (not reopens browser)
- Total: ~18 seconds for all 19 cases
- NO browser reopening = FAST
"""
from src.pages.authentication.signup_page import SignupPage
from src.utils.session import create_fresh_test_user


# ============================================================================
# TEST DATA - 19 VALIDATION TEST CASES
# ============================================================================

# First Name validation (3 cases)
FIRST_NAME_CASES = [
    {"value": "", "description": "Empty field"},
    {"value": "John123", "description": "Contains numbers"},
    {"value": "John@#$", "description": "Contains special characters"},
]

# Last Name validation (3 cases)
LAST_NAME_CASES = [
    {"value": "", "description": "Empty field"},
    {"value": "Smith123", "description": "Contains numbers"},
    {"value": "Smith@#$", "description": "Contains special characters"},
]

# Mobile validation (4 cases)
MOBILE_CASES = [
    {"value": "", "description": "Empty field"},
    {"value": "987654321", "description": "Less than 10 digits"},
    {"value": "98765432123", "description": "More than 10 digits"},
    {"value": "98765abcde", "description": "Non-numeric characters"},
]

# Email validation (4 cases)
EMAIL_CASES = [
    {"value": "", "description": "Empty field"},
    {"value": "invalidemail", "description": "Missing @ symbol"},
    {"value": "test@", "description": "Missing domain name"},
    {"value": "test@domain", "description": "Missing domain extension (.com, .in, etc)"},
]

# Password validation (4 cases)
PASSWORD_CASES = [
    {"password": "", "confirm": "", "description": "Both fields empty"},
    {"password": "Pass1", "confirm": "Pass1", "description": "Less than 6 characters"},
    {"password": "Test@1234", "confirm": "Different", "description": "Mismatch between password and confirm"},
    {"password": "Test@1234", "confirm": "", "description": "Confirm password field empty"},
]

# Terms & Conditions (1 case)
TOC_CASES = [
    {"toc": False, "description": "T&C checkbox not checked"},
]

# Combine all cases in order
ALL_TEST_CASES = []
for case in FIRST_NAME_CASES:
    ALL_TEST_CASES.append(("first_name", case))
for case in LAST_NAME_CASES:
    ALL_TEST_CASES.append(("last_name", case))
for case in MOBILE_CASES:
    ALL_TEST_CASES.append(("mobile", case))
for case in EMAIL_CASES:
    ALL_TEST_CASES.append(("email", case))
for case in PASSWORD_CASES:
    ALL_TEST_CASES.append(("password", case))
for case in TOC_CASES:
    ALL_TEST_CASES.append(("toc", case))


# ============================================================================
# TEST IMPLEMENTATION
# ============================================================================
class TestSignupNegative:
    """Signup form validation - 19 test cases on ONE page
    
    ✅ SINGLE TEST METHOD
    ✅ Opens page ONCE
    ✅ Tests all 19 cases with refresh between each
    ✅ No browser reopening = FAST
    """
    
    def test_03_all_signup_validations(self, sb):
        """❌ Test all 19 signup validation cases on same page with refresh between"""
        signup = SignupPage(sb)
        signup.open()  # ✅ OPEN PAGE ONCE
        
        passed = 0
        failed = 0
        
        for i, (field_name, case) in enumerate(ALL_TEST_CASES):
            # ✅ Refresh for next case (except first)
            if i > 0:
                signup.refresh_form()
            
            # Create user and set invalid field
            user = create_fresh_test_user()
            
            if field_name == "first_name":
                user["first_name"] = case["value"]
            elif field_name == "last_name":
                user["last_name"] = case["value"]
            elif field_name == "mobile":
                user["mobile"] = case["value"]
            elif field_name == "email":
                user["email"] = case["value"]
            elif field_name == "password":
                user["password"] = case["password"]
                user["confirm_password"] = case["confirm"]
            elif field_name == "toc":
                user["toc"] = case["toc"]
            
            # Submit invalid data
            signup.submit(user)
            
            # Verify form stayed on signup (validation rejected)
            current_url = sb.get_current_url()
            if "signup" in current_url:
                passed += 1
                print(f"  ✓ Case {i+1:2d}/19: {field_name.upper():12s} - {case['description']}")
            else:
                failed += 1
                print(f"  ✗ Case {i+1:2d}/19: {field_name.upper():12s} - {case['description']}")
                print(f"    ERROR: Expected signup page, got {current_url}")
                assert False, f"Form should stay on signup, but got {current_url}"
        
        print(f"\n✅ SUCCESS: All 19 validation cases passed!")
        print(f"   Passed: {passed}/19 | Failed: {failed}/19")
        print(f"   (No browser reopening - single page load with refreshes)")
        
        # ✅ IMPORTANT: Navigate to login page for next test
        # This way test_05 doesn't need to open new browser
        print(f"\n→ Navigating to login page for next test...")
        signup.login_page_url = "https://dev.v.shipgl.in/auth/login"
        sb.open(signup.login_page_url)


