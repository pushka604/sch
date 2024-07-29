import json

def read_employees():
    with open('data/pracownicy.json', 'r') as file:
        pracownicy = json.load(file)

    return pracownicy

