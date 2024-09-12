import bcrypt
from db import get_db_connection
from print_color import print as printf
from sqlite3 import IntegrityError


class User:
    def __init__(self, username, user_id):
        self.username = username
        self.user_id = user_id

    def change_username(self):
        with get_db_connection() as con:
            cur = con.cursor()

            for _ in range(5):
                new_username = input("New username: ")
                if not new_username:
                    printf("Username cannot be empty.", color="red")
                    continue
                if new_username == input("Re enter new username: "):
                    try:
                        cur.execute(
                            "UPDATE users SET username = ? WHERE username = ?",
                            (
                                new_username,
                                self.username,
                            ),
                        )
                        con.commit()
                    except IntegrityError:
                        printf("Username not availabe. Try another one.", color="red")
                        continue
                    printf("Username change successful.", color="green")
                    return
                else:
                    printf("Username doesn't match.", color="red")
                    continue
            printf("Username change unsuccessful after 5 attempts.", color="red")

    @classmethod
    def login(cls):
        with get_db_connection() as con:
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
                        return cls(username, user_id)
                    else:
                        printf(f"Invalid Password. {4-i} attempts left.", color="red")
                        continue
                else:
                    printf(f"Invalid Username. {4-i} attempts left.", color="red")
                    continue

            printf("Failed to login after 5 attempts.", color="red")
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
        with get_db_connection() as con:
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
                    return

                else:
                    printf("Password doesn't match", color="red")
                    continue

            printf(
                "Registration failed after 5 attempts. Try again shortly.", color="red"
            )

    def __str__(self):
        return self.username
