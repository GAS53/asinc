import logging.config
import socket
from threading import Lock, Thread
from queue import Queue

from client_prop import client_log_config1
import net_func


logging.config.dictConfig(client_log_config1)
log = logging.getLogger(f'client')

class Main:
    def __init__(self, port):
        self.term_lock = Lock()
        self.send_queue = Queue()
        self.init_socket(port)


    def init_socket(self, port):
        self.SOC = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.SOC.connect((socket.gethostname(), port))
        log.info(f'инициализирован клиент')

    def run(self):
        th_get = Thread(target=self.send_msg)
        th_get.start()
        log.info('Запущен получающий клиент')

        # th_term = Thread(target=self.terminal_worker)
        # th_term.start()
        # log.info('Запущен клиент берущий из терминала')

здесь переделать под gui до этого все ошибки исправлены

    def send_msg(self):
        while True:
            mess = input('iput message:  ')
            # mess = self.send_queue.get()
            self.SOC.send(net_func.encoder(mess))

if __name__ == '__main__':
    M = Main(12561)
    M.run()