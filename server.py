import logging
import logging.config
import socket
import select

from server_objects import check
from props import HOST, PORT, COUNT_DEQUE, term_or_file
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
    SOC.listen(COUNT_DEQUE)
    log.info(f'максимально возможная очередь {COUNT_DEQUE}')
    SOC.setblocking(False)

    return SOC

@Log(term_or_file)
def main():
    SOC = innit_connect()
    inputs = [SOC]  # сокеты, которые будем читать
    outputs = []  # сокеты, в которые надо писать
    messages ={} # здесь будем хранить сообщения для сокетов


    

    while True:
        try:
            reads, writes, errors = select.select(inputs, outputs, inputs, 0.2)
        except Exception as e:
                log.info(f'отключился клиент посмотреть какое исключение вышло - {e}')
        
        for conn in reads: # сокеты для чтения- что-то есть в сокетах для чтения
            if conn == SOC: # серверный сокет
                client_conn, client_addr = SOC.accept() # Проверка подключений
                log.info(f'создано соединение с {client_addr}')
                client_conn.setblocking(False)
                inputs.append(client_conn)
            else:  # клиентский сокет
                data = conn.recv(1024)
                if data:  # если от клиента что-то получено
                    if messages.get(client_conn, None):
                        messages[client_conn].append(data) # получено сообщение
                    else:
                        messages[conn] = [data]  # не получено сообщение
                    if client_conn not in outputs:
                        outputs.append(client_conn)
                else:  #  клиент отключился
                    
                    if client_conn in outputs:  # исключить клиента из сокетов для написания
                        outputs.remove(client_conn)
                    inputs.remove(client_conn)  # исключить клиента из сокетов для получения
                    client_conn.close() 
                    del messages[conn]
                    log.info(f'соединение с {client_addr} закрыто')
        

        for write_conn in writes:  # сокеты принимающие сообщения
            msg = messages.get(write_conn, None) # есть сообщения
            print(f'msg {msg}')
            if len(msg):
                it_send = check(msg.pop(0))
                if it_send:
                    log.info(f'от сервера требуется ответ по адресу {write_conn}')
                    write_conn.send(it_send)
                    log.info(f'с сервера клиенту отправлено сообщение')
        
            else:
                outputs.remove(write_conn)
                

        for exrror_conn in errors:
            log.info(f'клиент отключился с ошибкой {exrror_conn}')
            inputs.remove(exrror_conn)
            if conn in outputs:
                outputs.remove(exrror_conn)
            exrror_conn.close()
            log.info(f'для данного клиента закрываем соединение {exrror_conn}')
            del messages[exrror_conn]


        


if __name__=='__main__':
    main()