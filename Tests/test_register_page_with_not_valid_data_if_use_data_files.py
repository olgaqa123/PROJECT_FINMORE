from Tests.data.register_data import CONFIRM_REGISTER_PASSWORD_EMPTY, CONFIRM_REGISTER_PASSWORD_INVALID, REGISTER_EMAIL, REGISTER_EMAIL_EMPTY, REGISTER_EMAIL_INVALID1, REGISTER_EMAIL_INVALID2, REGISTER_EMAIL_INVALID3, REGISTER_EMAIL_INVALID4, REGISTER_EMAIL_INVALID5, REGISTER_NAME, REGISTER_NAME_EMPTY, REGISTER_PASSWORD, REGISTER_PASSWORD_EMPTY, REGISTER_PASSWORD_INVALID1, REGISTER_PASSWORD_INVALID2, CONFIRM_REGISTER_PASSWORD_INVALID
from pages.login_page import LoginPage
from pages.register_page import RegisterPage
 
def test_register_with_empty_fields(driver):
    login_page = LoginPage(driver)
    login_page.open_login_page()
    login_page.wait_loaded_login_form()
    login_page.click_register_switch() 
    
    register_page = RegisterPage(driver)
    register_page.wait_loaded_register_form()

    register_page.fill_registration_form(
        name = REGISTER_NAME_EMPTY,
        email = REGISTER_EMAIL_EMPTY,
        password = REGISTER_PASSWORD_EMPTY
    )

    register_page.submit()

    assert register_page.is_visible(register_page.REGISTER_FORM)
    assert register_page.get_value(register_page.NAME_INPUT) == REGISTER_NAME_EMPTY
    assert register_page.get_value(register_page.EMAIL_INPUT) == REGISTER_EMAIL_EMPTY
    assert register_page.get_value(register_page.PASSWORD_INPUT) == REGISTER_PASSWORD_EMPTY
    assert register_page.get_value(register_page.CONFIRM_PASSWORD_INPUT) == REGISTER_PASSWORD_EMPTY


def test_register_page_is_still_shown_if_register_with_empty_only_name(driver):
    login_page = LoginPage(driver)
    login_page.open_login_page()
    login_page.wait_loaded_login_form()
    login_page.click_register_switch()
 
    register_page = RegisterPage(driver)
    register_page.wait_loaded_register_form()
 
    register_page.fill_registration_form(
        name = REGISTER_NAME_EMPTY,
        email = REGISTER_EMAIL,
        password = REGISTER_PASSWORD
    )
 
    register_page.submit()

    assert register_page.is_visible(register_page.REGISTER_FORM)
    assert register_page.get_value(register_page.NAME_INPUT) == REGISTER_NAME_EMPTY
    assert register_page.get_value(register_page.EMAIL_INPUT) == REGISTER_EMAIL
    assert register_page.get_value(register_page.PASSWORD_INPUT) == REGISTER_PASSWORD
    assert register_page.get_value(register_page.CONFIRM_PASSWORD_INPUT) == REGISTER_PASSWORD

def test_register_page_is_still_shown_if_register_with_empty_only_email(driver):
    login_page = LoginPage(driver)
    login_page.open_login_page()
    login_page.wait_loaded_login_form()
    login_page.click_register_switch()
 
    register_page = RegisterPage(driver)
    register_page.wait_loaded_register_form()
 
    register_page.fill_registration_form(
        name = REGISTER_NAME,
        email = REGISTER_EMAIL_EMPTY,
        password = REGISTER_PASSWORD
    )
 
    register_page.submit()

    assert register_page.is_visible(register_page.REGISTER_FORM)
    assert register_page.get_value(register_page.NAME_INPUT) == REGISTER_NAME
    assert register_page.get_value(register_page.EMAIL_INPUT) == REGISTER_EMAIL_EMPTY
    assert register_page.get_value(register_page.PASSWORD_INPUT) == REGISTER_PASSWORD
    assert register_page.get_value(register_page.CONFIRM_PASSWORD_INPUT) == REGISTER_PASSWORD

def test_register_page_is_still_shown_if_register_with_empty_only_password(driver):
    login_page = LoginPage(driver)
    login_page.open_login_page()
    login_page.wait_loaded_login_form()
    login_page.click_register_switch()
 
    register_page = RegisterPage(driver)
    register_page.wait_loaded_register_form()
 
    register_page.fill_registration_form(
        name = REGISTER_NAME,
        email = REGISTER_EMAIL,
        password = REGISTER_PASSWORD_EMPTY
    )
 
    register_page.submit()

    assert register_page.is_visible(register_page.REGISTER_FORM)
    assert register_page.get_value(register_page.NAME_INPUT) == REGISTER_NAME
    assert register_page.get_value(register_page.EMAIL_INPUT) == REGISTER_EMAIL
    assert register_page.get_value(register_page.PASSWORD_INPUT) == REGISTER_PASSWORD_EMPTY
    assert register_page.get_value(register_page.CONFIRM_PASSWORD_INPUT) == REGISTER_PASSWORD_EMPTY

