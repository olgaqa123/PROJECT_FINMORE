from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pages.register_page import RegisterPage
 
 
BASE_URL = "https://finmore.netlify.app/"
EXPECTED_TITLE_PART = "Повнофункціональний фінансовий менеджер"
REGISTER_BUTTON = '[data-testid="switch-to-register-button"]'

#Constants with data-testid on register page:
REGISTER_PAGE = '[data-testid="register-page"]'
REGISTER_TITLE = '[data-testid="register-title"]'
REGISTER_FORM = '[data-testid="register-form"]'
REGISTER_NAME_INPUT = '[data-testid="register-name-input"]'
REGISTER_EMAIL_INPUT = '[data-testid="register-email-input"]'
REGISTER_PASSWORD_INPUT = '[data-testid="register-password-input"]'
TOGGLE_PASSWORD = '[data-testid="toggle-password-visibility"]'
REGISTER_CONFIRM_PASSWORD_INPUT = '[data-testid="register-confirm-password-input"]'
TOGGLE_CONFIRM_PASSWORD = '[data-testid="toggle-confirm-password-visibility"]'
REGISTER_CURRENCY_SELECT = '[data-testid="register-currency-select"]'
REGISTER_CURRENCY_OPTION_UAH = '[data-testid="currency-option-UAH"]'
REGISTER_CURRENCY_OPTION_USD = '[data-testid="currency-option-USD"]'
REGISTER_CURRENCY_OPTION_EUR = '[data-testid="currency-option-EUR"]'
REGISTER_CURRENCY_OPTION_GBP = '[data-testid="currency-option-GBP"]'
REGISTER_SUBMIT_BUTTON = '[data-testid="register-submit-button"]'
LOGIN_BUTTON = '[data-testid="switch-to-login-button"]'

BLUE_CIRCLE_UNDER_LOGO = "div.rounded-full "
LOGO_ICON_ON_REGISTER_PAGE = "svg.lucide-user-plus"

FIRST_TEXT_AT_THE_TOP_OF_REGISTER_PAGE = '//h1[text()="Реєстрація"]'
SECOND_TEXT_AT_THE_TOP_OF_REGISTER_PAGE = '//p[text()="Створіть новий обліковий запис"]'

FULL_NAME_ON_REGISTER_PAGE = '//label[text()="Повне ім\'я"]'
USER_ICON_ON_REGISTER_PAGE = "svg.lucide-user"
USER_PLACEHOLDER_ON_REGISTER_PAGE = "Іван Петренко"

EMAIL_ADDRESS_TEXT_ON_REGISTER_PAGE = '//label[text()="Email адреса"]'
ENVELOP_ICON_ON_REGISTER_PAGE = "svg.lucide-mail"
EMAIL_ADDRESS_PLACEHOLDER_ON_REGISTER_PAGE = "your@email.com"

PASSWORD_TEXT_ON_REGISTER_PAGE = '//label[text()="Пароль"]'
LOCK_ICON_ON_REGISTER_PAGE = "svg.lucide-lock"
PASSWORD_PLACEHOLDER_ON_REGISTER_PAGE = "Мінімум 6 символів"

CONFIRM_PASSWORD_TEXT_ON_REGISTER_PAGE = '//label[text()="Підтвердження паролю"]'
CONFIRM_LOCK_ICON_ON_REGISTER_PAGE = "svg.lucide-lock"
CONFIRM_PASSWORD_PLACEHOLDER_ON_REGISTER_PAGE = "Повторіть пароль"

TEXT_REGISTER_INSIDE_SUBMIT_BUTTON = '//button[text()="Зареєструватися"]'


TEXT_VZHE_E_OBLIK_ZAPUS = '//p[text()="Вже маєте обліковий запис?"]'
TEXT_FOR_HYPERTEXT_UVITI = '//button[text()="Увійти"]'


def test_register_page_elements_are_visible(driver):
    driver.get(BASE_URL)

    driver.find_element(By.CSS_SELECTOR, REGISTER_BUTTON).click()
 
    WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, REGISTER_FORM))
    )
 
 #For checking logo ICON and blue circle at the top of register page: 
    assert driver.find_element(By.CSS_SELECTOR, LOGO_ICON_ON_REGISTER_PAGE).is_displayed()
    #For checking blue circle under logo ICON:
    assert driver.find_element(By.CSS_SELECTOR, BLUE_CIRCLE_UNDER_LOGO).is_displayed()

 #For checking text "Реєстрація":
    assert driver.find_element(By.CSS_SELECTOR, REGISTER_TITLE).is_displayed()
    #Checking that text is exectly "Реєстрація":
    assert driver.find_element(By.XPATH, FIRST_TEXT_AT_THE_TOP_OF_REGISTER_PAGE).is_displayed()
 #For checking second text "Створіть новий обліковий запис":  
    assert driver.find_element(By.XPATH, FIRST_TEXT_AT_THE_TOP_OF_REGISTER_PAGE).is_displayed()
 
 #For checking that present section (form) on register page thich have data-testid="register-form" 
 #(it`s section on register page which have form with full name, address, passord, confirm password, currency and register submit button):
    assert driver.find_element(By.CSS_SELECTOR, REGISTER_FORM).is_displayed()

