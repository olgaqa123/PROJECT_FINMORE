import pytest
from pages.login_page import LoginPage
from pages.register_page import RegisterPage
 
 
@pytest.fixture
def register_page(driver):
 
    login_page = LoginPage(driver)
    login_page.open_login_page()
    login_page.wait_loaded_login_form()
    login_page.click_register_switch()
 
    register_page = RegisterPage(driver)
    register_page.wait_loaded_register_form()
 
    return register_page