import logging
import logging.config
import socket

from server_objects import check
from props import HOST, PORT, term_or_file
from base_log_config import server_log_config
from base_objects import Log

logging.config.dictConfig(server_log_config)
log = logging.getLogger('server')
log.debug("Ведение журнала настроено.")

@Log(term_or_file)
def main():
    SOC = socket.socket()
    log.info('создано соединение')

    SOC.bind((HOST, PORT))
    log.info('соединение настроено')
    count_deque = 5
    SOC.listen(count_deque)
    log.info(f'максимально возможная очередь {count_deque}')

    while True:

        client, addr = SOC.accept()
        log.info(f'создано соединение с {addr}')
 
        res = client.recv(1024)
        log.info(f'от клиента получены данные')

        it_send = check(res)
        if it_send:
            log.info(f'от сервера требуется ответ по адресу {addr}')
            client.send(it_send)
            log.info(f'с сервера клиенту отправлено сообщение')
        client.close()
        log.info(f'соединение с {addr} закрыто')


if __name__=='__main__':
    main()