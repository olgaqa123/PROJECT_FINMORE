from selenium.webdriver.common.by import By
from pages.base_page import BasePage
 
 
class RegisterPage(BasePage):
 
    REGISTER_FORM = (By.CSS_SELECTOR, '[data-testid="register-form"]')
    NAME_INPUT = (By.CSS_SELECTOR, '[data-testid="register-name-input"]')
    EMAIL_INPUT = (By.CSS_SELECTOR, '[data-testid="register-email-input"]')
    PASSWORD_INPUT = (By.CSS_SELECTOR, '[data-testid="register-password-input"]')
    CONFIRM_PASSWORD_INPUT = (By.CSS_SELECTOR, '[data-testid="register-confirm-password-input"]')
    SUBMIT_BUTTON = (By.CSS_SELECTOR, '[data-testid="register-submit-button"]')
    LOGIN_SWITCH = (By.CSS_SELECTOR, '[data-testid="switch-to-login-button"]')
 
    def wait_loaded_register_form(self):
        self.wait_visible(self.REGISTER_FORM)
 
    def fill_registration_form(self, name, email, password):
        self.type(self.NAME_INPUT, name)
        self.type(self.EMAIL_INPUT, email)
        self.type(self.PASSWORD_INPUT, password)
        self.type(self.CONFIRM_PASSWORD_INPUT, password)
 
    def submit(self):
        self.click(self.SUBMIT_BUTTON)
 
    def click_login_switch(self):
        self.click(self.LOGIN_SWITCH)

    def fill_registration_with_not_same_password_and_confirm_password(self, name, email, password1, password2):
        self.type(self.NAME_INPUT, name)
        self.type(self.EMAIL_INPUT, email)
        self.type(self.PASSWORD_INPUT, password1)
        self.type(self.CONFIRM_PASSWORD_INPUT, password2)    