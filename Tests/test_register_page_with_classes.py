from pages.login_page import LoginPage
from pages.register_page import RegisterPage
 
 
def test_register_page_open(driver):
    login_page = LoginPage(driver)
    login_page.open_login_page()
    login_page.wait_loaded_login_form()
    login_page.click_register_switch()
 
    register_page = RegisterPage(driver)
    register_page.wait_loaded_register_form()
 
    assert register_page.is_visible(register_page.REGISTER_FORM)
 
 
def test_register_with_valid_data(driver):
    login_page = LoginPage(driver)
    login_page.open_login_page()
    login_page.wait_loaded_login_form()
    login_page.click_register_switch()
 
    register_page = RegisterPage(driver)
    register_page.wait_loaded_register_form()
 
    register_page.fill_registration_form(
        name="Test User",
        email="testuser123@gmail.com",
        password="password123"
    )
 
    register_page.submit()