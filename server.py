import logging
import logging.config
import socket

from server_objects import check
from props import HOST, PORT
# from .log import server_log_config
from log.base_log_config import server_log_config

logging.config.dictConfig(server_log_config)
log = logging.getLogger('main')

def main():
    SOC = socket.socket()

    SOC.bind((HOST, PORT))
    SOC.listen(5)

    while True:

        client, addr = SOC.accept()
        print(f'соединение с {addr}')
        log.info(f'соединение с {addr}')
        res = client.recv(1024)

        it_send = check(res)
        if it_send:
            log.info(f'от сервера требуется ответ на {addr}')
            client.send(it_send)
            log.debug(f'с сервера клиенту отправлено сообщение')
        client.close()
        log.info(f'соединение с {addr} закрыто')


if __name__=='__main__':
    main()