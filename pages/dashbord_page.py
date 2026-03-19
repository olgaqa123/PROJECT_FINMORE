from selenium.webdriver.common.by import By
from pages.base_page import BasePage
from config import BASE_URL
 
 
class DashbordPage(BasePage):
 
    USER_NAME_TRIGGER = (By.CSS_SELECTOR, '[data-testid="user-menu-trigger"]')