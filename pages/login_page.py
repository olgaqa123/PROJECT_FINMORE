from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
 
 
class LoginPage:
 
    URL = "https://finmore.netlify.app/"
 
    LOGIN_FORM = (By.CSS_SELECTOR, '[data-testid="login-form"]')
    EMAIL_INPUT = (By.CSS_SELECTOR, '[data-testid="login-email-input"]')
    PASSWORD_INPUT = (By.CSS_SELECTOR, '[data-testid="login-password-input"]')
    SUBMIT_BUTTON = (By.CSS_SELECTOR, '[data-testid="login-submit-button"]')
 
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)
 
    def open(self):
        self.driver.get(self.URL)
 
    def wait_for_page_loaded(self):
        self.wait.until(
            EC.visibility_of_element_located(self.LOGIN_FORM)
        )
 
    def get_title(self):
        return self.driver.title
 
    def is_login_form_visible(self):
        return self.driver.find_element(*self.LOGIN_FORM).is_displayed()
 
    def click_submit(self):
        self.driver.find_element(*self.SUBMIT_BUTTON).click()
 
    def get_email_value(self):
        return self.driver.find_element(*self.EMAIL_INPUT).get_attribute("value")
 
    def get_password_value(self):
        return self.driver.find_element(*self.PASSWORD_INPUT).get_attribute("value")