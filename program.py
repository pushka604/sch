import os
import json
from datetime import datetime, timedelta
from copy import deepcopy
from dotmap import DotMap
import sys
from getpass import getpass

with open('pieski.json', 'r') as file:
    pieski = json.load(file)

with open('pracownicy.json', 'r') as file:
    pracownicy = json.load(file)

with open('uzytkownicy.json', 'r') as file:
    uzytkownicy = json.load(file)

t = {}
zalogowany_uzytkownik = {}

def main():
    while True:
        choose_language_view()

        choose_login_registration_view()

def login_view():
    global zalogowany_uzytkownik
    nazwa_uzytkownika = str(input(prompt(t.sign.name_of_user)))
    haslo = getpass(prompt(t.sign.password))

    znaleziono = False
    for uzytkownik in uzytkownicy:
        if nazwa_uzytkownika == uzytkownik["nazwa_użytkownika"]:
            if haslo == uzytkownik["hasło"]:
                znaleziono = True
                zalogowany_uzytkownik = uzytkownik
                break
    if znaleziono:
        print(t.sign.signing_in_successful)
        main_menu()
    else:
        print(t.sign.error_name_of_user)
        kontynuacja = str(input(prompt(t.misc.your_choice)))
        if kontynuacja.lower() == t.misc.no:
            sys.exit(t.misc.program_end)

def choose_login_registration_view():
    while True: 
        print(t.sign.login_registration)
        choice = int(input(prompt(t.misc.your_choice)))
        if choice not in [1, 2]:
            print(t.misc.failure_try_again)  
        else:
            break

    if choice == 1:
            register_view()

    elif choice == 2:
        login_view()

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

def prompt(text):
    return text + ': '

def clear_console():
    os.system('cls' if os.name == 'nt' else 'clear')

def validate_name(name):
    return name.isalpha() and len(name) > 0

def validate_birth_date(birth_date):
    try:
        birth_date_datetime = datetime.strptime(birth_date, '%d.%m.%Y')
        return birth_date_datetime <= datetime.now()
    except ValueError:
        return False

def validate_username(username):
    if len(username) < 5:
        print(t.sign.user_name_length_error)
        return False
    if not any(char.isupper() for char in username):
        print(t.sign.user_name_capital_letter_error)
        return False
    return True

def validate_password(password): 
    if len(password) < 8:
        print(t.sign.password_length_error)
        return False
    return True

def validate_access(role, hasło):
    while True:
        with open('klucze.json', 'r') as file:
            klucze = json.load(file)
        
        for klucz in klucze:
            if klucz["rola"] == role:
                if klucz["hasło"] == hasło:
                    return True
        return False
                        
def check_access(role, access_level):
    roles = {'gość': 1, 'wolontariusz': 2, 'manager': 3}
    return roles.get(role, 0) >= access_level

def contact_view():
    print('\n')
    print(t.contact.address)
    print(t.contact.directory)
    print(t.contact.open_hours)

def dogs_overview_view():
    for piesek in pieski:
        print(f'\n{t.misc.name}: {piesek['imię']}')
        print(f'{t.overview.date_of_birth}: {piesek['data_urodzenia']}')
        print(f'{t.overview.dogs_history}: {piesek['historia_pieska']}')
        print(f'{t.overview.health_history}: {piesek['historia_zdrowotna']}')
        print(f'{t.overview.adoption}: {piesek['adopcja']}')   

