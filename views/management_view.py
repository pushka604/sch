import time
from utils.helpers import check_access, clear_console, prompt
from views.storage_overview_view import add_to_storage_view, remove_from_storage_view, storage_overview_view
from crud.crud_employees import read_employees
from views.dogs_overview_view import add_dog_view, remove_dog_view, change_adoption_view
from context import t, zalogowany_uzytkownik

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
                print(f'\n{t.misc.name}: {pracownik['name']}, {t.misc.surname}: {pracownik['surname']}')
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
