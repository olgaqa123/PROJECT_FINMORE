from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
 
 
class BasePage:
 
    def __init__(self, driver, timeout=10):
        self.driver = driver
        self.wait = WebDriverWait(driver, timeout)
 
    def open(self, url):
        self.driver.get(url)
 
    def find(self, locator):
        return self.driver.find_element(*locator)
 
    def wait_visible(self, locator):
        return self.wait.until(
            EC.visibility_of_element_located(locator)
        )
 
    def click(self, locator):
        self.wait_visible(locator).click()
 
    def type(self, locator, text):
        element = self.wait_visible(locator)
        element.clear()
        element.send_keys(text)
 
    def get_value(self, locator):
        return self.find(locator).get_attribute("value")
 
    def is_visible(self, locator):
        return self.wait_visible(locator).is_displayed()
 
    def get_title(self):
        return self.driver.title