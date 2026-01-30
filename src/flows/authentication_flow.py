import os
from dotenv import load_dotenv
from src.pages.authentication.login_page import LoginPage
from src.pages.authentication.mobile_verification_page import MobileVerificationPage
from src.pages.authentication.signup_page import SignupPage
from src.pages.authentication.merchant_agreement_modal import MerchantAgreementModal

# Load .env file
load_dotenv()

# Read BASE_URL directly from .env - NO settings.py layer
BASE_URL = os.getenv("BASE_URL", "https://dev.v.shipgl.in")


class AuthenticationFlow:
    """
    Complete Authentication Flow:
    1. Signup with valid data → User redirected to mobile verification page
    2. Update DB: mobile_verified = 1 (simulating OTP verification)
    3. Logout from mobile verification page
    4. Login with same credentials
    5. Accept merchant agreement modal
    6. Verify orders page is loaded
    """

    def __init__(self, sb):
        self.sb = sb
        self.signup = SignupPage(sb)
        self.login = LoginPage(sb)
        self.mobile = MobileVerificationPage(sb)
        self.agreement = MerchantAgreementModal(sb)

    def step_1_signup(self, user):
        """Step 1: Signup - Open signup page and submit form
        
        Flow:
        - Opens: https://dev.v.shipgl.in/auth/signup
        - Fills: First Name, Last Name, Mobile, Email, Password, Confirm Password
        - Checks: Terms & Conditions checkbox
        - Clicks: Create Account button
        - Redirects to: https://dev.v.shipgl.in/verify-mobile
        
        Args:
            user (dict): User data with first_name, last_name, email, mobile, password, toc
        """
        self.signup.open()
        self.signup.submit(user)
        # Verify user is on mobile verification page
        assert self.mobile.is_on_verify_page(), "User was not redirected to mobile verification page"
        print(f"✅ Step 1 Complete: User signed up with email {user['email']}")

    def step_2_wait_and_verify_mobile_page(self):
        """Step 2: Wait on mobile verification page
        
        While on this page, test framework will:
        - Update DB: mobile_verified = 1 for the user's email
        - This simulates OTP verification in test environment
        """
        self.mobile.wait_for_page_load()
        print("✅ Step 2 Complete: Waited on mobile verification page (DB should be updated)")

    def step_3_logout_and_navigate_to_login(self):
        """Step 3: Logout and navigate to login page
        
        Flow:
        - Logs out from mobile verification page using: https://dev.v.shipgl.in/logout
        - Navigates to login page: https://dev.v.shipgl.in/auth/login
        """
        self.mobile.logout_and_navigate_to_login()
        # Verify user is on login page
        assert "auth/login" in self.sb.get_current_url(), "User was not navigated to login page"
        print("✅ Step 3 Complete: Logged out and navigated to login page")

    def step_4_login(self, email, password):
        """Step 4: Login - Enter credentials and submit
        
        Flow:
        - Opens: https://dev.v.shipgl.in/auth/login (already there from step 3)
        - Fills: Email (from signup)
        - Fills: Password (from signup)
        - Clicks: Submit button
        - Merchant agreement modal appears
        
        Args:
            email (str): User email
            password (str): User password
        """
        self.login.login(email, password)
        print(f"✅ Step 4 Complete: Logged in with email {email}")

    def step_5_accept_merchant_agreement(self):
        """Step 5: Accept merchant agreement modal
        
        Flow:
        - Modal appears after login
        - User reads merchant agreement (v19.0)
        - Clicks: Accept button
        - User is now fully authenticated
        """
        self.agreement.accept()
        print("✅ Step 5 Complete: Merchant agreement accepted")

    def step_6_verify_orders_page(self):
        """Step 6: Verify user is on orders page
        
        Flow:
        - After accepting merchant agreement, user should be redirected to orders
        - Expected URL: https://dev.v.shipgl.in/orders/all
        """
        # Wait for orders page element to confirm page load
        self.sb.wait_for_element("a[href*='order']", timeout=10)
        current_url = self.sb.get_current_url()
        assert "orders" in current_url, f"Expected orders page, but got {current_url}"
        print(f"✅ Step 6 Complete: Verified orders page loaded - {current_url}")
