from books import Books
from consolemenu import ConsoleMenu
from consolemenu.items import FunctionItem, SubmenuItem
from getpass import getpass
from print_color import print as printf
from time import sleep
from user import User


def main():
    """main function"""
    main_menu()


def main_menu():
    """Main menu"""
    # Create main menu
    menu = ConsoleMenu("Main menu", "Welcome to Library!", clear_screen=False)

    # Create main menu items
    function_login = FunctionItem("Login", login, [menu])
    function_register = FunctionItem("Register", register)
    function_search = FunctionItem("Book search", search)

    # Append main menu items
    menu.append_item(function_login)
    menu.append_item(function_register)
    menu.append_item(function_search)

    # Show main menu
    menu.show()


def logged_menu(user, main_menu):
    """Logged in menu"""
    # Pause main menu
    main_menu.pause()

    # Create menu
    menu = ConsoleMenu(
        "Main menu", f"Hi {user}!", exit_option_text="Logout", clear_screen=False
    )

    # Menu item 1
    function_search = FunctionItem("Book search", search)

    # Menu item 2
    my_books_menu = ConsoleMenu("My books", exit_option_text="Back", clear_screen=False)
    my_books = SubmenuItem("My books", my_books_menu, menu=menu)

    # Submenu items

    # Menu item 3
    my_account_menu = ConsoleMenu(
        "My account", exit_option_text="Back", clear_screen=False
    )
    my_account = SubmenuItem("My account", my_account_menu, menu=menu)

    # Submenu items
    function_username = FunctionItem("Change Username", change_username, [user])
    function_password = FunctionItem("Change Password", change_password, [user])

    # Append menus and submenus
    menu.append_item(function_search)
    menu.append_item(my_books)
    menu.append_item(my_account)
    my_account_menu.append_item(function_username)
    my_account_menu.append_item(function_password)

    # Show menu
    menu.show()

    # Resume main menu
    main_menu.resume()


def change_username(user):
    user.change_username()
    continues()


def change_password(user):
    user.change_password()
    continues()


def search():
    """Search for a book"""
    title = input("Title: ")
    books = Books.search(title)

    if books:
        authors = []
        for book in sorted(books, key=lambda book: book[1]):
            if not book[1] in authors:
                authors.append(book[1])
                print()
                print("+" + "-" * 58 + "+")
                printf(f"|    Author: {book[1]:<46}|", color="yellow")
                print("+" + "-" * 58 + "+")
            printf(f"|    Title: {book[0]:<47}|", color="blue")
            if book[2] == "true":
                printf(f"|    Available{" " * 45}|", color="green")
            else:
                printf("|    Not available    ", end="", color="purple")
                print(f"Return date: {book[3]:<24}|")
            print("+" + "-" * 58 + "+")
        print(f"{len(books)} results found")
    else:
        printf("No results found. Try another search", color="red")
    continues()


def login(menu):
    """User login"""
    user = User.login()
    if user:
        continues()
        logged_menu(user, menu)
    else:
        continues()


def register():
    """User registration"""
    User.register()
    continues()


def continues():
    sleep(1)
    print()
    printf("Press Enter to continue...", color="magenta")
    getpass("")


if __name__ == "__main__":
    main()
