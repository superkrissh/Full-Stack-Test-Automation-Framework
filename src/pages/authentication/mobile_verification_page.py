import os
from dotenv import load_dotenv
from src.core.base_page import BasePage

# Load .env file
load_dotenv()

# Read BASE_URL directly from .env
BASE_URL = os.getenv("BASE_URL", "https://dev.v.shipgl.in")


class MobileVerificationPage(BasePage):
    """Mobile verification page at https://dev.v.shipgl.in/verify-mobile
    
    User lands here after signup. While on this page:
    - Test framework updates DB to set mobile_verified = 1
    - User then needs to logout and go to login page
    """

    def is_on_verify_page(self):
        """Check if user is on mobile verification page"""
        # Check for URL that indicates we're on verify-mobile page
        current_url = self.sb.get_current_url()
        return "verify-mobile" in current_url
    
    def wait_for_page_load(self, timeout=15):
        """Wait for mobile verification page to fully load"""
        self.sb.wait(2)  # Wait for page to load
        return self.is_on_verify_page()
    
    def logout_and_navigate_to_login(self):
        """Logout from mobile verification page and navigate to login
        
        Flow:
        1. Navigate to logout URL: https://dev.v.shipgl.in/logout
        2. Then navigate to login page: https://dev.v.shipgl.in/auth/login
        
        This completes the flow: signup → mobile verification → DB update → logout → login
        """
        
        # Step 1: Navigate to logout URL - server handles logout
        logout_url = BASE_URL + "/logout"
        self.sb.open(logout_url)
        
        # Step 2: Navigate to login page (page loads automatically)
        login_url = BASE_URL + "/auth/login"
        self.sb.open(login_url)
