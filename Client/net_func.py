import json
import datetime

from Crypto.Cipher import AES

import client_prop

from client_prop import AUTH_KEY

def decoder(it):
    try:
        it = cript(it, encoding=False)
        print(f'befor json {it}')
        it = json.loads(it)
        print(f'befor cript {it}')
        return dict(it)
    except ValueError:
        return False


def encoder(it):
    it = json.dumps(it)
    print(f'after json {it}')
    
    print(f'after cript {it}')
    it = it.encode('utf-8')

    it = cript(it, encoding=True)
    return it

def padding(it):
    print(f'it {it}')
    count_space = (16 - len(it) % 16) % 16
    res = it + b' '*count_space

    print(f'res {res}')
    return res

count_cript = 0

def cript(it, encoding=True):
    global count_cript
    count_cript +=1
    print(f'count_cript {count_cript}')
    key = padding(AUTH_KEY)
    it = padding(it)


    if encoding:
        
        
        cipher = AES.new(key, AES.MODE_CBC)
        it = cipher.iv + cipher.encrypt(it)
    else:

        cipher = AES.new(key, AES.MODE_CBC, iv=it[:16])
        it = cipher.decrypt(it[16:])

    return it

def get_requests(li):
    my_requests = []
    my_requests.append(client_prop.MY_NONE)

    # res = connect_db('SELECT login FROM client')   # переделать под запрос на сервер
    my_requests.extend(li)
    return my_requests


class Base_message():
    def __init__(self, action, msg=None, di=None):
        self.di = {}
        self.di['time'] = datetime.datetime.now().strftime('%c')
        self.di['action'] = action
        # self.di['to'] = None
        self.di['status'] = 200
        if msg:
            self.di['message'] = msg
        if di:
            self.di.update(di)


    def from_not_server(self, new):
        self.di['from'] = new


    def __repr__(self):
        return f"class {self.__class__.__name__} message type {self.di['action']} status {self.di['status']}"
    

    def get_target(self):
        return self.di['to']

    def __call__(self):
        return self.di

if __name__ == '__main__':
    Bm = Base_message('ping')
    print(Bm())
