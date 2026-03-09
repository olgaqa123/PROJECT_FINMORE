from pages.login_page import LoginPage
from pages.register_page import RegisterPage
from utils.data_generator import generate_email
 

 
def test_register_with_valid_data(driver):
    login_page = LoginPage(driver)
    login_page.open_login_page()
    login_page.wait_loaded_login_form()
    login_page.click_register_switch()
 
    register_page = RegisterPage(driver)
    register_page.wait_loaded_register_form()
 
    register_page.fill_registration_form(
        name="Test User",
        email = generate_email(),
        password="password123"
    )
 
    register_page.submit()