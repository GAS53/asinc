import json
import datetime

import client_prop

def decoder(it):
    try:
        # print(f'in decoder {it}')
        it = json.loads(it)
        return dict(it)
    except ValueError:
        return False


def encoder(it):
    # print(f'in encoder {it}')
    it = json.dumps(it)
    it = it.encode('utf-8')
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
