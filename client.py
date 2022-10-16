import socket
import logging.config
from threading import Lock, Thread
from queue import Queue
# from uuid import uuid1
import sys

import message_type
from property import HOST
from message_type import Make_chat, Ping, Echo, User_user, Chat, User_all, Standard_msg, Who
from property import client_log_config
from overall import decoder


class Main():
    def __init__(self, port):
        # self.id = getter
        self.innit_logger()
        self.port = int(port)
        self.term_lock = Lock()
        # self.get_queue = Queue()
        self.send_queue = Queue()
        self.init_socket()


    def innit_logger(self):
        logging.config.dictConfig(client_log_config)
        self.log = logging.getLogger(f'client')


    def init_socket(self):
        self.SOC = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.SOC.connect((HOST, self.port))

    def run(self):
        # try:
        th_get = Thread(target=self.get_msg)
        th_get.start()
        self.log.info('Запущен получающий клиент')

        th_term = Thread(target=self.terminal_worker)
        th_term.start()
        self.log.info('Запущен клиент берущий из терминала')

        th_send = Thread(target=self.send_msg)
        th_send.start()
        self.log.info('Запущен отправляющий клиент')

        


    def terminal_worker(self):
        while True:
            # здесь бы with self.term_lock
            in_res = input('введите сообщение(пример: a написать всем\n')
            in_res = in_res.split()
            print(f'inres split {in_res}')
            send_config = in_res[0].lower()


            if send_config == 'a':
                ua = User_all()
                str_msg = ' '.join(in_res[1:])
                msg = ua.run(msg=str_msg)

            elif send_config == 'u':
                id_user = in_res[1]
                uu = User_user()
                uu.send_to(id_user)  # разобрться как выбрать пользователя для отправки
                str_msg = ' '.join(in_res[2:])
                print(f'str_msg {type(str_msg)}')
                msg = uu.run(msg=str_msg)

            elif send_config == 'p':
                p = Ping()
                msg = p.run()

            elif send_config == 'e':
                e = Echo()
                str_msg = ' '.join(in_res[1:])
                msg = e.run(msg=str_msg)

            elif send_config in ['w', 'who']:
                w = Who()
                msg = w.run()


            elif send_config == 'chat':
                ch = Chat()
                str_msg = ' '.join(in_res[1:])
                msg = ch.run(msg=str_msg)


            else:
                sm = Standard_msg()
                msg = sm.run(msg='тестовое сообщение')



            
            self.send_queue.put(msg)



    def get_msg(self):
        while True:
            data = self.SOC.recv(1024)
            with self.term_lock:
                data = decoder(data)
                res = f'сообщение {data["message"]}' if data.get('message') else f'статус {data["status"]}'
                print(res)

    def send_msg(self):
        while True:
            mess = self.send_queue.get()
            self.SOC.send(mess)


if __name__ == '__main__':
    m = Main(sys.argv[1] )
    m.run()

