import bcrypt
import sqlite3


con = sqlite3.connect("library.db")
cur = con.cursor()


class User:
    def __init__(self, user_id):
        self.user_id = user_id

    @classmethod
    def login(cls):
        for i in range(4):
            username, password = cls.__input_validate()
            cur.execute("SELECT id, password FROM users WHERE username = ?", (username,))
            result = cur.fetchone()

            if result:
                user_id, hashword = result
                password = password.encode("utf-8")
                if bcrypt.checkpw(password, hashword):
                    print("Login Successful!")
                    con.close()
                    return cls(user_id)
                else:
                    print(f"Invalid Password. {3-i} attempts left.")
                    continue
            else:
                print(f"Invalid Username. {3-i} attempts left.")
                continue
        print("Failed to login after 4 attempts.")
        con.close()
        return None

    """@property
    def user_id(self):
        return self._user_id
    
    @user_id.setter
    def user_id(self, user_id):
        if not user_id:
            raise NameError
        self._user_id = user_id"""

    @staticmethod
    def __input_validate():
        username = input("Username: ")
        password = input("Password: ")

        if not username:
            raise ValueError("Username cannot be empty")
        if not password:
            raise ValueError("Password cannot be empty")
        return username, password

    @staticmethod
    def register():
        while True:
            try:
                username, password = User.__input_validate()
                re_password = input("Re enter password: ")

                if password == re_password:
                    password = password.encode("utf-8")
                    hashed = bcrypt.hashpw(password, bcrypt.gensalt())

                    cur.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, hashed))
                    con.commit()

                    print("User registration successful!")
                    return

                else:
                    print("Password doesn't match")
                    continue

            except sqlite3.IntegrityError:
                print("Username is not available")
                continue