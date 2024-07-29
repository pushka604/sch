import os

def prompt(text):
    return text + ': '

def clear_console():
    os.system('cls' if os.name == 'nt' else 'clear')

def check_access(role, access_level):
    roles = {'gość': 1, 'wolontariusz': 2, 'manager': 3}
    return roles.get(role, 0) >= access_level