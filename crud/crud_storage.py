import json

def read_storage():
    with open('data/magazyn.json', 'r') as file:
        magazyn = json.load(file)
    
    return magazyn

def create_storage_item(item):

    success = False

    with open('data/magazyn.json', 'r') as file:
        magazyn = json.load(file)

    if item not in magazyn:
        magazyn.append(item)
        success = True
    
    if success:
        with open('data/magazyn.json', 'w') as file:
            json.dump(magazyn, file, ensure_ascii=False, indent=4)
        return True
    
def delete_storage_item(item):
    success = False

    with open('data/magazyn.json', 'r') as file:
        magazyn = json.load(file)

    if item in magazyn:
        magazyn.remove(item)
        success = True

    if success:
        with open('data/magazyn.json', 'w') as file:
            json.dump(magazyn, file, ensure_ascii=False, indent=4)
        return True
    

