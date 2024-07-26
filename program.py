import os
import json
from datetime import datetime, timedelta
from copy import deepcopy
from dotmap import DotMap
import sys
from getpass import getpass
import time

t = {}
zalogowany_uzytkownik = {}



def prompt(text):
    return text + ': '

def clear_console():
    os.system('cls' if os.name == 'nt' else 'clear')

def check_access(role, access_level):
    roles = {'gość': 1, 'wolontariusz': 2, 'manager': 3}
    return roles.get(role, 0) >= access_level

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



def read_dogs():
    with open('pieski.json', 'r') as file:
        pieski = json.load(file)
    
    return pieski

def read_employees():
    with open('pracownicy.json', 'r') as file:
        pracownicy = json.load(file)

    return pracownicy

def read_users():
    with open('uzytkownicy.json', 'r') as file:
        uzytkownicy = json.load(file)

    return uzytkownicy

def read_storage():
    with open('magazyn.json', 'r') as file:
        magazyn = json.load(file)
    
    return magazyn



def create_reservation(dog_name, reservation):
    success = False

    with open('pieski.json', 'r') as file:
        pieski = json.load(file)
    
    for piesek in pieski:
        if piesek['imię'] == dog_name:
            if reservation not in piesek['daty_i_godziny']:
                piesek['daty_i_godziny'].append(reservation)
                success = True
            break
    
    if success:
        with open('pieski.json', 'w') as file:
            json.dump(pieski, file, ensure_ascii=False, indent=4)
        return True

def reservation_timedate_prompt(wybór_pieska):
    for piesek in read_dogs():
        if piesek['imię'] == wybór_pieska:
            rezerwacje_dt= [datetime.strptime(data_i_godzina, '%d.%m.%Y/%H:%M') for data_i_godzina in piesek['daty_i_godziny']]

    while True:

        data = str(input(prompt(t.reservation.date_choice)))
        godzina = str(input(prompt(t.reservation.time_choice)))
    
        try:
            nowa_rezerwacja_dt = datetime.strptime(f'{data} {godzina}', '%d.%m.%Y %H:%M')

            wcześniejsze_rezerwacje = []
            późniejsze_rezerwacje = []

            for rezerwacja in rezerwacje_dt:
                if rezerwacja < nowa_rezerwacja_dt:
                    wcześniejsze_rezerwacje.append(rezerwacja)
                else:
                    późniejsze_rezerwacje.append(rezerwacja)
                    
            if wcześniejsze_rezerwacje and max(wcześniejsze_rezerwacje) + timedelta(minutes=30) > nowa_rezerwacja_dt:
                print(t.reservation.walking_reservation_failure)
                continue
            if późniejsze_rezerwacje and min(późniejsze_rezerwacje) - timedelta(minutes=30) < nowa_rezerwacja_dt:
                print(t.reservation.walking_reservation_failure)
                continue

            teraz_dt = datetime.now()

            if nowa_rezerwacja_dt < teraz_dt:
                print(t.reservation.early_date_error)
                continue
            else:
                nowa_data_i_godzina = data + '/' + godzina
                return nowa_data_i_godzina

        except ValueError:
            clear_console()
            print(t.reservation.invalid_date_format)
            time.sleep(4)
            clear_console()
            continue

def dogs_reservations_view():
    pieski = read_dogs()

    if not check_access(zalogowany_uzytkownik["rola"], 2):
        clear_console()
        print(t.misc.no_access)
        time.sleep(4)
        clear_console()
        return

    imiona = []
    for piesek in pieski:
        imiona.append(piesek['imię'])

    clear_console()

    while True:
        print(f'{t.reservation.dog_walking_choice} {imiona}: ')
        wybór_pieska = str(input(prompt(t.misc.your_choice)))
        
        if not wybór_pieska in imiona:
            clear_console()
            print(t.reservation.no_such_dog)
            time.sleep(4)
            clear_console()
            continue

        nowa_data_i_godzina = reservation_timedate_prompt(wybór_pieska)

        clear_console()

        if create_reservation(wybór_pieska, nowa_data_i_godzina):
            print(t.reservation.reservation_done)
            time.sleep(4)
        else:
            print(t.reservation.reservation_failure)
            time.sleep(4)

        clear_console()

        kontynuacja = input(prompt(t.reservation.continue_question)) 

        if kontynuacja.lower() != t.misc.yes:
            break
        clear_console()


def create_storage_item(item):
    success = False

    with open('magazyn.json', 'r') as file:
        magazyn = json.load(file)

    if item not in magazyn:
        magazyn.append(item)
        success = True
    
    if success:
        with open('magazyn.json', 'w') as file:
            json.dump(magazyn, file, ensure_ascii=False, indent=4)
        return True

def delete_storage_item(item):
    success = False

    with open('magazyn.json', 'r') as file:
        magazyn = json.load(file)

    if item in magazyn:
        magazyn.remove(item)
        success = True

    if success:
        with open('magazyn.json', 'w') as file:
            json.dump(magazyn, file, ensure_ascii=False, indent=4)
        return True

