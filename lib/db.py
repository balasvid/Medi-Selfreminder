import sqlite3
from contextlib import contextmanager
import threading

# Thread-local storage for database connection
thread_local = threading.local()

def get_db_connection():
    if not hasattr(thread_local, "conn"):
        thread_local.conn = sqlite3.connect('mediselfreminder.db')
    return thread_local.conn

@contextmanager
def open_db_connection():
    conn = get_db_connection()
    try:
        yield conn
    finally:
        pass  # Do not close the connection here; it will be reused
