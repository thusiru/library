from books import Books
from consolemenu import ConsoleMenu
from consolemenu.items import FunctionItem
from getpass import getpass
from print_color import print as printf
from time import sleep
from user import User


def main():
    """main function"""
    menu = ConsoleMenu("Main menu", "Welcome to Library!")

    function_login = FunctionItem("Login", login)
    function_register = FunctionItem("Register", register)
    function_search = FunctionItem("Book search", search)

    menu.append_item(function_login)
    menu.append_item(function_register)
    menu.append_item(function_search)

    menu.show()


def route(function):
    if function == "login":
        login()
    if function == "register":
        register()
    if function == "search":
        search()


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


def login():
    """User login"""
    user = User.login()
    print(user)
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
