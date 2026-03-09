from pages.login_page import LoginPage
from pages.register_page import RegisterPage
 
 

TEST_NAME = "Test User"
TEST_EMAIL = "testuser123@gmail.com"
TEST_PASSWORD = "password123"
 
 
def test_register_with_valid_data(driver):
    login_page = LoginPage(driver)
    login_page.open_login_page()
    login_page.wait_loaded_login_form()
    login_page.click_register_switch()
 
    register_page = RegisterPage(driver)
    register_page.wait_loaded_register_form()
 
    register_page.fill_registration_form(
        name=TEST_NAME,
        email=TEST_EMAIL,
        password=TEST_PASSWORD
    )
 
    register_page.submit()