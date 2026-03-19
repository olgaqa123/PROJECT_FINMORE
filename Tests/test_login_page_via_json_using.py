import pytest
from pages.dashbord_page import DashbordPage
from utils.data_loader import load_test_data
from pages.login_page import LoginPage
from config import EXPECTED_TITLE
 
 
data = load_test_data("login_data.json")

def test_login_page_load(driver):
    page = LoginPage(driver)
    page.open_login_page()
    page.wait_loaded_login_form()
 
    assert EXPECTED_TITLE == page.get_title()
    assert page.is_visible(page.LOGIN_FORM)
 
 
def test_login_with_empty_fields(driver):
    user = data["empty_user"]
 
    page = LoginPage(driver)
    page.open_login_page()
    page.wait_loaded_login_form()
 
    page.login(
        email=user["email"],
        password=user["password"]
    )
 
    assert page.get_value(page.EMAIL_INPUT) == ""
    assert page.get_value(page.PASSWORD_INPUT) == ""

    assert page.is_visible(page.LOGIN_FORM)
 
 
def test_login_with_valid_fields(driver):
    user = data["valid_user"]
 
    page = LoginPage(driver)
    page.open_login_page()
    page.wait_loaded_login_form()
 
    page.login(
        email=user["email"],
        password=user["password"]
    )
    dashbord_page = DashbordPage(driver)
    assert dashbord_page.is_visible(dashbord_page.USER_NAME_TRIGGER)