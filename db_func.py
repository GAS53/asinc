from os import path
import sqlite3

import property



def create_tables(cur):
    tables = ['CREATE TABLE IF NOT EXISTS client(id SERIAL PRIMARY KEY, login char(32))',
    'CREATE TABLE IF NOT EXISTS user(id SERIAL PRIMARY KEY, login char(32))',
    'CREATE TABLE IF NOT EXISTS client_history (client_id INT NOT NULL, enter_time CHAR(7), enter_date CHAR(7), FOREIGN KEY (client_id) REFERENCES client(id) ON UPDATE CASCADE ON DELETE CASCADE)',
    'CREATE TABLE IF NOT EXISTS user_client (user_id INT not null, client_id INT not null, FOREIGN KEY (client_id) REFERENCES client(id) ON UPDATE CASCADE ON DELETE CASCADE, FOREIGN KEY (user_id) REFERENCES user(id) ON UPDATE CASCADE ON DELETE CASCADE)',]

    for table in tables:
        cur.execute(table)

def cleaner(li):
    # print(li)
    new_li = []
    for i in li:
        new_li.append(i[0])
    return new_li

def connect_db(command):
    print(property.DB_PATH)
    conn = sqlite3.connect(property.DB_PATH)
    with conn:
        cur = conn.cursor()
        if command:
            res = cur.execute(command)
            return cleaner(res.fetchall())
        else:
            create_tables(cur)


def get_my_frends():
    my_frends = []
    my_frends.append(property.MY_NONE)

    res = connect_db('SELECT login FROM client')  # переделать под запрос на сервер
    my_frends.extend(res)
    return my_frends




def get_my_chats():
    my_chats = []
    my_chats.append(property.MY_NONE)

    res = connect_db('SELECT login FROM client')   # переделать под запрос на сервер
    my_chats.extend(res)
    return my_chats

def get_requests(li):
    my_requests = []
    my_requests.append(property.MY_NONE)

    # res = connect_db('SELECT login FROM client')   # переделать под запрос на сервер
    my_requests.extend(li)
    return my_requests