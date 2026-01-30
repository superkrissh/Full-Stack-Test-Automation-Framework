from src.core.base_page import BasePage
from src.locators.authentication_locators import MerchantAgreementLocators

class MerchantAgreementModal(BasePage):
    
    def is_agreement_shown(self):
        return self.sb.is_element_present(MerchantAgreementLocators.DIALOG)
    
    def accept(self):
        """Accept merchant agreement modal and redirect to orders page"""
        self.sb.wait_for_element(MerchantAgreementLocators.DIALOG, timeout=10)
        self.sb.click(MerchantAgreementLocators.MODAL_ACCEPT)
        # Wait for modal to disappear (page auto-redirects)
        self.sb.wait_for_element_not_visible(MerchantAgreementLocators.DIALOG, timeout=15)