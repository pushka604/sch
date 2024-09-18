from datetime import datetime, timedelta
from utils.helpers import check_access, clear_console, prompt
from crud.crud_reservations import create_reservation, read_reservations
import time
from context import t, zalogowany_uzytkownik

def dogs_reservations_view():

    if not check_access(zalogowany_uzytkownik["role"], 2):
        clear_console()
        print(t.misc.no_access)
        time.sleep(4)
        clear_console()
        return

    clear_console()

    while True:
        print(f'{t.reservation.dog_walking_choice}: ')
        dog_id = str(input(prompt(t.misc.your_choice)))

        nowa_data_i_godzina = reservation_timedate_prompt(dog_id)

        clear_console()

        if create_reservation(5, dog_id, nowa_data_i_godzina):
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

def reservation_timedate_prompt(dog_id):
    all_reservations = read_reservations(dog_id)
    dates = [item['date_and_hours'] for item in all_reservations]

    while True:

        data = str(input(prompt(t.reservation.date_choice)))
        godzina = str(input(prompt(t.reservation.time_choice)))
    
        try:
            nowa_rezerwacja_dt = datetime.strptime(f'{data} {godzina}', '%Y-%m-%d %H:%M')

            wcześniejsze_rezerwacje = []
            późniejsze_rezerwacje = []

            for reservation in dates:
                if reservation < nowa_rezerwacja_dt:
                    wcześniejsze_rezerwacje.append(reservation)
                else:
                    późniejsze_rezerwacje.append(reservation)
                    
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
                nowa_data_i_godzina = data + ' ' + godzina
                return nowa_data_i_godzina

        except ValueError:
            clear_console()
            print(t.reservation.invalid_date_format)
            time.sleep(4)
            clear_console()
            continue