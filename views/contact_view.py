from utils.helpers import prompt
from context import t

def contact_view():
    print('\n')
    print(t.contact.address)
    print(t.contact.directory)
    print(t.contact.open_hours)
    input(prompt(t.misc.press_q))