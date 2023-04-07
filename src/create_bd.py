import sqlite3

conn = sqlite3.connect("data/db.db")
cursor = conn.cursor()

# Создание таблицы
cursor.execute("""CREATE TABLE user
                  (id INTEGER PRIMARY KEY, id_tg INTEGER UNIQUE, name CHAR, coins INTEGER, commands CHAR,
                   ingame BIT)
               """)
