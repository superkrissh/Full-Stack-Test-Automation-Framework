class SignupLocators:
    FIRST_NAME = "input[name='firstName']"
    LAST_NAME = "input[name='lastName']"
    MOBILE = "input[name='mobile']"
    EMAIL = "input[name='email']"
    PASSWORD = "input[name='password']"
    CONFIRM_PASSWORD = "input[name='confirmPassword']"
    REFERRAL_CODE = "input[name='referral_code']"
    TNC = "#toc"
    SUBMIT = "#sign_up_submit"
    ERROR = ".error-message"


class LoginLocators:
    EMAIL = "input[name='email']"
    PASSWORD = "input[name='password']"
    SUBMIT = "#kt_sign_in_submit"
    ERROR = ".error-message"


class MobileVerificationLocators:
    PAGE_TITLE = "h1"
    VERIFIED_MESSAGE = "text:Mobile verified"


class MerchantAgreementLocators:
    DIALOG = "[role='alertdialog']"
    MODAL_ACCEPT = "button[type='submit']:contains('Accept')"
    TITLE = "h2"


