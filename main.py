import time

from consolemenu import ConsoleMenu
from consolemenu.items import FunctionItem, SubmenuItem

from user import User


def main():
    """main function"""

    # main menu
    """menu = ConsoleMenu("Main menu", "Welcome to Library!", clear_screen=False)
    submenu_user = ConsoleMenu("Login or Register")
    function_login = FunctionItem("Login", login)
    function_register = FunctionItem("Register", register)
    submenu_login = SubmenuItem("Login", submenu_user, menu=menu)
    function_search = FunctionItem("Book search", search)
    menu.append_item(submenu_login)
    menu.append_item(function_search)
    submenu_user.append_item(function_login)
    submenu_user.append_item(function_register)
    menu.show()"""

    login()

def search():
    """Search for a book"""

    print("search")
    continues()

def login():
    user = User.login()
    print(user)
    input("Press Enter to continue...")

def register():
    User.register()
    input("Press Enter to continue...")

def continues():
    time.sleep(3)
    input("Press Enter to continue...")

if __name__ == "__main__":
    main()   