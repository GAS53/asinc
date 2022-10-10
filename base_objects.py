from abc import abstractclassmethod
import datetime
import json
import sys
import socket

from props import HOST, PORT, COUNT_DEQUE
from props import PATH_LOGGING_CALL_FUNC


def decoder(it):
    it = it.decode('utf-8')
    print(f'type {type(it)}')
    it = json.loads(it)
    return dict(it)

class Log:
    def __init__(self, in_put='terminal'):
        self.in_put = in_put


    
    def __call__(self, func):
        def wrapper(*args):
            if self.in_put == 'terminal':
                print(f'call func - {func.__name__} with arg {args} class {__class__.__name__}')
            elif self.in_put == 'file' :
                with open(PATH_LOGGING_CALL_FUNC, 'a') as file:
                    file.write(f'call func - {func.__name__} with arg {args} class {__class__.__name__}\n')
            else:
                raise TypeError('неверно задан параметр в функции Log должен быть "file" или "terminal"')

            res = func(*args)
            return res
        return wrapper

# @Log('terminal')
class Base_message():
    def __init__(self, im):
        self.di = {}
        self.di['time'] = datetime.datetime.now().strftime('%c')
        self.di['action'] = self.chose_message_type()
        self.di['error'] = None
        self.di['from'] = im
        self.di['to'] = None
        self.di['status'] = self.chose_status()

    def from_not_server(self, new):
        self.di['from'] = new

    @abstractclassmethod
    def chose_message_type(self):
        print('необходимо выбрать тип сообщения в chose_message_type')
        

    @abstractclassmethod
    def chose_status(self):
        print('необходимо выбрать тип сообщения в chose_message_type')

    def __repr__(self):
        return f"class {self.__class__.__name__} message type {self.di['action']} status {self.di['status']}"
    
    # @abstractclassmethod
    # def who_im(self):
    #     print('необходимо указать server или id клиента')

    def clean_di(self):
        res_di = {}
        for k, v in self.di.items():
            if v:
                res_di[k] = v
        return res_di

    def send_to(self, recipient):
        if sys.argv[0].split('/')[-1]  == 'server':
            self.di['to'] = 'server'
        elif recipient:
            self.di['to'] = recipient
        else:
            raise ValueError('для сообщения в send_to, должен быть указан отправитель')

    def get_target(self):
        return self.di['to']

    def run(self, msg=None, di=None):
        if msg:
            self.di['message'] = msg

        if di:
            self.di.update(di)
        
        
        res_di = self.clean_di()
        # print(f'res_di {res_di}')
        j_di = json.dumps(res_di)

        bj_di = j_di.encode('utf-8')
        return bj_di

# @Log('terminal')
class Ok_response(Base_message):
    def chose_status(self):
        return '200'
# @Log('terminal')
class Ping(Ok_response):
    def chose_message_type(self):
        return 'ping'
    
# @Log('terminal')
class Echo(Ok_response):
    def chose_message_type(self):
        return 'echo'

class Quit(Ok_response):
    def chose_message_type(self):
        return 'quit'


class Chat_connect(Ok_response):
    def chose_message_type(self):
        return 'connect_chat'  

class User_user(Ok_response):
    def chose_message_type(self):
        return 'user_user'

class User_chat(Ok_response):
    def chose_message_type(self):
        return 'user_chat'

class User_all(Ok_response):
    def chose_message_type(self):
        return 'all'

class Standard_msg(Ok_response):
    def chose_message_type(self):
        return 'msg'


class Request_auth(Ok_response):
    def chose_message_type(self):
        return 'auth'


class Wrong_account(Base_message):
    def chose_status(self):
        return '400'
    

class Already_connected(Base_message):
    def chose_status(self):
        return '409'
    


