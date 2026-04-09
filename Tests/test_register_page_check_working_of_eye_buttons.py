import pytest
from Tests.data.register_data import REGISTER_PASSWORD
from pages.base_page import BasePage
from pages.register_page import RegisterPage



# Test case for checking working of eye/cross eye button in PASSWORD field:
def test_check_working_of_eye_button_for_password_on_register_page(register_page):
    
    # 1 Checking that by default after open registration form  type = password and shown eye button
    assert register_page.find(register_page.PASSWORD_INPUT).get_attribute("type") == "password"
    assert register_page.find(register_page.TOGGLE_PASSWORD_VISIBILITY).get_attribute("aria-label") == "Show password"

    # 2 Input in passworg field some characters and check that no changes for type (mean shown dots instead of characters) and still shown eye button
    register_page.fill(register_page.PASSWORD_INPUT, REGISTER_PASSWORD)
    assert register_page.find(register_page.PASSWORD_INPUT).get_attribute("type") == "password"
    assert register_page.find(register_page.TOGGLE_PASSWORD_VISIBILITY).get_attribute("aria-label") == "Show password"
    
    # 3 Click on  eye icon button inside password field:
    register_page.click(register_page.TOGGLE_PASSWORD_VISIBILITY)
    
    # 4 Chack that type changed to text (mean characters shown instead of dots in password field) and shown cross eye button:
    assert register_page.find(register_page.PASSWORD_INPUT).get_attribute("type") == "text"
    assert register_page.find(register_page.TOGGLE_PASSWORD_VISIBILITY).get_attribute("aria-label") == "Hide password"

    # 5 Click on  cross eye icon button inside password field:
    register_page.click(register_page.TOGGLE_PASSWORD_VISIBILITY)

    # 6 Chack that type changed to password (mean instead characters shown dots in password field) and shown eye icon button:
    assert register_page.find(register_page.PASSWORD_INPUT).get_attribute("type") == "password"
    assert register_page.find(register_page.TOGGLE_PASSWORD_VISIBILITY).get_attribute("aria-label") == "Show password"



# Test case for checking working of eye/cross eye button in CONFIRM PASSWORD field:
def test_checkworking_of_eye_button_for_confirm_password_on_register_page(register_page):
    
    # 1 Checking that by default after open registration form  type = password and shown eye button
    assert register_page.find(register_page.CONFIRM_PASSWORD_INPUT).get_attribute("type") == "password"
    assert register_page.find(register_page.TOGGLE_CONFIRM_PASSWORD_VISIBILITY).get_attribute("aria-label") == "Show password"

    # 2 Input in confirm passworg field some characters and check that no changes for type (mean shown dots instead of characters) and still shown eye button
    register_page.fill(register_page.CONFIRM_PASSWORD_INPUT, REGISTER_PASSWORD)
    assert register_page.find(register_page.CONFIRM_PASSWORD_INPUT).get_attribute("type") == "password"
    assert register_page.find(register_page.TOGGLE_CONFIRM_PASSWORD_VISIBILITY).get_attribute("aria-label") == "Show password"
    
    # 3 Click on  eye icon button inside confirm password field:
    register_page.click(register_page.TOGGLE_CONFIRM_PASSWORD_VISIBILITY)
    
    # 4 Chack that type changed to text (mean characters shown instead of dots in confirm password field) and shown cross eye button:
    assert register_page.find(register_page.CONFIRM_PASSWORD_INPUT).get_attribute("type") == "text"
    assert register_page.find(register_page.TOGGLE_CONFIRM_PASSWORD_VISIBILITY).get_attribute("aria-label") == "Hide password"

    # 5 Click on  cross eye icon button inside confirm password field:
    register_page.click(register_page.TOGGLE_CONFIRM_PASSWORD_VISIBILITY)

    # 6 Chack that type changed to password (mean instead characters shown dots in confirm password field) and shown eye icon button:
    assert register_page.find(register_page.CONFIRM_PASSWORD_INPUT).get_attribute("type") == "password"
    assert register_page.find(register_page.TOGGLE_CONFIRM_PASSWORD_VISIBILITY).get_attribute("aria-label") == "Show password"

   
