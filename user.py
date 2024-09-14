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
                try:
                    new_username = User.__input_username("New username: ")
                except ValueError as e:
                    printf(e, color="red")
                    continue
                try:
                    re_new_username = User.__input_username("Re enter new username: ")
                except ValueError:
                    print(e, color="red")
                    continue

                if new_username == re_new_username:
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

    def change_password(self):
        with get_db_connection() as con:
            cur = con.cursor()
            result = cur.execute(
                "SELECT password FROM users WHERE id = ?", (self.user_id,)
            ).fetchone()
            hashword = result[0]

            for _ in range(5):
                password = User.__input_password("Current Password: ")
                byteword = password.encode("utf-8")

                if bcrypt.checkpw(byteword, hashword):
                    new_password = User.__input_password("New Password: ")
                    re_new_password = User.__input_password("Re enter new password: ")

                    if new_password == re_new_password:
                        new_password = new_password.encode("utf=8")
                        new_hashword = bcrypt.hashpw(new_password, bcrypt.gensalt())

                        cur.execute(
                            "UPDATE users SET password = ? WHERE id = ?",
                            (
                                new_hashword,
                                self.user_id,
                            ),
                        )
                        con.commit()

                        printf("Password change successful.", color="green")
                        return
                    else:
                        printf("Password doesn't match.", color="red")
                else:
                    printf("Wrong password.", color="red")

        printf("Password change unsuccessful after 5 attemps.", color="red")

    @classmethod
    def login(cls):
        with get_db_connection() as con:
            cur = con.cursor()

            for i in range(5):
                try:
                    username = cls.__input_username("Username: ")
                    password = cls.__input_password("Password: ")
                except ValueError as e:
                    printf(f"{e} {4-i} attemps left", color="red")
                    continue

                cur.execute(
                    "SELECT id, password FROM users WHERE username = ?", (username,)
                )
                result = cur.fetchone()

                if result:
                    user_id, hashword = result
                    byteword = password.encode("utf-8")

                    if bcrypt.checkpw(byteword, hashword):
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
    def register():
        with get_db_connection() as con:
            cur = con.cursor()

            for _ in range(5):
                try:
                    username = User.__input_username("Username: ")
                    password = User.__input_password("Password: ")
                except ValueError as e:
                    printf(e, color="red")
                    continue
                re_password = User.__input_password("Re enter password: ")

                if password == re_password:
                    password = password.encode("utf-8")
                    hashword = bcrypt.hashpw(password, bcrypt.gensalt())

                    try:
                        cur.execute(
                            "INSERT INTO users (username, password) VALUES (?, ?)",
                            (username, hashword),
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

        printf("Registration failed after 5 attempts. Try again shortly.", color="red")

    @staticmethod
    def __input_username(prompt):
        username = input(prompt).strip()
        if not username:
            raise ValueError("Username cannot be empty.")
        if not username.islower():
            raise ValueError("Username must be lowercased.")
        else:
            return username
        
    @staticmethod
    def __input_password(prompt):
        password = input(prompt).strip()
        if not password:
            raise ValueError("Password cannot be empty.")
        if len(password) <= 4:
            raise ValueError("Password must be atleast 4 characters long.")
        if len(password) >= 16:
            raise ValueError("Password must be equal or less than 16 characters.")
        return password

    def __str__(self):
        return self.username
