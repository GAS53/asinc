from os import path
import sqlite3
from property import DB_SERVER, DB_CLIENT

import property

def check_user(in_put):
    login, password = in_put
    print(f'login {login} password {password}')
    conn = sqlite3.connect(DB_SERVER)
    with conn:
        cur = conn.cursor()
        cur.execute(f"select login, password from user where login='{login}' and  password='{password}';")
        res = cur.fetchall()
        if res:
            print(f'логин и пароль корректные{res}')
            return 'ok'
        else:
            print(f'Введениы неверные логин и/или пароль')
            return None




def get_from_server():
    res = None
    conn = sqlite3.connect(DB_SERVER)
    with conn:
        cur = conn.cursor()
        # cur.execute("select im, friend from friends f join user u on u.id=f.im where u.im='1' and not u.friend='null';")
        cur.execute("select im, friend from friends where im='1' and not friend='null';")
        res = cur.fetchall()
        print(res)

# get_from_server()

def get_my_frends(im):
    conn = sqlite3.connect(DB_SERVER)
    with conn:
        cur = conn.cursor()
        cur.execute(f"select im, friend from friends where im='{im}' and not friend='null';")
        res = cur.fetchall()
        my_friends = []
        for i_f in res:
            my_friends.append(i_f[1])
        return my_friends

def del_frend(im, friend):
    conn = sqlite3.connect(DB_SERVER)
    with conn:
        cur = conn.cursor()
        cur.execute(f"select im, friend from friends where im='{im}' and friend='{friend}' or im={friend} and friend='{im}';")
        res = cur.fetchall()
        if res == []:
            return f"вы с {friend} небыли друзьями"
        else:
            cur.execute(f"DELETE FROM friends WHERE im='{im}' and friend='{friend}' or im={friend} and friend='{im}';")
            return f"удаление из друзей {friend} успешно выполнено"


def add_frend(im, friend):
    conn = sqlite3.connect(DB_SERVER)
    with conn:
        cur = conn.cursor()
        cur.execute(f"select im, friend from friends where im='{im}' and friend='{friend}' or im={friend} and friend='{im}';")
        res = cur.fetchall()
        if res != []:
            return  f"вы с {friend}  уже являетесь друзьями"
        else:
            cur.execute(f"SELECT im, friend FROM frendship_request WHERE im='{im}' friend='{friend}';")
            fr_req_bean = cur.fetchall()
            if fr_req_bean :
                return "вы уже делали запрос на дружбу с {friend}, он пока не соглсился его принять"
            else:
                cur.execute(f"SELECT im, friend FROM frendship_request WHERE im='{friend}' friend='{im}';")
                frend_get_request = cur.fetchall()
                if  frend_get_request:
                    cur.execute(f"DELETE FROM TABLE  frendship_request WHERE im='{friend}' friend='{im}';")
                    cur.execute(f"ALTER TABLE friends({friend} {im}")
                    return  f"вы приняли заявку добавления в друзья от {friend}"
                else:
                    cur.execute(f"ALTER TABLE frendship_request({im} {friend}")
                    return f"вы подали заявку на добавление в друзья к {friend}"



def create_server(cur):
    tables = ['CREATE TABLE IF NOT EXISTS client(id SERIAL PRIMARY KEY, login char(32))',
    'CREATE TABLE IF NOT EXISTS user(id SERIAL PRIMARY KEY, login char(32), password char(32))',
    'CREATE TABLE IF NOT EXISTS client_history (client_id INT NOT NULL, request char(32), date CHAR(20), FOREIGN KEY (client_id) REFERENCES client(id) ON UPDATE CASCADE ON DELETE CASCADE)',
    'CREATE TABLE IF NOT EXISTS user_history (user_id INT NOT NULL, request char(32), date CHAR(20), FOREIGN KEY (user_id) REFERENCES user(id) ON UPDATE CASCADE ON DELETE CASCADE)',
    'CREATE TABLE IF NOT EXISTS user_client (user_id INT not null, client_id INT not null, FOREIGN KEY (client_id) REFERENCES client(id) ON UPDATE CASCADE ON DELETE CASCADE, FOREIGN KEY (user_id) REFERENCES user(id) ON UPDATE CASCADE ON DELETE CASCADE)',
    'CREATE TABLE IF NOT EXISTS friends(im INT not null, friend INT not null, FOREIGN KEY (im) REFERENCES user(id) ON UPDATE CASCADE ON DELETE CASCADE, FOREIGN KEY (friend) REFERENCES user(id) ON UPDATE CASCADE ON DELETE CASCADE)',
    'CREATE TABLE IF NOT EXISTS frendship_request(im INT not null, friend INT not null, FOREIGN KEY (im) REFERENCES user(id) ON UPDATE CASCADE ON DELETE CASCADE, FOREIGN KEY (friend) REFERENCES user(id) ON UPDATE CASCADE ON DELETE CASCADE)',]

    for table in tables:
        cur.execute(table)

def create_client(cur):
    tables = ['CREATE TABLE IF NOT EXISTS history(id SERIAL PRIMARY KEY, is_im int default(1), chat_user char(32), msg char(256), date CHAR(20))',]



    for table in tables:
        cur.execute(table)

def cleaner(li):
    # print(li)
    new_li = []
    for i in li:
        new_li.append(i[0])
    return new_li

def make_dbs(db_path=None):
    print(f'make {db_path}')
    conn = sqlite3.connect(db_path)
    with conn:
        cur = conn.cursor()
        if db_path == DB_SERVER:
            create_server(cur)
        elif db_path == DB_CLIENT:
            create_client(cur)
        else:
            print(f'error make db')




# def get_my_frends():
#     my_frends = []
#     my_frends.append(property.MY_NONE)

#     res = connect_db('SELECT login FROM client')  # переделать под запрос на сервер
#     my_frends.extend(res)
#     return my_frends




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

if __name__=='__main__':
    make_dbs(DB_CLIENT)
    make_dbs(DB_SERVER)