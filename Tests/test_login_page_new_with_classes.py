import pytest
from pages.login_page import LoginPage
from config import EXPECTED_TITLE
 
 
def test_login_page_load(driver):
    page = LoginPage(driver)
    page.open_login_page()
    page.wait_loaded_login_form()
 
    assert EXPECTED_TITLE == page.get_title()
    assert page.is_visible(page.LOGIN_FORM)
 
 
def test_login_with_empty_fields(driver):
    page = LoginPage(driver)
    page.open_login_page()
    page.wait_loaded_login_form()
 
    page.click_submit()
 
    assert page.get_value(page.EMAIL_INPUT) == ""
    assert page.get_value(page.PASSWORD_INPUT) == ""