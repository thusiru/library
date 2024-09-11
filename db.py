# db.py
import sqlite3
import threading

thread_local = threading.local()

def get_db_connection():
    if not hasattr(thread_local, 'connection'):
        thread_local.connection = sqlite3.connect("library.db")
    return thread_local.connection

def close_db_connection():
    if hasattr(thread_local, 'connection'):
        thread_local.connection.close()
        del thread_local.connection
