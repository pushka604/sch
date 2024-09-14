import sys
import time
from utils.helpers import clear_console, prompt
from views.contact_view import contact_view
from views.dogs_overview_view import dogs_overview_view
from views.dogs_reservations_view import dogs_reservations_view
from views.management_view import management_menu_view
from context import t, zalogowany_uzytkownik

def main_menu():
    while True:
        clear_console()
        print(f'{t.misc.hi} {zalogowany_uzytkownik["username"]}! {t.misc.greeting_menu}')
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