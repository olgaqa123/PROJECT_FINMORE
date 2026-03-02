from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
 
 
BASE_URL = "https://finmore.netlify.app/"
EXPECTED_TITLE_PART = "Повнофункціональний фінансовий менеджер"
LOGIN_TITLE = '[data-testid="login-title"]'
LOGIN_FORM = '[data-testid="login-form"]'
EMAIL_INPUT = '[data-testid="login-email-input"]'
PASSWORD_INPUT = '[data-testid="login-password-input"]'
SUBMIT_BUTTON = '[data-testid="login-submit-button"]'
TOGGLE_PASSWORD = '[data-testid="toggle-password-visibility"]'
REGISTER_BUTTON = '[data-testid="switch-to-register-button"]'

GREEN_CIRCLE_UNDER_LOGO = "div.rounded-full "
LOGO_ICON = "svg.lucide-log-in"

FIRST_TEXT_AT_THE_TOP = '//h1[text()="Вхід до системи"]'
SECOND_TEXT_AT_THE_TOP = '//p[text()="Увійдіть до свого облікового запису"]'

EMAIL_ADDRESS_TEXT = '//label[text()="Email адреса"]'
ENVELOP_ICON = "svg.lucide-mail"
EMAIL_ADDRESS_PLACEHOLDER = "your@email.com"

PASSWORD_TEXT = '//label[text()="Пароль"]'
LOCK_ICON = "svg.lucide-lock"
PASSWORD_PLACEHOLDER = "Введіть пароль"

TEXT_LOGIN_INSIDE_SUBMIT_BUTTON = '//button[text()="Увійти"]'

DEVIDER_LINE = "div.mt-8"

TEXT_FOR_HYPERTEXT_ZAREESTRUVATIS = '//button[text()="Зареєструватися"]'

TEXT_NEMAE_OBLIC_ZAPUS = '//p[text()="Немає облікового запису?"]'
TEXT_DEMO_OBLIC_ZAPUS = '//p[text()="Демо облікові записи:"]'
TEXT_DEMO_OBLIC_EMAIL = '//p[text()="admin@demo.com / admin123"]'
TEXT_DEMO_OBLIC_PASSWORD = '//p[text()="user@demo.com / user123"]'


def test_correct_url_is_opened(driver):
    driver.get(BASE_URL)
 
    WebDriverWait(driver, 10).until(
        lambda d: d.current_url.startswith(BASE_URL)
    )
 
    assert driver.current_url.startswith(BASE_URL)
 


def test_page_title_is_correct(driver):
    driver.get(BASE_URL)
 
    WebDriverWait(driver, 10).until(
        lambda d: d.title != ""
    )
 
    assert EXPECTED_TITLE_PART == driver.title



