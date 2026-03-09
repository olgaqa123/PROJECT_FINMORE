from pages.login_page import LoginPage
from pages.register_page import RegisterPage
 
def test_register_with_empty_fields(driver):
    login_page = LoginPage(driver)
    login_page.open_login_page()
    login_page.wait_loaded_login_form()
    login_page.click_register_switch() 
    
    register_page = RegisterPage(driver)
    register_page.wait_loaded_register_form()

    register_page.submit()

    assert register_page.is_visible(register_page.REGISTER_FORM)
    assert register_page.get_value(register_page.NAME_INPUT) == ""
    assert register_page.get_value(register_page.EMAIL_INPUT) == ""
    assert register_page.get_value(register_page.PASSWORD_INPUT) == ""
    assert register_page.get_value(register_page.CONFIRM_PASSWORD_INPUT) == ""


def test_register_page_is_still_shown_if_register_with_empty_only_name(driver):
    login_page = LoginPage(driver)
    login_page.open_login_page()
    login_page.wait_loaded_login_form()
    login_page.click_register_switch()
 
    register_page = RegisterPage(driver)
    register_page.wait_loaded_register_form()
 
    register_page.fill_registration_form(
        name="",
        email="testuser123@gmail.com",
        password="password123"
    )
 
    register_page.submit()

    assert register_page.is_visible(register_page.REGISTER_FORM)
    assert register_page.get_value(register_page.NAME_INPUT) == ""
    assert register_page.get_value(register_page.EMAIL_INPUT) == "testuser123@gmail.com"
    assert register_page.get_value(register_page.PASSWORD_INPUT) == "password123"
    assert register_page.get_value(register_page.CONFIRM_PASSWORD_INPUT) == "password123"

def test_register_page_is_still_shown_if_register_with_empty_only_email(driver):
    login_page = LoginPage(driver)
    login_page.open_login_page()
    login_page.wait_loaded_login_form()
    login_page.click_register_switch()
 
    register_page = RegisterPage(driver)
    register_page.wait_loaded_register_form()
 
    register_page.fill_registration_form(
        name="Test User",
        email="",
        password="password123"
    )
 
    register_page.submit()

    assert register_page.is_visible(register_page.REGISTER_FORM)
    assert register_page.get_value(register_page.NAME_INPUT) == "Test User"
    assert register_page.get_value(register_page.EMAIL_INPUT) == ""
    assert register_page.get_value(register_page.PASSWORD_INPUT) == "password123"
    assert register_page.get_value(register_page.CONFIRM_PASSWORD_INPUT) == "password123"

def test_register_page_is_still_shown_if_register_with_empty_only_password(driver):
    login_page = LoginPage(driver)
    login_page.open_login_page()
    login_page.wait_loaded_login_form()
    login_page.click_register_switch()
 
    register_page = RegisterPage(driver)
    register_page.wait_loaded_register_form()
 
    register_page.fill_registration_form(
        name="Test User",
        email="testuser123@gmail.com",
        password=""
    )
 
    register_page.submit()

    assert register_page.is_visible(register_page.REGISTER_FORM)
    assert register_page.get_value(register_page.NAME_INPUT) == "Test User"
    assert register_page.get_value(register_page.EMAIL_INPUT) == "testuser123@gmail.com"
    assert register_page.get_value(register_page.PASSWORD_INPUT) == ""
    assert register_page.get_value(register_page.CONFIRM_PASSWORD_INPUT) == ""

