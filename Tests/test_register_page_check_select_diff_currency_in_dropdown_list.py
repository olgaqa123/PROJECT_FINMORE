import pytest
from pages.base_page import BasePage
from pages.register_page import RegisterPage



def test_checking_changing_currency_on_register_page_VAR1(register_page):
    assert register_page.is_visible(register_page.CURRENCY_SELECT)
    register_page.click(register_page.CURRENCY_SELECT)

    register_page.is_visible(register_page.CURRENCY_OPTION_UAH)
    register_page.is_visible(register_page.CURRENCY_OPTION_USD)
    register_page.is_visible(register_page.CURRENCY_OPTION_EUR)
    register_page.is_visible(register_page.CURRENCY_OPTION_GBP)

    register_page.click(register_page.CURRENCY_OPTION_USD)
    assert register_page.get_value(register_page.CURRENCY_SELECT) == "USD"

    register_page.click(register_page.CURRENCY_SELECT)
    register_page.click(register_page.CURRENCY_OPTION_EUR)
    assert register_page.get_value(register_page.CURRENCY_SELECT) == "EUR"

    register_page.click(register_page.CURRENCY_SELECT)
    register_page.click(register_page.CURRENCY_OPTION_GBP)
    assert register_page.get_value(register_page.CURRENCY_SELECT) == "GBP"

    register_page.click(register_page.CURRENCY_SELECT)
    register_page.click(register_page.CURRENCY_OPTION_UAH)
    assert register_page.get_value(register_page.CURRENCY_SELECT) == "UAH"

    register_page.click(register_page.CURRENCY_SELECT)
    register_page.click(register_page.CURRENCY_OPTION_UAH)
    assert register_page.get_value(register_page.CURRENCY_SELECT) == "UAH"


def test_checking_changing_currency_on_register_page_VAR2(register_page):
    register_page.select_by_value(register_page.CURRENCY_SELECT, "USD")
    register_page.select_by_value(register_page.CURRENCY_SELECT, "EUR")
    register_page.select_by_value(register_page.CURRENCY_SELECT, "GBP")
    register_page.select_by_value(register_page.CURRENCY_SELECT, "UAH")