def test_login_form_is_visible(driver):
    driver.get(BASE_URL)
 
    WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, LOGIN_FORM))
    )
 
 #For checking logo ICON and green circle at the top of page: 
    assert driver.find_element(By.CSS_SELECTOR, LOGO_ICON).is_displayed()
    #For checking green circle under logo ICON:
    assert driver.find_element(By.CSS_SELECTOR, GREEN_CIRCLE_UNDER_LOGO).is_displayed()

 #For checking text "Вхід до системи":
    assert driver.find_element(By.CSS_SELECTOR, LOGIN_TITLE).is_displayed()
    #Checking that text is exectly "Вхід до системи":
    assert driver.find_element(By.XPATH, FIRST_TEXT_AT_THE_TOP).is_displayed()
 #For checking second text "Увійдіть до свого облікового запису":  
    assert driver.find_element(By.XPATH, SECOND_TEXT_AT_THE_TOP).is_displayed()


 #For checking that present section (form) on page thich have data-testid="login-form" 
 #(it`s section on page which have form with address, passord and submit button):
    assert driver.find_element(By.CSS_SELECTOR, LOGIN_FORM).is_displayed()

 #For checking in form text "Email адреса": 
    assert driver.find_element(By.XPATH, EMAIL_ADDRESS_TEXT).is_displayed()
 #For checking in form email input field:  
    assert driver.find_element(By.CSS_SELECTOR, EMAIL_INPUT).is_displayed()
 #For checking in form envelop ICON in email input field:  
    assert driver.find_element(By.CSS_SELECTOR, ENVELOP_ICON).is_displayed()
 #For checking in form placeholder "your@email.com" in email input field:  
    actual_email_placeholder = driver.find_element(By.CSS_SELECTOR, EMAIL_INPUT).get_attribute("placeholder")
    assert actual_email_placeholder == EMAIL_ADDRESS_PLACEHOLDER, f" Очікувався '{EMAIL_ADDRESS_PLACEHOLDER}', але отримано '{actual_email_placeholder}'"
    print(f"Placeholder вірний: '{actual_email_placeholder}'")

 #For checking in form text "Пароль": 
    assert driver.find_element(By.XPATH, PASSWORD_TEXT).is_displayed()
 #For checking in form password input field:  
    assert driver.find_element(By.CSS_SELECTOR, PASSWORD_INPUT).is_displayed()
 #For checking in form lock ICON in password input field: 
    assert driver.find_element(By.CSS_SELECTOR, LOCK_ICON).is_displayed()
 #For checking in form placeholder "Введіть пароль" in password input field:  
    actual_password_placeholder = driver.find_element(By.CSS_SELECTOR, PASSWORD_INPUT).get_attribute("placeholder")
    assert actual_password_placeholder == PASSWORD_PLACEHOLDER, f" Очікувався '{PASSWORD_PLACEHOLDER}', але отримано '{actual_password_placeholder}'"
    print(f"Placeholder вірний: '{actual_password_placeholder}'")
 #For checking in form password visibility button (eye ICON) in password input field: 
    assert driver.find_element(By.CSS_SELECTOR, TOGGLE_PASSWORD).is_displayed()

 #For checking in form submit button:
    assert driver.find_element(By.CSS_SELECTOR, SUBMIT_BUTTON).is_displayed()
    #Checking that text is exectly "Увійти":
    assert driver.find_element(By.XPATH, TEXT_LOGIN_INSIDE_SUBMIT_BUTTON).is_displayed()


  #For checking text "Немає облікового запису?":
    assert driver.find_element(By.XPATH, TEXT_NEMAE_OBLIC_ZAPUS).is_displayed()
 #For checking hypertext (type button) "Зареєструватися":
    assert driver.find_element(By.CSS_SELECTOR, REGISTER_BUTTON).is_displayed()
    #Checking that text is exectly "Зареєструватися":
    assert driver.find_element(By.XPATH, TEXT_FOR_HYPERTEXT_ZAREESTRUVATIS).is_displayed()
 
 
 #For checking that present DEVIDER line:  
    assert driver.find_element(By.CSS_SELECTOR, DEVIDER_LINE).is_displayed()

    
 #For checking text "Демо облікові записи:":
    assert driver.find_element(By.XPATH, TEXT_DEMO_OBLIC_ZAPUS).is_displayed()
 #For checking text for demo email "admin@demo.com / admin123":
    assert driver.find_element(By.XPATH, TEXT_DEMO_OBLIC_EMAIL).is_displayed()
 #For checking text for demo password "user@demo.com / user123":
    assert driver.find_element(By.XPATH, TEXT_DEMO_OBLIC_PASSWORD).is_displayed()



def test_login_with_empty_fields(driver):
    driver.get(BASE_URL)
 
    driver.find_element(By.CSS_SELECTOR, SUBMIT_BUTTON).click()
 
    email = driver.find_element(By.CSS_SELECTOR, EMAIL_INPUT)
    password = driver.find_element(By.CSS_SELECTOR, PASSWORD_INPUT)
 
    assert email.get_attribute("value") == ""
    assert password.get_attribute("value") == ""