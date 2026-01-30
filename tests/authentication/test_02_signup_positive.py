"""
✅ SIGNUP POSITIVE TEST - Valid signup with all fields

Simple flow:
1. Generate random email + mobile
2. Fill signup form with these values
3. Check if redirected to verify-mobile page
"""
from src.pages.authentication.signup_page import SignupPage
from src.utils.session import create_fresh_test_user


class TestSignupPositive:
    """Test: Valid signup form submission"""
    
    def test_02_signup_with_valid_data(self, sb):
        """✅ User can signup with valid data"""
        
        # STEP 1: Create random user data
        # Function: create_fresh_test_user() (from src/utils/session.py)
        # Returns: dict with email, mobile, password, first_name, last_name
        user = create_fresh_test_user()
        
        # STEP 2: Show what values we got
        print(f"\n--- Test Data Generated ---")
        print(f"First Name: {user['first_name']}")      # e.g., "John"
        print(f"Last Name: {user['last_name']}")        # e.g., "Doe"
        print(f"Email: {user['email']}")                # e.g., "auto_1704067200000_xyz@gmail.in"
        print(f"Mobile: {user['mobile']}")              # e.g., "9876543210"
        print(f"Password: {user['password']}")          # e.g., "Test@1234"
        
        # STEP 3: Create SignupPage object
        # SignupPage class: from src/pages/authentication/signup_page.py
        signup = SignupPage(sb)
        
        # STEP 4: Open signup page
        # This goes to: https://dev.v.shipgl.in/auth/signup
        signup.open()
        print(f"\n--- Page Opened ---")
        print(f"URL: {sb.get_current_url()}")
        
        # STEP 5: Fill form and submit
        # signup.submit() fills all fields with user data and clicks submit button
        signup.submit(user)
        print(f"\n--- Form Submitted ---")
        print(f"Filled: First Name, Last Name, Email, Mobile, Password, Confirm Password")
        print(f"Clicked: Submit Button")
        
        # STEP 6: Check page redirected to verify-mobile
        current_url = sb.get_current_url()
        print(f"\n--- Result Check ---")
        print(f"Current URL: {current_url}")
        
        # If URL contains "verify-mobile", test passes
        # If NOT, test fails
        assert "verify-mobile" in current_url, \
            f"FAILED: Expected to go to verify-mobile page, but got {current_url}"
        
        print(f"✅ SUCCESS: Redirected to mobile verification page!")