#For checking in register form text "Повне ім'я": 
    assert driver.find_element(By.XPATH, FULL_NAME_ON_REGISTER_PAGE).is_displayed()
 #For checking in register form name input field:  
    assert driver.find_element(By.CSS_SELECTOR, REGISTER_NAME_INPUT).is_displayed()
 #For checking in register form user ICON in namr input field:  
    assert driver.find_element(By.CSS_SELECTOR, USER_ICON_ON_REGISTER_PAGE).is_displayed()
 #For checking in register form placeholder "Іван Петренко" in name input field:  
    actual_name_placeholder = driver.find_element(By.CSS_SELECTOR, REGISTER_NAME_INPUT).get_attribute("placeholder")
    assert actual_name_placeholder == USER_PLACEHOLDER_ON_REGISTER_PAGE


 #For checking in register form text "Email адреса": 
    assert driver.find_element(By.XPATH, EMAIL_ADDRESS_TEXT_ON_REGISTER_PAGE).is_displayed()
 #For checking in register form email input field:  
    assert driver.find_element(By.CSS_SELECTOR, REGISTER_EMAIL_INPUT).is_displayed()
 #For checking in register form envelop ICON in email input field:  
    assert driver.find_element(By.CSS_SELECTOR, ENVELOP_ICON_ON_REGISTER_PAGE).is_displayed()
 #For checking in register form placeholder "your@email.com" in email input field:  
    actual_email_placeholder = driver.find_element(By.CSS_SELECTOR, REGISTER_EMAIL_INPUT).get_attribute("placeholder")
    assert actual_email_placeholder == EMAIL_ADDRESS_PLACEHOLDER_ON_REGISTER_PAGE

 #For checking in register form text "Пароль": 
    assert driver.find_element(By.XPATH, PASSWORD_TEXT_ON_REGISTER_PAGE).is_displayed()
 #For checking in register form password input field:  
    assert driver.find_element(By.CSS_SELECTOR, REGISTER_PASSWORD_INPUT).is_displayed()
 #For checking in register form lock ICON in password input field: 
    assert driver.find_element(By.CSS_SELECTOR, LOCK_ICON_ON_REGISTER_PAGE).is_displayed()
 #For checking in register form placeholder "Введіть пароль" in password input field:  
    actual_password_placeholder = driver.find_element(By.CSS_SELECTOR, REGISTER_PASSWORD_INPUT).get_attribute("placeholder")
    assert actual_password_placeholder == PASSWORD_PLACEHOLDER_ON_REGISTER_PAGE
 #For checking in register form password visibility button (eye ICON) in password input field: 
    assert driver.find_element(By.CSS_SELECTOR, TOGGLE_PASSWORD).is_displayed()

 #For checking in register form text "Підтвердження паролю": 
    assert driver.find_element(By.XPATH, CONFIRM_PASSWORD_TEXT_ON_REGISTER_PAGE).is_displayed()
 #For checking in register form confirm password input field:  
    assert driver.find_element(By.CSS_SELECTOR, REGISTER_CONFIRM_PASSWORD_INPUT).is_displayed()
 #For checking in register form present lock ICON in confirm password input field: 
    assert driver.find_element(By.CSS_SELECTOR, CONFIRM_LOCK_ICON_ON_REGISTER_PAGE).is_displayed()
 #For checking in register form placeholder "Повторіть пароль" in confirm password input field:  
    actual_confirm_password_placeholder = driver.find_element(By.CSS_SELECTOR, REGISTER_CONFIRM_PASSWORD_INPUT).get_attribute("placeholder")
    assert actual_confirm_password_placeholder == CONFIRM_PASSWORD_PLACEHOLDER_ON_REGISTER_PAGE
 #For checking in register form password visibility button (eye ICON) in confirm password input field: 
    assert driver.find_element(By.CSS_SELECTOR, REGISTER_CONFIRM_PASSWORD_INPUT).is_displayed()


 #For checking in register form register submit button:
    assert driver.find_element(By.CSS_SELECTOR, REGISTER_SUBMIT_BUTTON).is_displayed()
    #Checking that text is exectly "Зареєструватися":
    assert driver.find_element(By.XPATH, TEXT_REGISTER_INSIDE_SUBMIT_BUTTON).is_displayed()

 #For checking text "Вже маєте обліковий запис??":
    assert driver.find_element(By.XPATH, TEXT_VZHE_E_OBLIK_ZAPUS).is_displayed()
 #For checking hypertext (type button) "Увійти":
    assert driver.find_element(By.CSS_SELECTOR, LOGIN_BUTTON).is_displayed()
    #Checking that text is exectly "Увійти":
    assert driver.find_element(By.XPATH, TEXT_FOR_HYPERTEXT_UVITI).is_displayed()
 

