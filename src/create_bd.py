import sqlite3

conn = sqlite3.connect("data/db.db")
cursor = conn.cursor()

# Создание таблицы
cursor.execute("""CREATE TABLE user
                  (id INTEGER PRIMARY KEY, id_tg INTEGER UNIQUE, name CHAR, email CHAR, password CHAR, money CHAR,
                  user_sh BIT)
               """)

cursor.execute("""CREATE TABLE site
                  (email CHAR, money CHAR)""")
