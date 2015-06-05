# Testing Code to Print out DB Tables

import sqlite3 as lite

conn = lite.connect('data/cache.db')
cur = conn.cursor()

def get_items():
    cur.execute("SELECT * FROM Item")
    for record in cur.fetchall():
        print(record)

def get_urls():
    cur.execute("SELECT * FROM CachedURL")
    for record in cur.fetchall():
        print(record)


get_items()
get_urls()