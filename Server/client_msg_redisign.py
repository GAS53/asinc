import sqlite3

from server_prop import DB_SERVER, SALT
from hashlib import pbkdf2_hmac


def get_dbpswd(login):
    conn = sqlite3.connect(DB_SERVER)
    with conn:
        cur = conn.cursor()
        cur.execute(f"select * from users where login='{login}' limit 1")
        res = cur.fetchall()
        if res:
            db_id, db_login, db_pswd = res[0]
            # db_pswd = db_pswd.encode('utf-8')
            return db_pswd
    return False

def make_pswd(pswd):
    pswd = pswd.encode('utf-8')
    pswd = pbkdf2_hmac('sha256', pswd, SALT, 100000)
    return str(pswd)



def identeficate(msg):
    if msg['action'] == 'handshake':
        try:
            login, pswd = msg['message']
            db_pswd = get_dbpswd(login)
            user_pswd = make_pswd(pswd)
            print(type(db_pswd))
            print(type(user_pswd))
            if user_pswd == db_pswd and user_pswd!= None and db_pswd !=None:
                print('пароль совпал')
                return True, login
            else:
                print('пароль не совпал')
                return True, False
                

        except Exception as e:
            print(f'exeption {e}')
            return False, False

    else:
        return False


def msg_redisign(msg):
    ...



def DDL():
    print(DB_SERVER)
    conn = sqlite3.connect(DB_SERVER)
    with conn:
        cur = conn.cursor()


        tables = ['CREATE TABLE IF NOT EXISTS client(id SERIAL PRIMARY KEY, login char(32))',
        'CREATE TABLE IF NOT EXISTS user(id SERIAL PRIMARY KEY, login char(32), password char(32))',
        'CREATE TABLE IF NOT EXISTS client_history (client_id INT NOT NULL, request char(32), date CHAR(20), FOREIGN KEY (client_id) REFERENCES client(id) ON UPDATE CASCADE ON DELETE CASCADE)',
        'CREATE TABLE IF NOT EXISTS user_history (user_id INT NOT NULL, request char(32), date CHAR(20), FOREIGN KEY (user_id) REFERENCES user(id) ON UPDATE CASCADE ON DELETE CASCADE)',
        'CREATE TABLE IF NOT EXISTS user_client (user_id INT not null, client_id INT not null, FOREIGN KEY (client_id) REFERENCES client(id) ON UPDATE CASCADE ON DELETE CASCADE, FOREIGN KEY (user_id) REFERENCES user(id) ON UPDATE CASCADE ON DELETE CASCADE)',
        'CREATE TABLE IF NOT EXISTS friends(im INT not null, friend INT not null, FOREIGN KEY (im) REFERENCES user(id) ON UPDATE CASCADE ON DELETE CASCADE, FOREIGN KEY (friend) REFERENCES user(id) ON UPDATE CASCADE ON DELETE CASCADE)',
        'CREATE TABLE IF NOT EXISTS frendship_request(im INT not null, friend INT not null, FOREIGN KEY (im) REFERENCES user(id) ON UPDATE CASCADE ON DELETE CASCADE, FOREIGN KEY (friend) REFERENCES user(id) ON UPDATE CASCADE ON DELETE CASCADE)',]

        for table in tables:
            cur.execute(table)

if __name__ == '__main__':
    DDL()
    # engine = create_engine()
    # engine.connect(DB_SERVER)
    # print(DB_SERVER)