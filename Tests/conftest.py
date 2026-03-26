import pytest
from Tests.data.login_data import LOGIN_EMAIL, LOGIN_PASSWORD
from pages.login_page import LoginPage
from pages.register_page import RegisterPage
from pages.dashbord_page import DashbordPage
from utils.data_loader import load_test_data
 
 
@pytest.fixture
def register_page(driver):
 
    login_page = LoginPage(driver)
    login_page.open_login_page()
    login_page.wait_loaded_login_form()
    login_page.click_register_switch()
 
    register_page = RegisterPage(driver)
    register_page.wait_loaded_register_form()
 
    return register_page

@pytest.fixture
def login_page(driver):
 
    page = LoginPage(driver)
    page.open_login_page()
    page.wait_loaded_login_form()
 
    return page


@pytest.fixture
def dashbord_page(driver):
    page = LoginPage(driver)
    page.open_login_page()
    page.wait_loaded_login_form()
 
    page.login(
        email = LOGIN_EMAIL,
        password = LOGIN_PASSWORD
    )
    dashbordpage = DashbordPage(driver)
    return dashbordpage