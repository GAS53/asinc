import socket
import sys
import logging.config

from client_objects import check
from props import HOST, PORT
from base_objects import Ping, Echo
from base_log_config import client_log_config

IM = '123'

logging.config.dictConfig(client_log_config)
log = logging.getLogger(f'client_{IM}')
log.debug("Ведение журнала настроено.")





  # id client



def main():

    SOC = socket.socket()


    SOC.connect((HOST, PORT))
    log.info(f'у клиента создано соединение {HOST} {PORT}')

    if len(sys.argv) == 1:
        log.info('ping server')
        ping_cl = Ping(IM)
        ping_cl.send_to('server')
        # logging.info(ping_cl.run())
        SOC.send(ping_cl.run())

    elif sys.argv[1]:
        msg = sys.argv[1]
        log.info(f'отправлено эхо-сообщение на сервер - {msg}')
        
        echo_cl = Echo(IM)
        echo_cl.send_to('server')
        
        SOC.send(echo_cl.run(msg))
        
        



    recv = SOC.recv(1024)
    log.debug('получены данные от сервера')
    check(recv)
    SOC.close()

if __name__=='__main__':
    main()
