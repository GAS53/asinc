import logging
import logging.config
import socket
import select

from server_objects import check
from props import HOST, PORT, term_or_file
from base_log_config import server_log_config
from base_objects import Log

logging.config.dictConfig(server_log_config)
log = logging.getLogger('server')
log.debug("Ведение журнала настроено.")

def innit_connect():
    SOC = socket.socket()
    log.info('создано соединение')

    SOC.bind((HOST, PORT))
    log.info('соединение настроено')
    count_deque = 5
    SOC.listen(count_deque)
    log.info(f'максимально возможная очередь {count_deque}')
    return SOC

@Log(term_or_file)
def main():
    clients = []
    SOC = innit_connect()

    while True:
        try:
            client, addr = SOC.accept() # Проверка подключений
        except OSError as e:
            pass
        else:
            log.info(f'создано соединение с {addr}')
            clients.append(client)
        finally:
            writest = []
            try:
                readst, writest, errorst = select.select([], clients, [], 0.2)
            except Exception as e:
                log.info(f'отключился клиент посмотреть какое исключение вышло - {e}')
        
 
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