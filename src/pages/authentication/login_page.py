import os
from dotenv import load_dotenv
from src.core.base_page import BasePage
from src.locators.authentication_locators import LoginLocators

# Load .env file
load_dotenv()

# Read BASE_URL directly from .env
BASE_URL = os.getenv("BASE_URL", "https://dev.v.shipgl.in")

class LoginPage(BasePage):

    def open(self):
        self.sb.open(f"{BASE_URL}/auth/login")
        # Wait for form to load
        self.sb.wait_for_element(LoginLocators.EMAIL, timeout=15)

    def refresh_form(self):
        """Refresh page to reset form for next test case (same page, multiple tests)
        
        Use this when testing multiple validation cases on the same page.
        Example: Test 5 different invalid passwords without reopening browser.
        """
        self.sb.refresh()
        # Wait for form to load after refresh
        self.sb.wait_for_element(LoginLocators.EMAIL, timeout=10)

    def login(self, email, password):
        """Login with email and password credentials"""
        self.sb.type(LoginLocators.EMAIL, email)
        self.sb.type(LoginLocators.PASSWORD, password)
        self.sb.click(LoginLocators.SUBMIT)
        # Browser auto-redirects - next page's wait_for_element handles readiness
    
    def assert_error(self, text):
        self.sb.assert_text(text, LoginLocators.ERROR)
