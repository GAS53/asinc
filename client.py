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


def main():

    SOC = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    SOC.connect((HOST, PORT))
    log.info(f'у клиента создано соединение {HOST} {PORT}')
    log.info(f'количество переданнх аргументов {len(sys.argv)}')
    # in_put = input()
    
    if len(sys.argv) == 1:
        log.info('ping server')
        ping_cl = Ping(IM)
        ping_cl.send_to('server')
        # logging.info(ping_cl.run())
        SOC.send(ping_cl.run())

    elif len(sys.argv) == 2:
        msg = sys.argv[1]
        log.info(f'отправлено эхо-сообщение на сервер - {msg}')
        
        echo_cl = Echo(IM)
        echo_cl.send_to('server')
        
        SOC.send(echo_cl.run(msg))
        # recv = SOC.recv(1024)
        # log.info(f'получены данные от сервера {recv}')
        # check(recv)

    
    elif len(sys.argv) == 3:
        # print(sys.argv)
        send_to = sys.argv[1].lower()
        msg = sys.argv[2]
        if send_to == 'a' or send_to == 'all':
            log.info(f'Пользователь {IM} написал всем -{msg}')
            uu = User_all(IM)
            uu.send_to('all')
            SOC.send(uu.run(msg=msg))
        else:
            log.info(f'передан неизвестный аргумент - {send_to} должно быть u(user) или с(chat)')
            
    # elif len(sys.argv) == 4:
    #     print(sys.argv)
    #     which_rout = sys.argv[1].lower()
    #     send_to = sys.argv[2]
    #     msg = sys.argv[2]
    #     log.info(f'сообщени для {which_rout}')
    #     if which_rout == 'u' or which_rout == 'user':
    #         log.info(f'переписка user-user {IM}-{send_to}')
    #         uu = User_user(IM)
    #         uu.send_to(send_to)
    #         SOC.send(uu.run(msg=msg))
    #     elif which_rout == 'c' or which_rout == 'chat' or which_rout == 'a' or which_rout == 'chat':
    #         log.info(f'переписка user-chat {IM}-{send_to}')
    #         uc = User_chat(IM)
    #         uc.send_to(send_to)
    #         SOC.send(uc.run(msg=msg))
    #     else:
    #         log.info(f'передан неизвестный аргумент - {send_to} должно быть u(user) или с(chat)')
            

    recv = SOC.recv(1024)
    log.info('получены данные от сервера')
    check(recv)
    SOC.close()

if __name__=='__main__':
    main()
