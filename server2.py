import logging
import logging.config
import socket
import select
import queue

from server_objects import check
from props import term_or_file, HOST, PORT, COUNT_DEQUE
from base_log_config import server_log_config
from base_objects import Log, decoder

logging.config.dictConfig(server_log_config)
log = logging.getLogger('server')
log.debug("Ведение журнала настроено.")


def innit_connect():
    SOC = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    log.info('создано соединение')
    SOC.bind((HOST, PORT))
    log.info('соединение настроено')
    SOC.listen(COUNT_DEQUE)
    log.info(f'максимально возможная очередь {COUNT_DEQUE}')
    SOC.setblocking(False)
    return SOC


@Log(term_or_file)
def main():
    sock = innit_connect()
    inputs = [sock]  # сокеты, которые будем читать
    outputs = []  # сокеты, в которые надо писать
    messages ={} # здесь будем хранить сообщения для сокетов
    

    while inputs:
        reads, send, excepts = select.select(inputs, outputs, inputs, 0.2)

        for conn in reads:#  сокеты, готовые к чтению
            if conn == sock:  # серверный сокет значит пришло просто подклчюение
                new_conn, client_addr = conn.accept()
                new_conn.setblocking(False)
                log.info(f'создано соединение с {client_addr}')
                inputs.append(new_conn) # очередь на прослушивание

            else:  # клиентский сокет значит пришла информация
                data = conn.recv(1024)
                if data:  # если от клиента что-то получено
                    if messages.get(conn, None):
                        messages[conn].append(data) # добавим в словарь сообщеий
                    else:
                        messages[conn] = [data]

                    if conn not in outputs:
                        outputs.append(conn)

                else:  #  клиент отключился
                    if conn in outputs:
                        outputs.remove(conn)  # исключить клиента из сокетов для написания
                    inputs.remove(conn)  # исключить клиента из сокетов для получения
                    conn.close()
                    del messages[conn]
                    log.info(f'соединение закрыто')

                    # if conn in outputs:  
                    #     outputs.remove(conn)
                    # inputs.remove(conn)  
                    # conn.close() 
                    # del messages[conn]

        for conn in send:  # сокеты, готовые принять сообщение
            msg = messages.get(conn, None)
            

            if msg:
                msg = msg.pop(0)
                print(f'type {type(msg)}')
                msg = check(msg)
                print(f'msg {msg}')
                print(f'type {type(msg)}')

            
                    
        # for msg_conn, data in messages.items():
        #     # data = decoder(data)
        #     print(f'data {data[0]}')
        #     data = check(data[0])
        #     print(f'type {type(data)}')
        #     if data['action'] == 'all':
        #         for conn in send:
        #             conn.send(data)
        #     elif data['action'] in ['ping', 'echo']:
        #         for conn in send:
        #             if conn == msg_conn:
        #                 conn.send(data)
        #     else:
        #         outputs.remove(conn)



        
        
           
            # except queue.Empty as e:
            # log.info(f'ошибка в исходящих - ')
            # print(f'write_conn {write_conn} all conn - {writes}')
            # outputs.remove(write_conn)
            # if len(msg):
            #     log.info(f'сообщение на отправку {msg}')
            
                
            #     it_send, send_to = check(msg)  #.pop(0))
            #     log.info(f'результат проверки сообщения')  # {it_send}')
            #     if send_to == 'im':
            #         # log.info(f'от сервера требуется ответ по адресу {write_conn}')
            #         conn.send(it_send)
            #         log.info(f'с сервера клиенту отправлено сообщение')
            #         # log.info(f'с сервера клиенту отправлено сообщение {it_send}')
            #     elif send_to == 'all':
            #         log.info(f'с сервера всем отправлено сообщение')
            #         # print(readable)
            #         for a in readable:
            #             print(f'сообщение {send_to} отправлено {a}')
            #             a.send(it_send)
            #     else:
            #         outputs.remove(conn)
                        
                    

                
                

        for exrror_conn in excepts:  # обработчик исключений
            log.info(f'клиент отключился с ошибкой {exrror_conn}')
            inputs.remove(exrror_conn)
            if conn in outputs:
                outputs.remove(exrror_conn)
            exrror_conn.close()
            log.info(f'для данного клиента закрываем соединение {exrror_conn}')
            del messages[exrror_conn]


        


if __name__=='__main__':
    main()
