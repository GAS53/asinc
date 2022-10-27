from os import path
import sqlite3

from property import DB_PATH

def check_tables(cur, is_clean=False):
    tables = ['CREATE TABLE IF NOT EXISTS client(id SERIAL PRIMARY KEY, login char(32))',
    'CREATE TABLE IF NOT EXISTS user(id SERIAL PRIMARY KEY, login char(32))',
    'CREATE TABLE IF NOT EXISTS client_history (client_id INT NOT NULL, enter_time CHAR(7), enter_date CHAR(7), FOREIGN KEY (client_id) REFERENCES client(id) ON UPDATE CASCADE ON DELETE CASCADE)',
    'CREATE TABLE IF NOT EXISTS user_client (user_id INT not null, client_id INT not null, FOREIGN KEY (client_id) REFERENCES client(id) ON UPDATE CASCADE ON DELETE CASCADE, FOREIGN KEY (user_id) REFERENCES user(id) ON UPDATE CASCADE ON DELETE CASCADE)',]
    # if is_clean:
    #     name_tables = cur.execute('.table')
    #     print(name_tables)

    for table in tables:
        cur.execute(table)

def connect_db():
    print(DB_PATH)
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

   
    check_tables(cur)  #, is_clean=True)



connect_db()
