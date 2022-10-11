import socket
import logging.config
from uuid import uuid1
import sys

import message_type
from property import HOST
# from base_objects import Ping, Echo, User_user, User_chat, User_all
from property import client_log_config


class Main():
    def __init__(self, port):
        self.id = uuid1()
        self.innit_logger()
        self.port = int(port)


    def innit_logger(self):
        logging.config.dictConfig(client_log_config)
        self.log = logging.getLogger(f'client_{self.id}')


    def init_socket(self):
        self.SOC = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.SOC.connect((HOST, self.port))


    def run(self):
        self.init_socket()
        while True:
            mess = input('\nВведите что нибудь >>> ')
            if any(mess.lower() in ext for ext in ['quit', 'exit', 'q']):
                break  

            ua = message_type.User_all(self.id)      
            # ua = Echo(IM)    
            self.SOC.sendall(ua.run(msg=mess))

            data = self.SOC.recv(1024)
            print('\nПолучено: ', data.decode('utf-8'))

if __name__ == '__main__':
    m = Main(sys.argv[1])
    m.run()