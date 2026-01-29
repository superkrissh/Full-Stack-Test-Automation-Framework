"""
❌ SIGNUP NEGATIVE TEST CASES (Form Validation)

Simple test data objects - 19 validation test cases
Each case tests ONE validation rule

Expected: Form stays on signup page (validation rejects invalid data)

Every test uses:
- FRESH email (auto_[timestamp]_[random]@gmail.in)
- FRESH mobile (9XXXXXXXXX)
- INVALID data in ONE field to test validation
- Verifies form stays on signup page (validation rejects it)

Easy to add new tests:
- Add new dict to VALIDATION_CASES list
- That's it! Pytest will run it automatically
"""
import pytest
from src.pages.authentication.signup_page import SignupPage
from src.utils.session import create_fresh_test_user


# ============================================================================
# TEST DATA - 19 VALIDATION TEST CASES (Dictionary Format)
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


# ============================================================================
# TEST IMPLEMENTATION
# ============================================================================
class TestSignupNegative:
    """Test: Form validation rejects invalid data"""
    
    # First Name Tests
    @pytest.mark.parametrize("first_name_case", FIRST_NAME_CASES)
    def test_03a_first_name_validation(self, sb, first_name_case):
        """❌ First Name validation - test each case"""
        user = create_fresh_test_user()
        user["first_name"] = first_name_case["value"]
        
        signup = SignupPage(sb)
        signup.open()
        signup.submit(user)
        
        sb.wait(1)
        assert "signup" in sb.get_current_url(), \
            f"First name '{first_name_case['value']}' should be rejected"
    
    # Last Name Tests
    @pytest.mark.parametrize("last_name_case", LAST_NAME_CASES)
    def test_03b_last_name_validation(self, sb, last_name_case):
        """❌ Last Name validation - test each case"""
        user = create_fresh_test_user()
        user["last_name"] = last_name_case["value"]
        
        signup = SignupPage(sb)
        signup.open()
        signup.submit(user)
        
        sb.wait(1)
        assert "signup" in sb.get_current_url(), \
            f"Last name '{last_name_case['value']}' should be rejected"
    
    # Mobile Tests
    @pytest.mark.parametrize("mobile_case", MOBILE_CASES)
    def test_03c_mobile_validation(self, sb, mobile_case):
        """❌ Mobile validation - test each case"""
        user = create_fresh_test_user()
        user["mobile"] = mobile_case["value"]
        
        signup = SignupPage(sb)
        signup.open()
        signup.submit(user)
        
        sb.wait(1)
        assert "signup" in sb.get_current_url(), \
            f"Mobile '{mobile_case['value']}' should be rejected"
    
    # Email Tests
    @pytest.mark.parametrize("email_case", EMAIL_CASES)
    def test_03d_email_validation(self, sb, email_case):
        """❌ Email validation - test each case"""
        user = create_fresh_test_user()
        user["email"] = email_case["value"]
        
        signup = SignupPage(sb)
        signup.open()
        signup.submit(user)
        
        sb.wait(1)
        assert "signup" in sb.get_current_url(), \
            f"Email '{email_case['value']}' should be rejected"
    
    # Password Tests
    @pytest.mark.parametrize("password_case", PASSWORD_CASES)
    def test_03e_password_validation(self, sb, password_case):
        """❌ Password validation - test each case"""
        user = create_fresh_test_user()
        user["password"] = password_case["password"]
        user["confirm_password"] = password_case["confirm"]
        
        signup = SignupPage(sb)
        signup.open()
        signup.submit(user)
        
        sb.wait(1)
        assert "signup" in sb.get_current_url(), \
            f"Password case '{password_case['description']}' should be rejected"
    
    # Terms & Conditions Tests
    @pytest.mark.parametrize("toc_case", TOC_CASES)
    def test_03f_toc_validation(self, sb, toc_case):
        """❌ Terms & Conditions validation"""
        user = create_fresh_test_user()
        user["toc"] = toc_case["toc"]
        
        signup = SignupPage(sb)
        signup.open()
        signup.submit(user)
        
        sb.wait(1)
        assert "signup" in sb.get_current_url(), \
            f"T&C validation failed for: {toc_case['description']}"

