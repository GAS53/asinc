import socket
import sys
import logging.config

from client_objects import check
from props import HOST, PORT, term_or_file
from base_objects import Ping, Echo, User_user, User_chat, User_all
from base_log_config import client_log_config


IM = '123'

logging.config.dictConfig(client_log_config)
log = logging.getLogger(f'client_{IM}')
log.debug("Ведение журнала настроено.")

print('Для выхода из чата наберите: `exit`, `quit` или `q`.')

SOC = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
SOC.connect((HOST, PORT))


with SOC as s:

    
    while True:
        mess = input('\nВведите что нибудь >>> ')
        if any(mess.lower() in ext for ext in ['quit', 'exit', 'q']):
            break  
        # mess = mess.encode('utf-8')
        ua = User_all(IM)      
        # ua = Echo(IM)    
        s.sendall(ua.run(msg=mess))

        data = s.recv(1024)
        print('\nПолучено: ', data.decode('utf-8'))