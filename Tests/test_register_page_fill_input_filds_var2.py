from Tests.data.register_data import REGISTER_EMAIL, REGISTER_NAME, REGISTER_PASSWORD
from pages.login_page import LoginPage
from pages.register_page import RegisterPage
 

 
def test_register_with_valid_data(driver):
    login_page = LoginPage(driver)
    login_page.open_login_page()
    login_page.wait_loaded_login_form()
    login_page.click_register_switch()
 
    register_page = RegisterPage(driver)
    register_page.wait_loaded_register_form()
 
    register_page.fill_registration_form(
        name = REGISTER_NAME,
        email = REGISTER_EMAIL,
        password = REGISTER_PASSWORD
    )
 
    register_page.submit()