import time
from utils.helpers import prompt, clear_console
from crud.crud_storage import create_storage_item, delete_storage_item, read_storage
from context import t

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

def storage_overview_view():
    print(f'{t.management.things_in_storage}: {read_storage()}')
    input(prompt(t.misc.press_q))