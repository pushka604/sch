import json
from datetime import datetime 

with open('pieski.json', 'r') as file:
    pieski = json.load(file)

with open('pracownicy.json', 'r') as file:
    pracownicy = json.load(file)

with open('magazyn.json', 'r') as file:
    magazyn = json.load(file)

def validate_name(name):
    return name.isalpha() and len(name) > 0

def validate_birth_date(birth_date):
    try:
        birth_date_datetime = datetime.strptime(birth_date, '%d.%m.%Y')
        return birth_date_datetime <= datetime.now()
    except ValueError:
        return False

while True:
    print('Witamy na stronie głównej schroniska "Słoneczko"!')
    print('Menu:')
    print('1 - Dane kontaktowe schroniska')
    print('2 - Przegląd piesków')
    print('3 - Wyprowadzanie piesków')
    print('4 - Zarządzanie schroniskiem')
    print('5 - Zakończ program')
    choice = int(input('Twój wybór: '))

    if choice not in [1, 2, 3, 4, 5]:
        print('Brak dostępu do podanej funkcji')

    elif choice == 1:
        print('\n')
        print('Adres schroniska: \n ul. Koszykowa 12 \n 15-003 Białystok \n')
        print('Nasz zarząd: \n')
        print('Kierownik schroniska: \n Waldemar Kowalski \n tel.: 566 306 987 \n adres e-mail: waldemar.kowalski@gmail.com \n')
        print('Zastępca kierownika: \n Barbara Orzechowska \n tel:. 543 567 890 \n adres e-mail: barbara.orzechowska@gmail.com \n')
        print('Biuro: \n tel.: 540 420 456 \n adres e-mail: schronisko.słoneczko@gmail.com \n')
        print('Godziny otwarcia schroniska: \n poniedziałek: 8:00 - 16: 00 \n wtorek: 8:00 - 16:00 \n środa: 8:00 - 16:00 \n czwartek: 8:00 - 16:00 \n piątek: 8:00 - 16:00 \n sobota: 10:00 - 14:00')

    elif choice == 2:
        for piesek in pieski:
            print(f'\nImię: {piesek['imię']}')
            print(f'Data urodzenia: {piesek['data_urodzenia']}')
            print(f'Historia pieska: {piesek['historia_pieska']}')
            print(f'Historia zdrowotna: {piesek['historia_zdrowotna']}')
            print(f'Adopcja: {piesek['adopcja']}')

    elif choice == 3:
        imiona = []
        for piesek in pieski:
            imiona.append(piesek['imię'])
        while True:
            print(f'Którego pieska chciałbyś/chciałabyś wyprowadzić? {imiona}: ')
            wybór_pieska = str(input('Twój wybór: '))
            if wybór_pieska in imiona:
                while True:
                    data = str(input('Podaj datę (dzień.miesiąc.rok): '))
                    godzina = str(input('Podaj godzinę (hh:mm): '))
                    try:
                        dt = datetime.strptime(f'{data} {godzina}', '%d.%m.%Y %H:%M')
                        teraz = datetime.now()
                        if dt > teraz:
                            nowa_data_i_godzina = data + '/' + godzina
                            break
                        else:
                            print('Podana data i godzina są wcześniejsze niż obecna data i godzina. Spróbuj ponownie.')
                    except ValueError:
                        print('Niepoprawny format daty lub godziny. Spróbuj ponownie.')
                for piesek in pieski:
                    if piesek['imię'] == wybór_pieska:
                        if nowa_data_i_godzina not in piesek['daty_i_godziny']:
                            print('Zarezerwowano spacer!')
                            piesek['daty_i_godziny'].append(nowa_data_i_godzina)
                        else:
                            print('Próba rezerwacji nieudana!')
                        break
            else:
                print('Nie ma takiego pieska!')

            kontynuacja = input('Czy chcesz kontynuować? (tak/nie): ')
            if kontynuacja.lower() != 'tak':
                break

    elif choice == 4:

        while True:
            wybór = int(input(('Wybierz: \n 1 - Zarządzanie magazynem \n 2 - Zarządzanie pracownikami \n 3 - Zarządzanie zwierzątkami \n 4 - Powrót \n Twój wybór: ')))
            if wybór not in [1, 2, 3, 4]:
                print('Brak dostępu do podanej funkcji')
                
            elif wybór == 1:
                while True:
                    opcje = int(input('Wybierz: \n 1 - Dodaj rzecz do magazynu \n 2 - Usuń rzecz z magazynu \n 3 - Spis rzeczy w magazynie \n 4 - Powrót \n Twój wybór: '))
                    if opcje not in [1, 2, 3, 4]:
                        print('Brak dostępu do podanej funkcji')
                    elif opcje == 1:
                        rzecz = str(input('Jaką rzecz chcesz dodać do magazynu?: '))
                        if rzecz not in magazyn:
                            magazyn.append(rzecz)
                        else:
                            print(f'{rzecz} znajduje się już w magazynie!')
                    elif opcje == 2:
                        rzecz = str(input('Jaką rzecz chcesz usunąć z magazynu?: '))
                        if rzecz in magazyn:
                            magazyn.remove(rzecz)
                        else:
                            print(f'{rzecz} nie znajduje się już w magazynie!')
                    elif opcje == 3:
                        print(f'Spis rzeczy w magazynie: {magazyn}')
                    elif opcje == 4:
                        break
            
            elif wybór == 2:
                while True:
                    opcje = int(input('Wybierz: \n 1 - Pokaż imiona i nazwiska pracowników \n 2 - Pokaż staż pracy \n 3 - Pokaż wynagrodzenie \n 4 - Powrót \n Twój wybór'))
                    if opcje not in [1, 2, 3, 4]:
                        print('Brak dostępu do podanej funkcji')
                    elif opcje == 1:
                        for pracownik in pracownicy:
                            print(f'\nimię: {pracownik['imię']}, nazwisko: {pracownik['nazwisko']}')
                    elif opcje == 2:
                        for pracownik in pracownicy:
                            print(f'\nimię: {pracownik['imię']}, nazwisko: {pracownik['nazwisko']}, staż pracy (w latach): {pracownik['staż_pracy_(w latach)']}')
                    elif opcje == 3:
                        for pracownik in pracownicy:
                            print(f'\nimię: {pracownik['imię']}, nazwisko: {pracownik['nazwisko']}, wynagrodzenie: {pracownik['wynagrodzenie']}')
                    elif opcje == 4:
                        break
            
            elif wybór == 3:
                while True:
                    opcje = int(input('Wybierz: \n 1 - Dodaj pieska \n 2 - Usuń pieska \n 3 - Zmień stan adopcji \n 4 - Powrót \n Twój wybór: '))
                    if opcje not in [1, 2, 3, 4]:
                        print('Brak dostępu do podanej funkcji')
                    elif opcje == 1:
                        while True:
                            imię = str(input('Podaj imię pieska: '))
                            if validate_name(imię):
                                break
                            else:
                                print('Niepoprawne imię. Imię powinno zawierać tylko litery i nie być puste.')
                        
                        while True:
                            data_urodzenia = str(input('Podaj datę urodzenia pieska: '))
                            if validate_birth_date(data_urodzenia):
                                break
                            else:
                                print('Niepoprawna data urodzenia. Data powinna być w formacie dzień.miesiąc.rok i nie być późniejsza niż bieżący rok.')
                        
                        historia_pieska = str(input('Podaj historię pieska: '))
                        historia_zdrowotna = str(input('Podaj historię zdrowotną pieska: '))
                        nowy_piesek = {
                            'imię': imię,
                            'data_urodzenia': data_urodzenia,
                            'historia_pieska': historia_pieska,
                            'historia_zdrowotna': historia_zdrowotna,
                            'adopcja': 'wolny',
                            'daty_i_godziny': []
                        }
                        pieski.append(nowy_piesek)
                        print(f'Dodano pieska: {imię}')
                    elif opcje == 2:
                        imię = input('Podaj imię pieska do usunięcia: ')
                        pieski = [piesek for piesek in pieski if piesek['imię'] != imię]
                        print(f'Usunięto pieska: {imię}')
                    elif opcje == 3:
                        imię = str(input('Podaj imię pieska, którego stan adopcji chcesz zmienić: '))
                        for piesek in pieski:
                            if piesek['imię'] == imię:
                                print(f'Obecny status pieska {piesek['imię']}: {piesek['adopcja']}')
                                potwierdzenie = str(input('Czy na pewno chcesz zmienić stan adopcji pieska? (tak/nie): '))
                                if potwierdzenie.lower() == 'tak':
                                    if piesek['adopcja'] == 'wolny':
                                        piesek['adopcja'] = 'zarezerwowany'
                                    else:
                                        piesek['adopcja'] = 'wolny'
                                print(f'Stan pieska po zmianie: {piesek['adopcja']}')
                    elif opcje == 4:
                        break

            elif wybór == 4:
                break
    elif choice == 5:
        with open('pieski.json', 'w') as file:
            json.dump(pieski, file, ensure_ascii=False, indent=4)
        with open('magazyn.json', 'w') as file:
            json.dump(magazyn, file, ensure_ascii=False, indent=4)
        break