def test_register_page_is_still_shown_if_register_with_empty_only_confirm_password(driver):
    login_page = LoginPage(driver)
    login_page.open_login_page()
    login_page.wait_loaded_login_form()
    login_page.click_register_switch()
 
    register_page = RegisterPage(driver)
    register_page.wait_loaded_register_form()
 
    register_page.fill_registration_with_not_same_password_and_confirm_password(
        name = "Test User",
        email = "testuser123@gmail.com",
        password1 = "password123",
        password2 = ""
    )
 
    register_page.submit()

    assert register_page.is_visible(register_page.REGISTER_FORM)
    assert register_page.get_value(register_page.NAME_INPUT) == "Test User"
    assert register_page.get_value(register_page.EMAIL_INPUT) == "testuser123@gmail.com"
    assert register_page.get_value(register_page.PASSWORD_INPUT) == "password123"
    assert register_page.get_value(register_page.CONFIRM_PASSWORD_INPUT) == ""

def test_register_page_is_still_shown_if_register_with_not_valid_email1(driver):
    login_page = LoginPage(driver)
    login_page.open_login_page()
    login_page.wait_loaded_login_form()
    login_page.click_register_switch()
 
    register_page = RegisterPage(driver)
    register_page.wait_loaded_register_form()
 
    register_page.fill_registration_form(
        name = "Test User",
        email = "@gmail.com",
        password = "password123"
    )
 
    register_page.submit()

    assert register_page.is_visible(register_page.REGISTER_FORM)
    assert register_page.get_value(register_page.NAME_INPUT) == "Test User"
    assert register_page.get_value(register_page.EMAIL_INPUT) == "@gmail.com"
    assert register_page.get_value(register_page.PASSWORD_INPUT) == "password123"
    assert register_page.get_value(register_page.CONFIRM_PASSWORD_INPUT) == "password123"

def test_register_page_is_still_shown_if_register_with_not_valid_email2(driver):
    login_page = LoginPage(driver)
    login_page.open_login_page()
    login_page.wait_loaded_login_form()
    login_page.click_register_switch()
 
    register_page = RegisterPage(driver)
    register_page.wait_loaded_register_form()
 
    register_page.fill_registration_form(
        name = "Test User",
        email = "testuser123@",
        password = "password123"
    )
 
    register_page.submit()

    assert register_page.is_visible(register_page.REGISTER_FORM)
    assert register_page.get_value(register_page.NAME_INPUT) == "Test User"
    assert register_page.get_value(register_page.EMAIL_INPUT) == "testuser123@"
    assert register_page.get_value(register_page.PASSWORD_INPUT) == "password123"
    assert register_page.get_value(register_page.CONFIRM_PASSWORD_INPUT) == "password123"

def test_register_page_is_still_shown_if_register_with_not_valid_email3(driver):
    login_page = LoginPage(driver)
    login_page.open_login_page()
    login_page.wait_loaded_login_form()
    login_page.click_register_switch()
 
    register_page = RegisterPage(driver)
    register_page.wait_loaded_register_form()
 
    register_page.fill_registration_form(
        name = "Test User",
        email = "testuser123gmail.com",
        password = "password123"
    )
 
    register_page.submit()

    assert register_page.is_visible(register_page.REGISTER_FORM)
    assert register_page.get_value(register_page.NAME_INPUT) == "Test User"
    assert register_page.get_value(register_page.EMAIL_INPUT) == "testuser123gmail.com"
    assert register_page.get_value(register_page.PASSWORD_INPUT) == "password123"
    assert register_page.get_value(register_page.CONFIRM_PASSWORD_INPUT) == "password123"

def test_register_page_is_still_shown_if_register_with_not_valid_email4(driver):
    login_page = LoginPage(driver)
    login_page.open_login_page()
    login_page.wait_loaded_login_form()
    login_page.click_register_switch()
 
    register_page = RegisterPage(driver)
    register_page.wait_loaded_register_form()
 
    register_page.fill_registration_form(
        name = "Test User",
        email = "testuser123@gggggggggggggg.com",
        password = "password123"
    )
 
    register_page.submit()

    assert register_page.is_visible(register_page.REGISTER_FORM)
    assert register_page.get_value(register_page.NAME_INPUT) == "Test User"
    assert register_page.get_value(register_page.EMAIL_INPUT) == "testuser123@gggggggggggggg.com"
    assert register_page.get_value(register_page.PASSWORD_INPUT) == "password123"
    assert register_page.get_value(register_page.CONFIRM_PASSWORD_INPUT) == "password123"