def test_register_page_is_still_shown_if_register_with_empty_only_confirm_password(driver):
    login_page = LoginPage(driver)
    login_page.open_login_page()
    login_page.wait_loaded_login_form()
    login_page.click_register_switch()
 
    register_page = RegisterPage(driver)
    register_page.wait_loaded_register_form()
 
    register_page.fill_registration_with_not_same_password_and_confirm_password(
        name = REGISTER_NAME,
        email = REGISTER_EMAIL,
        password1 = REGISTER_PASSWORD,
        password2 = CONFIRM_REGISTER_PASSWORD_EMPTY
    )
 
    register_page.submit()

    assert register_page.is_visible(register_page.REGISTER_FORM)
    assert register_page.get_value(register_page.NAME_INPUT) == REGISTER_NAME
    assert register_page.get_value(register_page.EMAIL_INPUT) == REGISTER_EMAIL
    assert register_page.get_value(register_page.PASSWORD_INPUT) == REGISTER_PASSWORD
    assert register_page.get_value(register_page.CONFIRM_PASSWORD_INPUT) == CONFIRM_REGISTER_PASSWORD_EMPTY

def test_register_page_is_still_shown_if_register_with_not_valid_email1(driver):
    login_page = LoginPage(driver)
    login_page.open_login_page()
    login_page.wait_loaded_login_form()
    login_page.click_register_switch()
 
    register_page = RegisterPage(driver)
    register_page.wait_loaded_register_form()
 
    register_page.fill_registration_form(
        name = REGISTER_NAME,
        email = REGISTER_EMAIL_INVALID1,
        password = REGISTER_PASSWORD
    )
 
    register_page.submit()

    assert register_page.is_visible(register_page.REGISTER_FORM)
    assert register_page.get_value(register_page.NAME_INPUT) == REGISTER_NAME
    assert register_page.get_value(register_page.EMAIL_INPUT) == REGISTER_EMAIL_INVALID1
    assert register_page.get_value(register_page.PASSWORD_INPUT) == REGISTER_PASSWORD
    assert register_page.get_value(register_page.CONFIRM_PASSWORD_INPUT) == REGISTER_PASSWORD

def test_register_page_is_still_shown_if_register_with_not_valid_email2(driver):
    login_page = LoginPage(driver)
    login_page.open_login_page()
    login_page.wait_loaded_login_form()
    login_page.click_register_switch()
 
    register_page = RegisterPage(driver)
    register_page.wait_loaded_register_form()
 
    register_page.fill_registration_form(
        name = REGISTER_NAME,
        email = REGISTER_EMAIL_INVALID2,
        password = REGISTER_PASSWORD
    )
 
    register_page.submit()

    assert register_page.is_visible(register_page.REGISTER_FORM)
    assert register_page.get_value(register_page.NAME_INPUT) == REGISTER_NAME
    assert register_page.get_value(register_page.EMAIL_INPUT) == REGISTER_EMAIL_INVALID2
    assert register_page.get_value(register_page.PASSWORD_INPUT) == REGISTER_PASSWORD
    assert register_page.get_value(register_page.CONFIRM_PASSWORD_INPUT) == REGISTER_PASSWORD

def test_register_page_is_still_shown_if_register_with_not_valid_email3(driver):
    login_page = LoginPage(driver)
    login_page.open_login_page()
    login_page.wait_loaded_login_form()
    login_page.click_register_switch()
 
    register_page = RegisterPage(driver)
    register_page.wait_loaded_register_form()
 
    register_page.fill_registration_form(
        name = REGISTER_NAME,
        email = REGISTER_EMAIL_INVALID3,
        password = REGISTER_PASSWORD
    )
 
    register_page.submit()

    assert register_page.is_visible(register_page.REGISTER_FORM)
    assert register_page.get_value(register_page.NAME_INPUT) == REGISTER_NAME
    assert register_page.get_value(register_page.EMAIL_INPUT) == REGISTER_EMAIL_INVALID3
    assert register_page.get_value(register_page.PASSWORD_INPUT) == REGISTER_PASSWORD
    assert register_page.get_value(register_page.CONFIRM_PASSWORD_INPUT) == REGISTER_PASSWORD

