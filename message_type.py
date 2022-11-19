from abc import abstractclassmethod
import datetime
import json
import sys

class Base_message():
    def __init__(self):
        self.di = {}
        self.di['time'] = datetime.datetime.now().strftime('%c')
        self.di['action'] = None
        self.di['error'] = None
        self.di['from'] = None
        self.di['to'] = None
        self.di['status'] = self.chose_status()
        # self.init_status()

    def from_not_server(self, new):
        self.di['from'] = new

    # def init_status(self):
    #     if not self.di['action']:
    #         self.di['']

    # @abstractclassmethod
    # def chose_message_type(self, i):
    #     # print('необходимо выбрать тип сообщения в chose_message_type')
    #     self.di['action'] = i

        

    @abstractclassmethod
    def chose_status(self):
        print('необходимо выбрать тип сообщения в chose_message_type')

    def __repr__(self):
        return f"class {self.__class__.__name__} message type {self.di['action']} status {self.di['status']}"
    

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

    def get_recipient(self):
        return self.di['to']

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

    def __call__(self):
        return self.di


class Ok_response(Base_message):
    def __init__(self, i=None):
        super().__init__()
        self.di['action'] = i

    def chose_status(self):
        return '200'

class Handshake(Base_message):
    def __init__(self):
        super().__init__()
        self.di['action'] = 'handshake'

    def chose_status(self):
        return '200'



class Ping(Ok_response):
    def chose_message_type(self):
        return 'ping'
    

class Echo(Ok_response):
    def chose_message_type(self):
        return 'echo'

class Quit(Ok_response):
    def chose_message_type(self):
        return 'quit'

class Chat(Ok_response):
    def chose_message_type(self):
        return 'chat' 

class Admin_chat(Ok_response):
    def chose_message_type(self):
        return 'admin_chat' 

class User_user(Ok_response):
    # @abstractclassmethod
    def chose_message_type(self):
        return 'user'


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

class Who(Ok_response):
    def chose_message_type(self):
        return 'who'
