from src.core.base_page import BasePage
from src.locators.authentication_locators import LoginLocators
from configs.settings import BASE_URL

class LoginPage(BasePage):

    def open(self):
        self.sb.open(f"{BASE_URL}/auth/login")
        # Wait for form to load
        self.sb.wait_for_element(LoginLocators.EMAIL, timeout=15)

    def login(self, email, password):
        """Login with email and password credentials"""
        self.sb.type(LoginLocators.EMAIL, email)
        self.sb.type(LoginLocators.PASSWORD, password)
        self.sb.click(LoginLocators.SUBMIT)
        # Wait for merchant agreement modal or redirect
        self.sb.wait(2)
    
    def assert_error(self, text):
        self.sb.assert_text(text, LoginLocators.ERROR)
