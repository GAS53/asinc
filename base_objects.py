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
        self.di['im'] = sys.argv[0].split('/')[-1]

    @abstractclassmethod
    def chose_message_type(self):
        print('необходимо выбрать тип сообщения в chose_message_type')


    def run(self, msg):
        if msg:
            # print(f'msg {msg}')
            self.di['message'] = msg
        # print(f'self.di {self.di} type {type(self.di)}')
        j_di = json.dumps(self.di)
        # print(f'run {j_di}')
        bj_di = j_di.encode('utf-8')
        return bj_di