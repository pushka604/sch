import json
from dotmap import DotMap
from context import t

def choose_language_view():
    global t

    print("Wybierz język (pl, eng): ")
    jezyk = str(input('Twój wybór: '))
    if jezyk == 'eng':
        with open('data/eng.json', 'r') as file:
            t.update(DotMap(json.load(file)))
    else:
        with open('data/pl.json', 'r') as file:
            t.update(DotMap(json.load(file)))