def add_to_storage_view():

    rzecz = str(input(prompt(t.management.add_thing_choice)))

    clear_console()

    if create_storage_item(rzecz):
        print(f'{t.management.added} {rzecz} {t.management.to_storage}')
        time.sleep(4)
    else:
        print(f'{rzecz} {t.management.is_in_storage}')
        time.sleep(4)

    clear_console()

def remove_from_storage_view():
    rzecz = str(input(prompt(t.management.remove_thing_choice)))

    clear_console()

    if delete_storage_item(rzecz):
        print(f'{t.management.removed} {rzecz} {t.management.from_storage}')
        time.sleep(4)
    else:
        print(f'{rzecz} {t.management.is_not_in_storage}')
        time.sleep(4)

    clear_console()



def create_dog(new_dog):
    with open('pieski.json', 'r') as file:
        pieski = json.load(file)

    pieski.append(new_dog)

    with open('pieski.json', 'w') as file:
        json.dump(pieski, file, ensure_ascii=False, indent=4)
    return True

def delete_dog(dog_name):
    success = False

    with open('pieski.json', 'r') as file:
        pieski = json.load(file)

    if any(piesek['imię'] == dog_name for piesek in pieski):
        new_pieski = [piesek for piesek in pieski if piesek['imię'] != dog_name]

        with open('pieski.json', 'w') as file:
            json.dump(new_pieski, file, ensure_ascii=False, indent=4)
        
        success = True

    return success

def update_dog(dog_name, new_dog_data):
    success = False

    with open('pieski.json', 'r') as file:
        pieski = json.load(file)

    for index, piesek in enumerate(pieski):
        if piesek['imię'] == dog_name:
            pieski[index] = new_dog_data
            success = True
    
    if success:
        with open('pieski.json', 'w') as file:
            json.dump(pieski, file, ensure_ascii=False, indent=4)
        return True

def read_dog(dog_name):
    result = {}

    with open('pieski.json', 'r') as file:
        pieski = json.load(file)
    
    for piesek in pieski:
        if piesek['imię'] == dog_name:
            result = piesek
    
    return result

def change_adoption_view():
    imię = str(input(prompt(t.management.change_adoption_dog_name)))

    clear_console()

    piesek = read_dog(imię)

    if not piesek:
        return
    
    print(f'{t.management.current_adoption_state} {piesek['imię']}: {piesek['adopcja']}')

    potwierdzenie = str(input(prompt(t.management.confirmation)))
    if potwierdzenie.lower() == t.misc.yes:
        if piesek['adopcja'] == t.misc.free:
            piesek['adopcja'] = t.misc.reserved
            update_dog(imię, piesek)
        else:
            piesek['adopcja'] = t.misc.free
            update_dog(imię, piesek)

    clear_console()

    print(f'{t.management.after_change_adoption_state}: {piesek['adopcja']}')
    time.sleep(4)

    clear_console()

def add_dog_view():
    while True:
        imię = str(input(prompt(t.management.add_give_dog_name)))
        if validate_name(imię):
            break
        else:
            print(t.management.name_error)

    while True:
        data_urodzenia = str(input(prompt(t.management.give_birth_date)))
        if validate_birth_date(data_urodzenia):
            break
        else:
            print(t.management.birth_date_error)

    historia_pieska = str(input(prompt(t.management.give_dog_history)))
    historia_zdrowotna = str(input(prompt(t.management.give_dog_health_history)))
    nowy_piesek = {
        'imię': imię,
        'data_urodzenia': data_urodzenia,
        'historia_pieska': historia_pieska,
        'historia_zdrowotna': historia_zdrowotna,
        'adopcja': 'wolny',
        'daty_i_godziny': []
    }

    if create_dog(nowy_piesek):

        clear_console()

        print(f'{t.management.dog_done}: {imię}')
        time.sleep(4)

        clear_console()

def remove_dog_view():
    imię = input(prompt(t.management.remove_dog_name))

    if delete_dog(imię):

        clear_console()

        print(f'{t.management.dog_remove}: {imię}')
        time.sleep(4)

        clear_console()

    else:

        clear_console()
        print(f'{t.management.no_such_dog_named} {imię} {t.management.in_shelter}')
        time.sleep(4)
        clear_console()


def contact_view():
    print('\n')
    print(t.contact.address)
    print(t.contact.directory)
    print(t.contact.open_hours)
    input(prompt(t.misc.press_q))

def choose_language_view():
    global t

    print("Wybierz język (pl, eng): ")
    jezyk = str(input('Twój wybór: '))
    if jezyk == 'eng':
        with open('eng.json', 'r') as file:
            t = DotMap(json.load(file))
    else:
        with open('pl.json', 'r') as file:
            t = DotMap(json.load(file))

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
                zalogowany_uzytkownik = uzytkownik
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



def storage_overview_view():
    print(f'{t.management.things_in_storage}: {read_storage()}')
    input(prompt(t.misc.press_q))