def dogs_reservations_view():
    global pieski
    if check_access(zalogowany_uzytkownik["rola"], 2):
        imiona = []
        for piesek in pieski:
            imiona.append(piesek['imię'])
        while True:
            print(f'{t.reservation.dog_walking_choice} {imiona}: ')
            wybór_pieska = str(input(prompt(t.misc.your_choice)))
            if wybór_pieska in imiona:
                for piesek in pieski:
                    if piesek['imię'] == wybór_pieska:
                        rezerwacje_dt = []
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
                            break

                    except ValueError:
                        print(t.reservation.invalid_date_format)
                        continue

                pieski_kopia = deepcopy(pieski)
                for piesek in pieski_kopia:
                    if piesek['imię'] == wybór_pieska:
                        if nowa_data_i_godzina not in piesek['daty_i_godziny']:
                            print(t.reservation.reservation_done)
                            piesek['daty_i_godziny'].append(nowa_data_i_godzina)
                            with open('pieski.json', 'w') as file:
                                json.dump(pieski_kopia, file, ensure_ascii=False, indent=4)
                            with open('pieski.json', 'r') as file:
                                pieski = json.load(file)
                        else:
                            print(t.reservation.reservation_failure)
                        break
            else:
                print(t.reservation.no_such_dog)

            kontynuacja = input(prompt(t.reservation.continue_question))
            if kontynuacja.lower() != t.misc.yes:
                break
    else:
        print(t.misc.no_access)            

def storage_management_menu_view():
    with open('magazyn.json', 'r') as file:
                magazyn = json.load(file)

    while True:
        print(t.management.menu_for_storage)
        opcje = int(input(prompt(t.misc.your_choice)))

        if opcje not in [1, 2, 3, 4]:
            print(t.misc.no_access)

        elif opcje == 1:
            rzecz = str(input(prompt(t.management.add_thing_choice)))
            if rzecz not in magazyn:
                magazyn_kopia = deepcopy(magazyn)
                magazyn_kopia.append(rzecz)
                with open('magazyn.json', 'w') as file:
                    json.dump(magazyn_kopia, file, ensure_ascii=False, indent=4) 
                with open('magazyn.json', 'r') as file:
                    magazyn = json.load(file)  
            else:
                print(f'{rzecz} {t.management.is_in_storage}')

        elif opcje == 2:
            rzecz = str(input(prompt(t.management.remove_thing_choice)))
            if rzecz in magazyn:
                magazyn_kopia = deepcopy(magazyn)
                magazyn_kopia.remove(rzecz)
                with open('magazyn.json', 'w') as file:
                    json.dump(magazyn_kopia, file, ensure_ascii=False, indent=4) 
                with open('magazyn.json', 'r') as file:
                    magazyn = json.load(file)
            else:
                print(f'{rzecz} {t.management.is_not_in_storage}')

        elif opcje == 3:
            print(f'{t.management.things_in_storage}: {magazyn}')

        elif opcje == 4:
            break

def employees_management_menu_view():
    while True:
        print(t.management.menu_for_emplyees)
        opcje = int(input(prompt(t.misc.your_choice)))
        if opcje not in [1, 2, 3, 4]:
            print(t.misc.no_access)
        elif opcje == 1:
            for pracownik in pracownicy:
                print(f'\n{t.misc.name}: {pracownik['imię']}, {t.misc.surname}: {pracownik['nazwisko']}')
        elif opcje == 2:
            for pracownik in pracownicy:
                print(f'\n{t.misc.name}: {pracownik['imię']}, {t.misc.surname}: {pracownik['nazwisko']}, {t.management.seniority}: {pracownik['staż_pracy_(w latach)']}')
        elif opcje == 3:
            for pracownik in pracownicy:
                print(f'\n{t.misc.name}: {pracownik['imię']}, {t.misc.surname}: {pracownik['nazwisko']}, {t.management.salary}: {pracownik['wynagrodzenie']}')
        elif opcje == 4:
            break

def add_dog_view():
    global pieski

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
    pieski_kopia = deepcopy(pieski)
    pieski_kopia.append(nowy_piesek)
    with open('pieski.json', 'w') as file:
        json.dump(pieski_kopia, file, ensure_ascii=False, indent=4)
    with open('pieski.json', 'r') as file:
        pieski = json.load(file)
    print(f'{t.management.dog_done}: {imię}')

