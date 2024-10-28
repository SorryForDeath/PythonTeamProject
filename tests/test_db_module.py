import pytest
import sqlite3
from src.db_module import open_connection, close_connection, add_records, update_records, delete_records, is_number

connection = None
db_name = 'event_database.db'
def test_open_connection():
    open_connection()
    assert connection is None

def test_close_connection():
    close_connection()
    assert connection is None

def test_add_records():
    assert add_records('', '') == 0

def test_update_records():
    assert update_records('', '', '') == 0

def test_delete_records():
    assert delete_records('','') == 0

def test_is_number():
    assert is_number('13', int)[0] == 13