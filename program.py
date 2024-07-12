import json

with open('pieski.json', 'r') as file:
    pieski = json.load(file)

with open('pracownicy.json', 'r') as file:
    pracownicy = json.load(file)

with open('magazyn.json', 'r') as file:
    magazyn = json.load(file)

print('Witamy na stronie głównej schroniska "Słoneczko"!')
print('Menu:')
print('1 - Dane kontaktowe schroniska')
print('2 - Przegląd piesków')
print('3 - Wyprowadzanie piesków')
print('4 - Zarządzanie schroniskiem')

choice = int(input('Twój wybór: '))

while choice not in [1, 2, 3, 4]:
    print('Brak dostępu do podanej funkcji')
    choice = int(input('Twój wybór: '))

if choice == 1:
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
        wybór_pieska = str(input())
        if wybór_pieska in imiona:
            data = str(input('Podaj datę (dzień.miesiąc.rok): '))
            godzina = str(input('Podaj godzinę: '))
            nowa_data_i_godzina = data + '/' + godzina

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
    wybór = int(input(('Wybierz: \n 1 - Zarządzanie magazynem \n 2 - Zarządzanie pracownikami \n 3 - Zarządzanie zwierzątkami \n')))
    if wybór not in [1, 2, 3]:
        print('Brak dostępu do podanej funkcji')
        wybór = int(input(('Wybierz: \n 1 - Zarządzanie magazynem \n 2 - Zarządzanie pracownikami \n 3 - Zarządzanie zwierzątkami \n')))

    elif wybór == 1:
        opcje = int(input('Wybierz: \n 1 - Dodaj rzecz do magazynu \n 2 - Usuń rzecz z magazynu \n 3 - Spis rzeczy w magazynie \n'))
        if opcje not in [1, 2, 3]:
            print('Brak dostępu do podanej funkcji')
            opcje = int(input('Wybierz: \n 1 - Dodaj rzecz do magazynu \n 2 - Usuń rzecz z magazynu \n 3 - Spis rzeczy w magazynie \n'))
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
    
    elif wybór == 2:
        opcje = int(input('Wybierz: \n 1 - Pokaż imiona i nazwiska pracowników \n 2 - Pokaż staż pracy \n 3 - Pokaż wynagrodzenie \n'))
        if opcje == 1:
            for pracownik in pracownicy:
                print(f'\nimię: {pracownik['imię']}, nazwisko: {pracownik['nazwisko']}')
        if opcje == 2:
            for pracownik in pracownicy:
                print(f'\nimię: {pracownik['imię']}, nazwisko: {pracownik['nazwisko']}, staż pracy (w latach): {pracownik['staż_pracy_(w latach)']}')
        if opcje == 3:
            for pracownik in pracownicy:
                print(f'\nimię: {pracownik['imię']}, nazwisko: {pracownik['nazwisko']}, wynagrodzenie: {pracownik['wynagrodzenie']}')
        
    elif wybór == 3:
        opcje = int(input('Wybierz: \n 1 - Dodaj pieska \n 2 - Usuń pieska \n 3 - Zmień stan adopcji \n'))
        if opcje not in [1, 2, 3]:
            print('Brak dostępu do podanej funkcji')
            opcje = int(input('Wybierz: \n 1 - Dodaj pieska \n 2 - Usuń pieska \n 3 - Zmień stan adopcji \n'))
        elif opcje == 1:
            imię = str(input('Podaj imię pieska: '))
            data_urodzenia = int(input('Podaj datę urodzenia pieska: '))
            historia_pieska = str(input('Podaj historię pieska: '))
            historia_zdrowotna = str(input('Podaj historię zdrowotną pieska: '))
            adopcja = str(input('Podaj stan adopcji (wolny/zarezerwowany): '))
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

with open('pieski.json', 'w') as file:
    json.dump(pieski, file, ensure_ascii=False, indent=4)

with open('magazyn.json', 'w') as file:
    json.dump(magazyn, file, ensure_ascii=False, indent=4)