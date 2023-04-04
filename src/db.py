import sqlite3
from .config import SQLITE_DB_FILE
import os


class DataBase:
    def __init__(self):
        self.conn = sqlite3.connect(os.path.join('src', SQLITE_DB_FILE), check_same_thread=False)
        self.cursor = self.conn.cursor()


def get_all_user():
    return cursor.execute('''SELECT * FROM user ''').fetchall()


def get_user(user_id_tg):
    return cursor.execute('''SELECT * FROM user WHERE id_tg=? ''', (user_id_tg, )).fetchone()


def create_user(user_id_tg, user_name):
    cursor.execute('''INSERT INTO user(id_tg, name, user_sh ) VALUES(?, ?, ?);''', (user_id_tg, user_name, False))
    conn.commit()


def get_user_sh(user_id_tg):
    return cursor.execute('''SELECT user_sh FROM user WHERE id_tg=? ''', (user_id_tg, )).fetchone()


def get_money(user_id_tg):
    return cursor.execute('''SELECT money FROM user WHERE id_tg=? ''', (user_id_tg, )).fetchone()[0]


def minus_money(user_id_tg, money):
    money_now = int(get_money(user_id_tg))
    cursor.execute('''UPDATE user SET money = ? WHERE id_tg=?;''',
                   (money_now - money, user_id_tg))
    conn.commit()


def update_status_sh(user_id_tg, email, password, money, user_sh):
    cursor.execute('''UPDATE user SET (email, password, money, user_sh) = (?, ?, ?, ?) WHERE id_tg=?;''',
                   (email, password, money, user_sh, user_id_tg))
    conn.commit()


def get_money_for_reg(email):
    return cursor.execute('''SELECT money FROM site WHERE email=? ''', (email,)).fetchone()[0]


def set_money(email, money):
    cursor.execute('''INSERT INTO site(email, money) VALUES(?, ?);''', (email, money))
    conn.commit()


def clear_tables():
    cursor.execute('''DELETE FROM site;''')
    cursor.execute('''DELETE FROM user;''')
    conn.commit()


if __name__ == '__main__':
    init_db()
    print(cursor.execute('''SELECT * FROM user ''').fetchall())
    print(cursor.execute('''SELECT * FROM site ''').fetchall())
