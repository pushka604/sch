import time
from utils.helpers import prompt, clear_console, check_access
from crud.crud_dogs import read_dog, update_dog, create_dog, delete_dog, read_dogs
from utils.validation import validate_name, validate_birth_date
from context import t, zalogowany_uzytkownik

def change_adoption_view():
    dog_id = str(input(prompt(t.management.change_adoption_dog_name)))

    clear_console()

    piesek = read_dog(dog_id)

    if not piesek:
        return
    
    print(f'{t.management.current_adoption_state} {piesek['name']}: {piesek['adoption']}')

    potwierdzenie = str(input(prompt(t.management.confirmation)))
    if potwierdzenie.lower() == t.misc.yes:
        if piesek['adoption'] == "wolny":
            piesek = update_dog(dog_id, adopted="adoptowany")
        else:
            piesek = update_dog(dog_id, adopted="wolny")

    clear_console()

    print(f'{t.management.after_change_adoption_state}: {piesek['adoption']}')
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

    if create_dog(imię, historia_pieska, data_urodzenia, historia_zdrowotna):

        clear_console()

        print(f'{t.management.dog_done}: {imię}')
        time.sleep(4)

        clear_console()

def remove_dog_view():
    dog_id = input(prompt(t.management.remove_dog_name))

    if delete_dog(dog_id):

        clear_console()

        print(f'{t.management.dog_remove}: {dog_id}')
        time.sleep(4)

        clear_console()

    else:

        clear_console()
        print(f'{t.management.no_such_dog_named} {dog_id} {t.management.in_shelter}')
        time.sleep(4)
        clear_console()

def dogs_overview_view():

    clear_console()

    for piesek in read_dogs():
        print("\n")
        if check_access(zalogowany_uzytkownik["role"], 2):
            print(f"Id pieska: {piesek["dog_id"]}")
        print(f'{t.misc.name}: {piesek['name']}')
        print(f'{t.overview.date_of_birth}: {piesek['year_of_birth']}')
        print(f'{t.overview.dogs_history}: {piesek['dog_history']}')
        # print(f'{t.overview.health_history}: {piesek['description']}')
        # print(f'{t.overview.adoption}: {piesek['adoption']}')

    input(prompt(t.misc.press_q))


