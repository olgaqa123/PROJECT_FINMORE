import pytest
from Tests.data import register_data as data
 
 
def test_register_with_empty_fields(register_page):
 
    register_page.fill_registration_form(

        name=data.REGISTER_NAME_EMPTY,

        email=data.REGISTER_EMAIL_EMPTY,

        password=data.REGISTER_PASSWORD_EMPTY

    )
 
    register_page.submit()
 
    assert register_page.is_visible(register_page.REGISTER_FORM)
 
 
@pytest.mark.parametrize("name, email, password", [

    ("", data.REGISTER_EMAIL, data.REGISTER_PASSWORD),

    (data.REGISTER_NAME, "", data.REGISTER_PASSWORD),

    (data.REGISTER_NAME, data.REGISTER_EMAIL, ""),
    
    ("", "", data.REGISTER_PASSWORD),
    (data.REGISTER_NAME, "", ""),
    ("", data.REGISTER_EMAIL, ""),

])

def test_register_with_empty_required_fields(register_page, name, email, password):
 
    register_page.fill_registration_form(

        name=name,

        email=email,

        password=password

    )
 
    register_page.submit()
 
    assert register_page.is_visible(register_page.REGISTER_FORM)
 
 
@pytest.mark.parametrize("email", data.REGISTER_EMAIL_INVALID)

def test_register_with_invalid_email(register_page, email):
 
    register_page.fill_registration_form(

        name=data.REGISTER_NAME,

        email=email,

        password=data.REGISTER_PASSWORD

    )
 
    register_page.submit()
 
    assert register_page.is_visible(register_page.REGISTER_FORM)
 
 
@pytest.mark.parametrize("password", data.REGISTER_PASSWORD_INVALID)

def test_register_with_invalid_password(register_page, password):
 
    register_page.fill_registration_form(

        name=data.REGISTER_NAME,

        email=data.REGISTER_EMAIL,

        password=password

    )
 
    register_page.submit()
 
    assert register_page.is_visible(register_page.REGISTER_FORM)
 
 
def test_register_with_empty_confirm_password(register_page):
 
    register_page.fill_registration_form(

        name=data.REGISTER_NAME,

        email=data.REGISTER_EMAIL,

        password=data.REGISTER_PASSWORD,

        confirm_password=data.CONFIRM_REGISTER_PASSWORD_EMPTY

    )
 
    register_page.submit()
 
    assert register_page.is_visible(register_page.REGISTER_FORM)
 
 
def test_register_with_not_matching_password(register_page):
 
    register_page.fill_registration_form(

        name=data.REGISTER_NAME,

        email=data.REGISTER_EMAIL,

        password=data.REGISTER_PASSWORD,

        confirm_password=data.CONFIRM_REGISTER_PASSWORD_INVALID

    )
 
    register_page.submit()
 
    assert register_page.is_visible(register_page.REGISTER_FORM)
    assert register_page.get_value(register_page.NAME_INPUT) == data.REGISTER_NAME
    assert register_page.get_value(register_page.EMAIL_INPUT) == data.REGISTER_EMAIL
    assert register_page.get_value(register_page.PASSWORD_INPUT) == data.REGISTER_PASSWORD
    assert register_page.get_value(register_page.CONFIRM_PASSWORD_INPUT) == data.CONFIRM_REGISTER_PASSWORD_INVALID
    assert register_page.is_visible(register_page.CONFIRM_PASSWORD_ERROR_TEXT)

 