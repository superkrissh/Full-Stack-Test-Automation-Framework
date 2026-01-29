"""
❌ LOGIN NEGATIVE TEST CASES (Form Validation)

Simple test data objects - 8 validation test cases organized by field
Each case tests ONE validation scenario

Expected: Form stays on login page (validation rejects invalid credentials)

Easy to add new tests:
- Add new dict to the appropriate CASES list
- Pytest will run it automatically with @pytest.mark.parametrize
"""
import pytest
from src.pages.authentication.login_page import LoginPage


# ============================================================================
# TEST DATA - 8 LOGIN VALIDATION TEST CASES (Dictionary Format)
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
    {"email": "", "password": "", "description": "Empty"},
    {"email": "invalidemail", "password": "short", "description": "Invalid"},
]


# ============================================================================
# TEST IMPLEMENTATION
# ============================================================================
class TestLoginNegative:
    """Test: Form validation rejects invalid login data"""
    
    # Email Tests
    @pytest.mark.parametrize("email_case", EMAIL_CASES)
    def test_05a_email_validation(self, sb, email_case):
        """❌ Email validation - test each case"""
        login = LoginPage(sb)
        login.open()
        login.login(email_case["email"], email_case["password"])
        
        sb.wait(1)
        assert "login" in sb.get_current_url(), \
            f"Email validation failed for: {email_case['description']}"
    
    # Password Tests
    @pytest.mark.parametrize("password_case", PASSWORD_CASES)
    def test_05b_password_validation(self, sb, password_case):
        """❌ Password validation - test each case"""
        login = LoginPage(sb)
        login.open()
        login.login(password_case["email"], password_case["password"])
        
        sb.wait(1)
        assert "login" in sb.get_current_url(), \
            f"Password validation failed for: {password_case['description']}"
    
    # Both Fields Invalid Tests
    @pytest.mark.parametrize("both_case", BOTH_INVALID_CASES)
    def test_05c_both_fields_validation(self, sb, both_case):
        """❌ Multiple fields validation - test each case"""
        login = LoginPage(sb)
        login.open()
        login.login(both_case["email"], both_case["password"])
        
        sb.wait(1)
        assert "login" in sb.get_current_url(), \
            f"Both fields validation failed for: {both_case['description']}"

