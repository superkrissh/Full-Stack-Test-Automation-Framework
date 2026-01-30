import os
from dotenv import load_dotenv
from src.core.base_page import BasePage
from src.locators.authentication_locators import SignupLocators

# Load .env file
load_dotenv()

# Read BASE_URL directly from .env
BASE_URL = os.getenv("BASE_URL", "https://dev.v.shipgl.in")

class SignupPage(BasePage):
    def open(self):
        """Open signup page at https://dev.v.shipgl.in/auth/signup"""
        self.sb.open(f"{BASE_URL}/auth/signup")
        # Wait for form to load
        self.sb.wait_for_element(SignupLocators.FIRST_NAME, timeout=15)

    def refresh_form(self):
        """Refresh page to reset form for next test case (same page, multiple tests)
        
        Use this when testing multiple validation cases on the same page.
        Example: Test 5 different invalid emails without reopening browser.
        """
        self.sb.refresh()
        # Wait for form to load after refresh
        self.sb.wait_for_element(SignupLocators.FIRST_NAME, timeout=10)

    def submit(self, user):
        """Fill signup form and submit - redirects to mobile verification page"""
        self.sb.type(SignupLocators.FIRST_NAME, user.get("first_name", ""))
        self.sb.type(SignupLocators.LAST_NAME, user.get("last_name", ""))
        self.sb.type(SignupLocators.MOBILE, user.get("mobile", ""))
        self.sb.type(SignupLocators.EMAIL, user.get("email", ""))
        self.sb.type(SignupLocators.PASSWORD, user.get("password", ""))
        self.sb.type(SignupLocators.CONFIRM_PASSWORD, user.get("confirm_password", ""))
        
        if user.get("referral_code"):
            self.sb.type(SignupLocators.REFERRAL_CODE, user.get("referral_code"))

        # Check T&C checkbox
        if user.get("toc"):
            self.sb.click(SignupLocators.TNC)

        # Click submit button
        self.sb.click(SignupLocators.SUBMIT)
        # Wait for redirect to mobile verification page
        self.sb.wait(3)

    def assert_error(self, text):
        """Assert error message appears on signup page"""
        self.sb.assert_text(text, SignupLocators.ERROR)