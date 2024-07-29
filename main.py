from views.choose_language_view import choose_language_view
from views.auth_view import choose_login_registration_view


def main():
    while True:
        choose_language_view()

        choose_login_registration_view()

main()