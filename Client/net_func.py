'''функции для работы с сетью'''

import json
import datetime

from Crypto.Cipher import AES

import client_prop

from client_prop import AUTH_KEY

def decoder(it):
    ''' Декодировщик сообщений '''
    try:
        it = cript(it, encoding=False)
        it = json.loads(it)
        return dict(it)
    except ValueError:
        return False


def encoder(it):
    ''' Кодировщик сообщений '''
    it = json.dumps(it)
    it = it.encode('utf-8')
    it = cript(it, encoding=True)
    return it

def padding(it):
    ''' Добавление дополнительных символов необходимо для кодирования'''
    count_space = (16 - len(it) % 16) % 16
    res = it + b' '*count_space
    return res

def cript(it, encoding=True):
    ''' Шифрование сообщения '''
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
    ''' Создание списка запросов включая первый None (MY_NONE)'''
    my_requests = []
    my_requests.append(client_prop.MY_NONE)
    my_requests.extend(li)
    return my_requests


class Base_message():
    ''' Базовый тип сообщения '''
    def __init__(self, action, msg=None, di=None):
        ''' Инициализация базового сообщения'''
        self.di = {}
        self.di['time'] = datetime.datetime.now().strftime('%c')
        self.di['action'] = action
        # self.di['to'] = None
        self.di['status'] = 200
        if msg:
            self.di['message'] = msg
        if di:
            self.di.update(di)

    def __repr__(self):
        return f"class {self.__class__.__name__} message type {self.di['action']} status {self.di['status']}"
    
    def __call__(self):
        return self.di

if __name__ == '__main__':
    Bm = Base_message('ping')
    print(Bm())
