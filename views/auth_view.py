import sys
from getpass import getpass
import time
from utils.helpers import clear_console, prompt
from crud.crud_users import read_users
from views.main_view import main_menu
from utils.validation import validate_username, validate_password, validate_access
from crud.crud_users import create_new_user
from context import t, zalogowany_uzytkownik

def choose_login_registration_view():
    while True: 
        clear_console()
        print(t.sign.login_registration)
        choice = int(input(prompt(t.misc.your_choice)))
        if choice not in [1, 2]:
            clear_console()
            print(t.misc.failure_try_again)
            time.sleep(4)
            clear_console()  
        else:
            break

    if choice == 1:
        register_view()

    elif choice == 2:
        login_view()

def login_view():
    global zalogowany_uzytkownik

    nazwa_uzytkownika = str(input(prompt(t.sign.name_of_user)))
    haslo = getpass(prompt(t.sign.password))

    znaleziono = False

    for uzytkownik in read_users():
        if nazwa_uzytkownika == uzytkownik["nazwa_użytkownika"]:
            if haslo == uzytkownik["hasło"]:
                znaleziono = True
                zalogowany_uzytkownik["nazwa_użytkownika"] = uzytkownik["nazwa_użytkownika"]
                zalogowany_uzytkownik["rola"] = uzytkownik["rola"]
                break

    if znaleziono:

        clear_console()

        print(t.sign.signing_in_successful)
        time.sleep(4)

        clear_console()

        main_menu()
    else:
        print(t.sign.error_name_of_user)
        kontynuacja = str(input(prompt(t.misc.your_choice)))

        if kontynuacja.lower() == t.misc.no:
            sys.exit(t.misc.program_end)

def register_view():

    clear_console()

    print(t.sign.registration)
    while True:
        nazwa_użytkownika = str(input(prompt(t.sign.name_of_user)))
        if validate_username(nazwa_użytkownika):
            break

    while True:
        hasło = str(getpass(prompt(t.sign.password)))
        if validate_password(hasło):
            break

    role = str(input(prompt(t.misc.give_role))) 
    if role != "gość":
        hasło_zabezpieczające = str(input(prompt(t.sign.give_role_password)))
        if not validate_access(role, hasło_zabezpieczające):
            return 

    nowy_użytkownik = {
        "nazwa_użytkownika": nazwa_użytkownika,
        "hasło": hasło,
        "rola": role
    }

    if create_new_user(nowy_użytkownik):

        clear_console()

        print(t.sign.registration_done)
        time.sleep(4)

        clear_console()