def remove_dog_view():
    global pieski

    imię = input(prompt(t.management.remove_dog_name))
    pieski_kopia = deepcopy(pieski)
    pieski_kopia = [piesek for piesek in pieski_kopia if piesek['imię'] != imię]
    with open('pieski.json', 'w') as file:
        json.dump(pieski_kopia, file, ensure_ascii=False, indent=4)
    with open('pieski.json', 'r') as file:
        pieski = json.load(file)
    print(f'{t.management.dog_remove}: {imię}')

def change_adoption_view():
    global pieski

    imię = str(input(prompt(t.management.change_adoption_dog_name)))
    pieski_kopia = deepcopy(pieski)
    for piesek in pieski_kopia:
        if piesek['imię'] == imię:
            print(f'{t.management.current_adoption_state}{piesek['imię']}: {piesek['adopcja']}')
            potwierdzenie = str(input(prompt(t.management.confirmation)))
            if potwierdzenie.lower() == t.misc.yes:
                if piesek['adopcja'] == t.misc.free:
                    piesek['adopcja'] = t.misc.reserved
                else:
                    piesek['adopcja'] = t.misc.free
                with open('pieski.json', 'w') as file:
                    json.dump(pieski_kopia, file, ensure_ascii=False, indent=4)
                with open('pieski.json', 'r') as file:
                    pieski = json.load(file)
            print(f'{t.management.after_change_adoption_state}: {piesek['adopcja']}')

def dogs_management_menu_view():
    while True:
        print(t.management.menu_for_dogs)
        opcje = int(input(prompt(t.misc.your_choice)))
        if opcje not in [1, 2, 3, 4]:
            print(t.misc.no_access)

        elif opcje == 1:
            add_dog_view()

        elif opcje == 2:
            remove_dog_view()

        elif opcje == 3:
            change_adoption_view()

        elif opcje == 4:
            break

def management_menu_view():
    if not check_access(zalogowany_uzytkownik["rola"], 3):
        print(t.misc.no_access)
        return 
    
    while True:
        print(t.management.menu)
        wybór = int(input(prompt(t.misc.your_choice)))
        if wybór not in [1, 2, 3, 4]:
            print(t.misc.no_access)
                
        elif wybór == 1:
            storage_management_menu_view()
        
        elif wybór == 2:
            employees_management_menu_view()
        
        elif wybór == 3:
            dogs_management_menu_view()

        elif wybór == 4:
            break
    
def main_menu():
    while True:
        print(f'{t.misc.hi} {zalogowany_uzytkownik["nazwa_użytkownika"]}! {t.misc.greeting_menu}')
        choice = int(input(prompt(t.misc.your_choice)))

        if choice not in [1, 2, 3, 4, 5, 6]:
            print(t.misc.no_access)

        elif choice == 1:
            contact_view()

        elif choice == 2:
            dogs_overview_view()

        elif choice == 3:
            dogs_reservations_view()

        elif choice == 4:
            management_menu_view()

        elif choice == 5:
            print(t.sign.logging_out)
            return


        elif choice == 6:
            sys.exit(t.misc.program_end)

def register_view():
    print(t.sign.registration)
    while True:
        nazwa_użytkownika = str(input(prompt(t.sign.name_of_user)))
        if validate_username(nazwa_użytkownika):
            break

    while True:
        hasło = str(getpass(prompt(t.sign.password)))
        if validate_password(hasło):
            break

    role = str(input(prompt(t.misc.role))) 
    if role != "gość":
        hasło_zabezpieczające = str(input(prompt(t.sign.give_role_password)))
        if not validate_access(role, hasło_zabezpieczające):
            return 

    nowy_użytkownik = {
        "nazwa_użytkownika": nazwa_użytkownika,
        "hasło": hasło,
        "rola": role
    }

    with open('uzytkownicy.json', 'r') as file:
        uzytkownicy = json.load(file)

    uzytkownicy.append(nowy_użytkownik)

    with open('uzytkownicy.json', 'w') as file:
        json.dump(uzytkownicy, file, ensure_ascii=False, indent=4)

    print(t.sign.registration_done)

main()