def test_register_page_is_still_shown_if_register_with_not_valid_email4(driver):
    login_page = LoginPage(driver)
    login_page.open_login_page()
    login_page.wait_loaded_login_form()
    login_page.click_register_switch()
 
    register_page = RegisterPage(driver)
    register_page.wait_loaded_register_form()
 
    register_page.fill_registration_form(
        name = REGISTER_NAME,
        email = REGISTER_EMAIL_INVALID4,
        password = REGISTER_PASSWORD
    )
 
    register_page.submit()

    assert register_page.is_visible(register_page.REGISTER_FORM)
    assert register_page.get_value(register_page.NAME_INPUT) == REGISTER_NAME
    assert register_page.get_value(register_page.EMAIL_INPUT) == REGISTER_EMAIL_INVALID4
    assert register_page.get_value(register_page.PASSWORD_INPUT) == REGISTER_PASSWORD
    assert register_page.get_value(register_page.CONFIRM_PASSWORD_INPUT) == REGISTER_PASSWORD

def test_register_page_is_still_shown_if_register_with_not_valid_email5(driver):
    login_page = LoginPage(driver)
    login_page.open_login_page()
    login_page.wait_loaded_login_form()
    login_page.click_register_switch()
 
    register_page = RegisterPage(driver)
    register_page.wait_loaded_register_form()
 
    register_page.fill_registration_form(
        name = REGISTER_NAME,
        email = REGISTER_EMAIL_INVALID5,
        password = REGISTER_PASSWORD
    )
 
    register_page.submit()

    assert register_page.is_visible(register_page.REGISTER_FORM)
    assert register_page.get_value(register_page.NAME_INPUT) == REGISTER_NAME
    assert register_page.get_value(register_page.EMAIL_INPUT) == REGISTER_EMAIL_INVALID5
    assert register_page.get_value(register_page.PASSWORD_INPUT) == REGISTER_PASSWORD
    assert register_page.get_value(register_page.CONFIRM_PASSWORD_INPUT) == REGISTER_PASSWORD

def test_register_page_is_still_shown_if_register_with_not_valid_password_when_only_one_character(driver):
    login_page = LoginPage(driver)
    login_page.open_login_page()
    login_page.wait_loaded_login_form()
    login_page.click_register_switch()
 
    register_page = RegisterPage(driver)
    register_page.wait_loaded_register_form()
 
    register_page.fill_registration_form(
        name = REGISTER_NAME,
        email = REGISTER_EMAIL,
        password = REGISTER_PASSWORD_INVALID1
    )
 
    register_page.submit()

    assert register_page.is_visible(register_page.REGISTER_FORM)
    assert register_page.get_value(register_page.NAME_INPUT) == REGISTER_NAME
    assert register_page.get_value(register_page.EMAIL_INPUT) == REGISTER_EMAIL
    assert register_page.get_value(register_page.PASSWORD_INPUT) == REGISTER_PASSWORD_INVALID1
    assert register_page.get_value(register_page.CONFIRM_PASSWORD_INPUT) == REGISTER_PASSWORD_INVALID1

def test_register_page_is_still_shown_if_register_with_not_valid_password_when_less_than_6_character(driver):
    login_page = LoginPage(driver)
    login_page.open_login_page()
    login_page.wait_loaded_login_form()
    login_page.click_register_switch()
 
    register_page = RegisterPage(driver)
    register_page.wait_loaded_register_form()
 
    register_page.fill_registration_form(
        name = REGISTER_NAME,
        email = REGISTER_EMAIL,
        password = REGISTER_PASSWORD_INVALID2
    )
 
    register_page.submit()

    assert register_page.is_visible(register_page.REGISTER_FORM)
    assert register_page.get_value(register_page.NAME_INPUT) == REGISTER_NAME
    assert register_page.get_value(register_page.EMAIL_INPUT) == REGISTER_EMAIL
    assert register_page.get_value(register_page.PASSWORD_INPUT) == REGISTER_PASSWORD_INVALID2
    assert register_page.get_value(register_page.CONFIRM_PASSWORD_INPUT) == REGISTER_PASSWORD_INVALID2

def test_register_page_is_still_shown_if_register_with_not_valid_confirm_password(driver):
    login_page = LoginPage(driver)
    login_page.open_login_page()
    login_page.wait_loaded_login_form()
    login_page.click_register_switch()
 
    register_page = RegisterPage(driver)
    register_page.wait_loaded_register_form()
 
    register_page.fill_registration_with_not_same_password_and_confirm_password(
        name = REGISTER_NAME,
        email = REGISTER_EMAIL,
        password1 = REGISTER_PASSWORD,
        password2 = CONFIRM_REGISTER_PASSWORD_INVALID
    )

    register_page.submit()

    assert register_page.is_visible(register_page.REGISTER_FORM)
    assert register_page.get_value(register_page.NAME_INPUT) == REGISTER_NAME
    assert register_page.get_value(register_page.EMAIL_INPUT) == REGISTER_EMAIL
    assert register_page.get_value(register_page.PASSWORD_INPUT) == REGISTER_PASSWORD
    assert register_page.get_value(register_page.CONFIRM_PASSWORD_INPUT) == CONFIRM_REGISTER_PASSWORD_INVALID