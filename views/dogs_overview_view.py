import time
from utils.helpers import prompt, clear_console
from crud.crud_dogs import read_dog, update_dog, create_dog, delete_dog, read_dogs
from utils.validation import validate_name, validate_birth_date
from context import t

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

def dogs_overview_view():

    clear_console()

    for piesek in read_dogs():
        print(f'\n{t.misc.name}: {piesek['imię']}')
        print(f'{t.overview.date_of_birth}: {piesek['data_urodzenia']}')
        print(f'{t.overview.dogs_history}: {piesek['historia_pieska']}')
        print(f'{t.overview.health_history}: {piesek['historia_zdrowotna']}')
        print(f'{t.overview.adoption}: {piesek['adopcja']}')   
    input(prompt(t.misc.press_q))