def dogs_overview_view():

    clear_console()

    for piesek in read_dogs():
        print(f'\n{t.misc.name}: {piesek['imię']}')
        print(f'{t.overview.date_of_birth}: {piesek['data_urodzenia']}')
        print(f'{t.overview.dogs_history}: {piesek['historia_pieska']}')
        print(f'{t.overview.health_history}: {piesek['historia_zdrowotna']}')
        print(f'{t.overview.adoption}: {piesek['adopcja']}')   
    input(prompt(t.misc.press_q))



def create_new_user(nowy_użytkownik):
    with open('uzytkownicy.json', 'r') as file:
        uzytkownicy = json.load(file)

    uzytkownicy.append(nowy_użytkownik)

    with open('uzytkownicy.json', 'w') as file:
        json.dump(uzytkownicy, file, ensure_ascii=False, indent=4)
    return True

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



def main():
    while True:
        choose_language_view()

        choose_login_registration_view()

def main_menu():
    while True:
        clear_console()
        print(f'{t.misc.hi} {zalogowany_uzytkownik["nazwa_użytkownika"]}! {t.misc.greeting_menu}')
        choice = int(input(prompt(t.misc.your_choice)))

        if choice not in [1, 2, 3, 4, 5, 6]:
            clear_console()

            print(t.misc.no_access)
            time.sleep(4)

            clear_console()

        elif choice == 1:
            clear_console()
            contact_view()

        elif choice == 2:
            dogs_overview_view()

        elif choice == 3:
            dogs_reservations_view()

        elif choice == 4:
            management_menu_view()

        elif choice == 5:
            clear_console()
            print(t.sign.logging_out)
            time.sleep(4)
            clear_console()
            return


        elif choice == 6:
            clear_console()
            sys.exit(t.misc.program_end)

def management_menu_view():
    if not check_access(zalogowany_uzytkownik["rola"], 3):
        clear_console()
        print(t.misc.no_access)
        time.sleep(4)
        clear_console()
        return 
    
    clear_console()
    while True:
        print(t.management.menu)
        wybór = int(input(prompt(t.misc.your_choice)))
        if wybór not in [1, 2, 3, 4]:
            clear_console()
            print(t.misc.no_access)
            time.sleep(4)
            clear_console()
        
        elif wybór == 1:
            clear_console()
            storage_management_menu_view()
        
        elif wybór == 2:
            clear_console()
            employees_management_menu_view()
        
        elif wybór == 3:
            clear_console()
            dogs_management_menu_view()

        elif wybór == 4:
            break

def storage_management_menu_view():
    while True:
        clear_console()
        print(t.management.menu_for_storage)
        opcje = int(input(prompt(t.misc.your_choice)))

        if opcje not in [1, 2, 3, 4]:
            clear_console()
            print(t.misc.no_access)
            time.sleep(4)
            clear_console()

        elif opcje == 1:
            clear_console()
            add_to_storage_view()

        elif opcje == 2:
            clear_console()
            remove_from_storage_view()

        elif opcje == 3:
            clear_console()
            storage_overview_view()

        elif opcje == 4:
            clear_console()
            break

def employees_management_menu_view():
    while True:
        clear_console()
        print(t.management.menu_for_emplyees)
        opcje = int(input(prompt(t.misc.your_choice)))

        if opcje not in [1, 2, 3, 4]:
            clear_console()
            print(t.misc.no_access)
            time.sleep(4)
            clear_console()

        elif opcje == 1:
            clear_console()
            for pracownik in read_employees():
                print(f'\n{t.misc.name}: {pracownik['imię']}, {t.misc.surname}: {pracownik['nazwisko']}')
            input(prompt(t.misc.press_q))

        elif opcje == 2:
            clear_console()
            for pracownik in read_employees():
                print(f'\n{t.misc.name}: {pracownik['imię']}, {t.misc.surname}: {pracownik['nazwisko']}, {t.management.seniority}: {pracownik['staż_pracy_(w latach)']}')
            input(prompt(t.misc.press_q))

        elif opcje == 3:
            clear_console()
            for pracownik in read_employees():
                print(f'\n{t.misc.name}: {pracownik['imię']}, {t.misc.surname}: {pracownik['nazwisko']}, {t.management.salary}: {pracownik['wynagrodzenie']}')
            input(prompt(t.misc.press_q))

        elif opcje == 4:
            clear_console()
            break

def dogs_management_menu_view():
    while True:
        print(t.management.menu_for_dogs)
        opcje = int(input(prompt(t.misc.your_choice)))

        if opcje not in [1, 2, 3, 4]:
            clear_console()
            print(t.misc.no_access)
            time.sleep(4)
            clear_console()

        elif opcje == 1:
            clear_console()
            add_dog_view()

        elif opcje == 2:
            clear_console()
            remove_dog_view()

        elif opcje == 3:
            clear_console()
            change_adoption_view()

        elif opcje == 4:
            clear_console()
            break



main()