from datetime import datetime, timedelta
from crud.crud_dogs import read_dogs
from utils.helpers import check_access, clear_console, prompt
from crud.crud_dogs import create_reservation
import time
from context import t, zalogowany_uzytkownik

def dogs_reservations_view():
    pieski = read_dogs()

    if not check_access(zalogowany_uzytkownik["role"], 2):
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