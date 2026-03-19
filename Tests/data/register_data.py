#REGISTER_NAME = "Test User"
#REGISTER_EMAIL = "testuser123@gmail.com"
#REGISTER_PASSWORD = "password123"


#variants for name, email, password for checking negative cases

#REGISTER_NAME_EMPTY = ""
#REGISTER_EMAIL_EMPTY = ""
#REGISTER_PASSWORD_EMPTY = ""
#CONFIRM_REGISTER_PASSWORD_EMPTY = ""
REGISTER_EMAIL_INVALID1 = "@gmail.com"    #if no name in email
REGISTER_EMAIL_INVALID2 = "testuser123@"  #if not present email domen
REGISTER_EMAIL_INVALID3 = "testuser123gmail.com"  #if not present character @
REGISTER_EMAIL_INVALID4 = "testuser123@gggggggggggggg.com"  #if email domen not exist
REGISTER_EMAIL_INVALID5 = "gmail.com"  #if present only email domen
REGISTER_PASSWORD_INVALID1 = "p"    #when only one character
REGISTER_PASSWORD_INVALID2 = "p1234"    #when less than 6 characters

#CONFIRM_REGISTER_PASSWORD_INVALID = "abcd1234a"  # if confirm register password not same as register password (REGISTER_PASSWORD)


REGISTER_NAME = "Test User"
REGISTER_NAME_EMPTY = ""
 
REGISTER_EMAIL = "testuser@gmail.com"
REGISTER_EMAIL_EMPTY = ""
 
REGISTER_EMAIL_INVALID = [
    "testgmail.com",
    "test@",
    "@gmail.com",
    "test@gmail",
    "test@.com",
    "test@gggggg.com"
]
 
REGISTER_PASSWORD = "Test1234"
REGISTER_PASSWORD_EMPTY = ""
 
REGISTER_PASSWORD_INVALID = [
    "1",
    "12345"
]
 
CONFIRM_REGISTER_PASSWORD_EMPTY = ""
CONFIRM_REGISTER_PASSWORD_INVALID = "WrongPassword123"