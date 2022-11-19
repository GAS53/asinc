import socket
from socket import AF_INET, SOCK_STREAM
import logging.config
from threading import Lock, Thread
from queue import Queue
import sys

from property import HOST
from message_type import Ping, Echo, User_user, Chat, User_all, Standard_msg, Who, Admin_chat
from property import client_log_config
from overall import decoder, Check_port

from meta_clases import ClientVerifier


class Main(metaclass=ClientVerifier):
    def __init__(self):
        self.innit_logger()
        self.term_lock = Lock()
        self.send_queue = Queue()
        self.init_socket()


    def innit_logger(self):
        logging.config.dictConfig(client_log_config)
        self.log = logging.getLogger(f'client')


    def init_socket(self):
        Cp = Check_port()
        print(Cp.port)
        self.SOC = socket.socket(AF_INET, SOCK_STREAM)
        self.SOC.connect((HOST, Cp.port))

    def run(self):
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
    m = Main()
    m.run()

