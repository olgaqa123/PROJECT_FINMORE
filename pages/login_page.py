from selenium.webdriver.common.by import By
from pages.base_page import BasePage
from config import BASE_URL
 
 
class LoginPage(BasePage):
 
    LOGIN_FORM = (By.CSS_SELECTOR, '[data-testid="login-form"]')
    EMAIL_INPUT = (By.CSS_SELECTOR, '[data-testid="login-email-input"]')
    PASSWORD_INPUT = (By.CSS_SELECTOR, '[data-testid="login-password-input"]')
    SUBMIT_BUTTON = (By.CSS_SELECTOR, '[data-testid="login-submit-button"]')
    REGISTER_SWITCH = (By.CSS_SELECTOR, '[data-testid="switch-to-register-button"]')
    USER_NAME_REGISTER = (By.CSS_SELECTOR, '[data-testid="user-menu-trigger"]')

 
    def open_login_page(self):
        self.open(BASE_URL)
 
    def wait_loaded_login_form(self):
        self.wait_visible(self.LOGIN_FORM)
 
    def enter_email(self, email):
        self.type(self.EMAIL_INPUT, email)
 
    def enter_password(self, password):
        self.type(self.PASSWORD_INPUT, password)
 
    def click_submit(self):
        self.click(self.SUBMIT_BUTTON)
 
    def click_register_switch(self):
        self.click(self.REGISTER_SWITCH)
 
    def login(self, email, password):
        self.enter_email(email)
        self.enter_password(password)
        self.click_submit()