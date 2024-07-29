import json

def read_users():
    with open('data/uzytkownicy.json', 'r') as file:
        uzytkownicy = json.load(file)

    return uzytkownicy

def create_new_user(nowy_użytkownik):
    with open('data/uzytkownicy.json', 'r') as file:
        uzytkownicy = json.load(file)

    uzytkownicy.append(nowy_użytkownik)

    with open('data/uzytkownicy.json', 'w') as file:
        json.dump(uzytkownicy, file, ensure_ascii=False, indent=4)
    return True