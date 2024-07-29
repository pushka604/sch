import json

def read_dogs():
    with open('data/pieski.json', 'r') as file:
        pieski = json.load(file)
    
    return pieski

def create_dog(new_dog):
    with open('data/pieski.json', 'r') as file:
        pieski = json.load(file)

    pieski.append(new_dog)

    with open('data/pieski.json', 'w') as file:
        json.dump(pieski, file, ensure_ascii=False, indent=4)
    return True

def delete_dog(dog_name):
    success = False

    with open('data/pieski.json', 'r') as file:
        pieski = json.load(file)

    if any(piesek['imię'] == dog_name for piesek in pieski):
        new_pieski = [piesek for piesek in pieski if piesek['imię'] != dog_name]

        with open('data/pieski.json', 'w') as file:
            json.dump(new_pieski, file, ensure_ascii=False, indent=4)
        
        success = True

    return success

def update_dog(dog_name, new_dog_data):
    success = False

    with open('data/pieski.json', 'r') as file:
        pieski = json.load(file)

    for index, piesek in enumerate(pieski):
        if piesek['imię'] == dog_name:
            pieski[index] = new_dog_data
            success = True
    
    if success:
        with open('data/pieski.json', 'w') as file:
            json.dump(pieski, file, ensure_ascii=False, indent=4)
        return True
    
def read_dog(dog_name):
    result = {}

    with open('data/pieski.json', 'r') as file:
        pieski = json.load(file)
    
    for piesek in pieski:
        if piesek['imię'] == dog_name:
            result = piesek
    
    return result

def create_reservation(dog_name, reservation):
    success = False

    with open('data/pieski.json', 'r') as file:
        pieski = json.load(file)
    
    for piesek in pieski:
        if piesek['imię'] == dog_name:
            if reservation not in piesek['daty_i_godziny']:
                piesek['daty_i_godziny'].append(reservation)
                success = True
            break
    
    if success:
        with open('data/pieski.json', 'w') as file:
            json.dump(pieski, file, ensure_ascii=False, indent=4)
        return True