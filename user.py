import bcrypt
from db import get_db_connection, close_db_connection
from print_color import print as printf
from sqlite3 import IntegrityError


class User:
    def __init__(self, user_id):
        self.user_id = user_id

    @classmethod
    def login(cls):
        con = get_db_connection()
        cur = con.cursor()

        for i in range(5):
            try:
                username, password = cls.__input_validate()
            except ValueError as e:
                printf(f"{e} {4-i} attemps left", color="red")
                continue

            cur.execute(
                "SELECT id, password FROM users WHERE username = ?", (username,)
            )
            result = cur.fetchone()

            if result:
                user_id, hashword = result
                password = password.encode("utf-8")
                if bcrypt.checkpw(password, hashword):
                    printf("Login Successful!", color="green")
                    close_db_connection()
                    return cls(user_id)
                else:
                    printf(f"Invalid Password. {4-i} attempts left.", color="red")
                    continue
            else:
                printf(f"Invalid Username. {4-i} attempts left.", color="red")
                continue

        printf("Failed to login after 5 attempts.", color="red")
        close_db_connection
        return None

    @staticmethod
    def __input_validate():
        username = input("Username: ")
        password = input("Password: ")

        if not username:
            raise ValueError("Username cannot be empty.")
        if not password:
            raise ValueError("Password cannot be empty.")
        return username, password

    @staticmethod
    def register():
        con = get_db_connection()
        cur = con.cursor()

        for _ in range(5):
            try:
                username, password = User.__input_validate()
            except ValueError as e:
                printf(e, color="red")
                continue

            re_password = input("Re enter password: ")

            if password == re_password:
                password = password.encode("utf-8")
                hashed = bcrypt.hashpw(password, bcrypt.gensalt())

                try:
                    cur.execute(
                        "INSERT INTO users (username, password) VALUES (?, ?)",
                        (username, hashed),
                    )
                    con.commit()
                except IntegrityError:
                    printf("Username is not available", color="red")
                    continue

                printf("User registration successful!", color="green")
                close_db_connection()
                return

            else:
                printf("Password doesn't match", color="red")
                continue

        printf("Registration failed after 5 attempts", color="red")
