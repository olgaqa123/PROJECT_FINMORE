import random

import string
 
 
def generate_email():

    name = ''.join(random.choices(string.ascii_lowercase, k=6))

    number = random.randint(1000, 9999)

    return f"{name}{number}@gmail.com"

 