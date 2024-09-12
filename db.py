# db.py
import sqlite3
import threading

thread_local = threading.local()


class DatabaseConnection:
    def __enter__(self):
        if not hasattr(thread_local, "connection"):
            thread_local.connection = sqlite3.connect("library.db")
        self.connection = thread_local.connection
        return self.connection

    def __exit__(self, exc_type, exc_value, traceback):
        if hasattr(thread_local, "connection"):
            thread_local.connection.close()
            del thread_local.connection


def get_db_connection():
    return DatabaseConnection()
