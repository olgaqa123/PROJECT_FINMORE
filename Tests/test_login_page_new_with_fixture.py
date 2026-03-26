import pytest
from pages.dashbord_page import DashbordPage
from utils.data_loader import load_test_data
from pages.login_page import LoginPage
from config import EXPECTED_TITLE
 
 
data = load_test_data("login_data.json")

def test_login_page_load(login_page):
  
    assert EXPECTED_TITLE == login_page.get_title()
    assert login_page.is_visible(login_page.LOGIN_FORM)
 
 
def test_login_with_empty_fields(login_page):
    user = data["empty_user"]
 
    login_page.login(
        email=user["email"],
        password=user["password"]
    )
 
    assert login_page.get_value(login_page.EMAIL_INPUT) == ""
    assert login_page.get_value(login_page.PASSWORD_INPUT) == ""

    assert login_page.is_visible(login_page.LOGIN_FORM)
 
 
def test_login_with_valid_fields(dashbord_page):
    
    assert dashbord_page.is_visible(dashbord_page.USER_NAME_TRIGGER)