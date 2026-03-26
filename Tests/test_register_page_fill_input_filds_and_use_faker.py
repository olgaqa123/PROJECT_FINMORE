from pages.login_page import LoginPage
from pages.register_page import RegisterPage
from faker import Faker
 
 
#Test  via using faker №1 : 
# UA (Ukraine), domain exectly  "gmail.com", password with 10 characters WITOUT numbers and at list 1 character in password is lower character
fake = Faker("uk_UA")
 
def generate_user():
    return {
        "name": fake.name(),
        "email": fake.email(domain="gmail.com"),
        "password": fake.password(length=10, digits=False, lower_case=True)
    }

def test_register_with_valid_data1(register_page):
    user = generate_user()
 
    register_page.fill_registration_form(
        name=user["name"],
        email=user["email"],
        password=user["password"]
    )

    register_page.submit()

    print(f"Name: {user['name']}")
    print(f"Email: {user['email']}")
    print(f"Password: {user['password']}")

#Test  via using faker №2 : 
# JP (Japan), domain is any , password with length=20, no special characters, no upper characters

def generate_user2():
    fake = Faker("ja_JP")
    return {
        "name": fake.name(),
        "email": fake.email(),
        "password": fake.password(length=20, special_chars=False, upper_case=False)
    }

def test_register_with_valid_data2(register_page):
    user = generate_user2()
 
    register_page.fill_registration_form(
        name=user["name"],
        email=user["email"],
        password=user["password"]
    )

    register_page.submit()

    print(f"Name: {user['name']}")
    print(f"Email: {user['email']}")
    print(f"Password: {user['password']}")
    
#Test  via using faker №3 : 
# CN (China), domain is any , password -  with length=30, no numbers, present special characters, present upper characters, no lower characters

def generate_user3():
    fake = Faker("zh_CN")
    allowed_domains = ['gmail.com', 'ukr.net', 'outlook.com', 'icloud.com']
    return {
        "name": fake.name(),
        "email": f"{fake.user_name()}@{fake.random_element(allowed_domains)}",
        "password": fake.password(length=30, digits=False, special_chars=True, upper_case=True, lower_case=False)
    }

def test_register_with_valid_data3(register_page):
    user = generate_user3()
 
    register_page.fill_registration_form(
        name=user["name"],
        email=user["email"],
        password=user["password"]
    )

    register_page.submit()

    print(f"Name: {user['name']}")
    print(f"Email: {user['email']}")
    print(f"Password: {user['password']}")    