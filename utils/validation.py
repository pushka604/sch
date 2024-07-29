import json
from datetime import datetime
from context import t

def validate_name(name):
    return name.isalpha() and len(name) > 0

def validate_birth_date(birth_date):
    try:
        birth_date_datetime = datetime.strptime(birth_date, '%d.%m.%Y')
        return birth_date_datetime <= datetime.now()
    except ValueError:
        return False

def validate_access(role, hasło):
    while True:
        with open('klucze.json', 'r') as file:
            klucze = json.load(file)
        
        for klucz in klucze:
            if klucz["rola"] == role:
                if klucz["hasło"] == hasło:
                    return True
        return False

def validate_password(password): 
    if len(password) < 8:
        print(t.sign.password_length_error)
        return False
    return True

def validate_username(username):
    if len(username) < 5:
        print(t.sign.user_name_length_error)
        return False
    if not any(char.isupper() for char in username):
        print(t.sign.user_name_capital_letter_error)
        return False
    return True