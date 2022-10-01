from abc import abstractclassmethod
import datetime
import json
import sys

class Base_message():
    def __init__(self, im):
        self.di = {}
        self.di['time'] = datetime.datetime.now().strftime('%c')
        self.di['action'] = self.chose_message_type()
        self.di['error'] = None
        self.di['from'] = im
        self.di['to'] = None
        self.di['status'] = self.chose_status()

    @abstractclassmethod
    def chose_message_type(self):
        print('необходимо выбрать тип сообщения в chose_message_type')
        

    @abstractclassmethod
    def chose_status(self):
        print('необходимо выбрать тип сообщения в chose_message_type')

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


    def run(self, msg=None, di=None):
        if msg:
            # print(f'msg {msg}')
            self.di['message'] = msg
        # print(f'self.di {self.di} type {type(self.di)}')
        if di:
            self.di.update(di)
        
        res_di = self.clean_di()
        j_di = json.dumps(res_di)
        # print(f'run {j_di}')
        bj_di = j_di.encode('utf-8')
        return bj_di


class Ok_response(Base_message):
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


class Chat_connect(Ok_response):
    def chose_message_type(self):
        return 'connect_chat'  

class User_user(Ok_response):
    def chose_message_type(self):
        return 'user_user'

class User_chat(Ok_response):
    def chose_message_type(self):
        return f'user_chat'



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
    
