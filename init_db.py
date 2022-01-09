"""
WARNING!: deletes existing database file
"""

import os
import sqlite3

DB_FILE = "inventory.db"

if os.path.isfile(DB_FILE):
    os.remove(DB_FILE)

with sqlite3.connect(DB_FILE) as conn:
    cursor = conn.cursor()
    with open("schema.sql", "r") as schema_file:
        cursor.executescript(schema_file.read())
