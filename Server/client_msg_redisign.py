import sqlite3


from hashlib import pbkdf2_hmac

from server_prop import DB_SERVER, SALT
import net_func


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
            if user_pswd == db_pswd and user_pswd != None and db_pswd != None:
                print('пароль совпал')
                return True, login
            else:
                print('пароль не совпал')
                return True, False
                

        except Exception as e:
            print(f'exeption {e}')
            return False, False

    else:
        return False, False


def msg_sender(msg, conn_dict):
    recipients = msg['to']
    byte_msg = net_func.encoder(msg)
    if isinstance(recipients, list):
        for send_login, conn in conn_dict.items():
            if send_login in recipients:
                conn.sendall(byte_msg)
    else:
       conn = conn_dict[recipients]
       conn.sendall(byte_msg)


def msg_routing(in_msg, inner_login, conn_dict):
    print(f'обработка входящего {in_msg}')


    if in_msg['action'] == 'ping':
        pre_msg = net_func.Base_message('re_ping')
        msg = pre_msg()
        msg['to'] = inner_login
        msg['from'] = 'server'
        msg['message'] = 'ping прошел успешно'
    # elif in_msg['action'] == 'ping':
    # !!!!!!!!!!!!!!





    msg_sender(msg, conn_dict)





def get_revers(di):
    new_di = {}
    for k, v in di.items():
        new_di[v] = k
    return new_di




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