def test_register_page_is_still_shown_if_register_with_not_valid_email5(driver):
    login_page = LoginPage(driver)
    login_page.open_login_page()
    login_page.wait_loaded_login_form()
    login_page.click_register_switch()
 
    register_page = RegisterPage(driver)
    register_page.wait_loaded_register_form()
 
    register_page.fill_registration_form(
        name = "Test User",
        email = "gmail.com",
        password = "password123"
    )
 
    register_page.submit()

    assert register_page.is_visible(register_page.REGISTER_FORM)
    assert register_page.get_value(register_page.NAME_INPUT) == "Test User"
    assert register_page.get_value(register_page.EMAIL_INPUT) == "gmail.com"
    assert register_page.get_value(register_page.PASSWORD_INPUT) == "password123"
    assert register_page.get_value(register_page.CONFIRM_PASSWORD_INPUT) == "password123"

def test_register_page_is_still_shown_if_register_with_not_valid_password_when_only_one_character(driver):
    login_page = LoginPage(driver)
    login_page.open_login_page()
    login_page.wait_loaded_login_form()
    login_page.click_register_switch()
 
    register_page = RegisterPage(driver)
    register_page.wait_loaded_register_form()
 
    register_page.fill_registration_form(
        name = "Test User",
        email = "testuser123@gmail.com",
        password = "p"
    )
 
    register_page.submit()

    assert register_page.is_visible(register_page.REGISTER_FORM)
    assert register_page.get_value(register_page.NAME_INPUT) == "Test User"
    assert register_page.get_value(register_page.EMAIL_INPUT) == "testuser123@gmail.com"
    assert register_page.get_value(register_page.PASSWORD_INPUT) == "p"
    assert register_page.get_value(register_page.CONFIRM_PASSWORD_INPUT) == "p"

def test_register_page_is_still_shown_if_register_with_not_valid_password_when_less_than_6_character(driver):
    login_page = LoginPage(driver)
    login_page.open_login_page()
    login_page.wait_loaded_login_form()
    login_page.click_register_switch()
 
    register_page = RegisterPage(driver)
    register_page.wait_loaded_register_form()
 
    register_page.fill_registration_form(
        name = "Test User",
        email = "testuser123@gmail.com",
        password = "p1234"
    )
 
    register_page.submit()

    assert register_page.is_visible(register_page.REGISTER_FORM)
    assert register_page.get_value(register_page.NAME_INPUT) == "Test User"
    assert register_page.get_value(register_page.EMAIL_INPUT) == "testuser123@gmail.com"
    assert register_page.get_value(register_page.PASSWORD_INPUT) == "p1234"
    assert register_page.get_value(register_page.CONFIRM_PASSWORD_INPUT) == "p1234"

def test_register_page_is_still_shown_if_register_with_not_valid_confirm_password(driver):
    login_page = LoginPage(driver)
    login_page.open_login_page()
    login_page.wait_loaded_login_form()
    login_page.click_register_switch()
 
    register_page = RegisterPage(driver)
    register_page.wait_loaded_register_form()
 
    register_page.fill_registration_with_not_same_password_and_confirm_password(
        name = "Test User",
        email = "testuser123@gmail.com",
        password1 = "password123",
        password2 = "abcd1234a"
    )

    register_page.submit()

    assert register_page.is_visible(register_page.REGISTER_FORM)
    assert register_page.get_value(register_page.NAME_INPUT) == "Test User"
    assert register_page.get_value(register_page.EMAIL_INPUT) == "testuser123@gmail.com"
    assert register_page.get_value(register_page.PASSWORD_INPUT) == "password123"
    assert register_page.get_value(register_page.CONFIRM_PASSWORD_INPUT) == "abcd1234a"