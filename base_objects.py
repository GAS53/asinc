from abc import abstractclassmethod
import datetime
import json
import sys

class Base_message():
    def __init__(self):
        self.di = {}
        self.di['time'] = datetime.datetime.now().strftime('%c')
        self.di["action"] = self.chose_message_type()
        self.di['error'] = None
        self.di['from'] = sys.argv[0].split('/')[-1]
        self.di['status'] = self.chose_status()

    @abstractclassmethod
    def chose_message_type(self):
        print('необходимо выбрать тип сообщения в chose_message_type')

    @abstractclassmethod
    def chose_status(self):
        print('необходимо выбрать тип сообщения в chose_message_type')

    def run(self, msg=None, di=None):
        if msg:
            # print(f'msg {msg}')
            self.di['message'] = msg
        # print(f'self.di {self.di} type {type(self.di)}')
        if di:
            self.di.update(di)
        j_di = json.dumps(self.di)
        # print(f'run {j_di}')
        bj_di = j_di.encode('utf-8')
        return bj_di

class Ok_response(Base_message):
    def chose_status(self):
        return '200'

