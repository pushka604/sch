import json
from datetime import datetime 
from copy import deepcopy
from dotmap import DotMap

with open('pieski.json', 'r') as file:
    pieski = json.load(file)

with open('pracownicy.json', 'r') as file:
    pracownicy = json.load(file)

with open('magazyn.json', 'r') as file:
    magazyn = json.load(file)

with open('pl.json', 'r') as file:
    t = DotMap(json.load(file))

def prompt(text):
    return text + ': '

def validate_name(name):
    return name.isalpha() and len(name) > 0

def validate_birth_date(birth_date):
    try:
        birth_date_datetime = datetime.strptime(birth_date, '%d.%m.%Y')
        return birth_date_datetime <= datetime.now()
    except ValueError:
        return False

def check_access(role, access_level):
    roles = {'gość': 1, 'wolontariusz': 2, 'manager': 3}
    return roles.get(role, 0) >= access_level

role = input(prompt(t.misc.give_role))

while True:
    print(t.misc.greeting_menu)
    choice = int(input(prompt(t.misc.your_choice)))

    if choice not in [1, 2, 3, 4, 5]:
        print(t.misc.no_access)

    elif choice == 1:
        print('\n')
        print(t.contact.address)
        print(t.contact.directory)
        print(t.contact.open_hours)

    elif choice == 2:
        for piesek in pieski:
            print(f'\n{t.misc.name}: {piesek['imię']}')
            print(f'{t.overview.date_of_birth}: {piesek['data_urodzenia']}')
            print(f'{t.overview.dogs_history}: {piesek['historia_pieska']}')
            print(f'{t.overview.health_history}: {piesek['historia_zdrowotna']}')
            print(f'{t.overview.adoption}: {piesek['adopcja']}')

    elif choice == 3:
        if check_access(role, 2):
            imiona = []
            for piesek in pieski:
                imiona.append(piesek['imię'])
            while True:
                print(f'{t.reservation.dog_walking_choice} {imiona}: ')
                wybór_pieska = str(input(prompt(t.misc.your_choice)))
                if wybór_pieska in imiona:
                    while True:
                        data = str(input(prompt(t.reservation.date_choice)))
                        godzina = str(input(prompt(t.reservation.time_choice)))
                        try:
                            dt = datetime.strptime(f'{data} {godzina}', '%d.%m.%Y %H:%M')
                            teraz = datetime.now()
                            if dt > teraz:
                                nowa_data_i_godzina = data + '/' + godzina
                                break
                            else:
                                print(t.reservation.early_date_error)
                        except ValueError:
                            print(t.reservation.invalid_date_format)
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

    elif choice == 4:
        if check_access(role, 3):
            while True:
                print(t.management.menu)
                wybór = int(input(prompt(t.misc.your_choice)))
                if wybór not in [1, 2, 3, 4]:
                    print(t.misc.no_access)
                    
                elif wybór == 1:
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
                
                elif wybór == 2:
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
                
                elif wybór == 3:
                    while True:
                        print(t.management.menu_for_dogs)
                        opcje = int(input(prompt(t.misc.your_choice)))
                        if opcje not in [1, 2, 3, 4]:
                            print(t.misc.no_access)
                        elif opcje == 1:
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
                        elif opcje == 2:
                            imię = input(prompt(t.management.remove_dog_name))
                            pieski_kopia = deepcopy(pieski)
                            pieski_kopia = [piesek for piesek in pieski_kopia if piesek['imię'] != imię]
                            with open('pieski.json', 'w') as file:
                                json.dump(pieski_kopia, file, ensure_ascii=False, indent=4)
                            with open('pieski.json', 'r') as file:
                                pieski = json.load(file)
                            print(f'{t.management.dog_remove}: {imię}')
                        elif opcje == 3:
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
                        elif opcje == 4:
                            break

                elif wybór == 4:
                    break
        else:
            print(t.misc.no_access)      

    elif choice == 5:
        with open('pieski.json', 'w') as file:
            json.dump(pieski, file, ensure_ascii=False, indent=4)
        with open('magazyn.json', 'w') as file:
            json.dump(magazyn, file, ensure_ascii=False, indent=4)
        break