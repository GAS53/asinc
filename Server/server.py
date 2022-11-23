import logging.config
import socket
import select
import os
import hmac
import hashlib
from time import sleep

import server_prop
import net_func
from client_msg_redisign import identeficate, msg_redisign


logging.config.dictConfig(server_prop.server_log_config1)
log = logging.getLogger(f'server')



class Main:
    def __init__(self, port):
        self.inputs = []
        self.outputs = []
        self.innit_server(port)
        self.messages = {}
        self.auth_list = []
        self.ident = {}
        


    def innit_server(self, port):
        self.server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_sock.bind((socket.gethostname(), port))
        self.server_sock.listen(server_prop.MAX_CLIENTS)
        self.server_sock.setblocking(False)
        self.inputs.append(self.server_sock)
        log.info(f'инициализирован сервер')

    def updater(self, mess, key, val):
        if mess.get(key, None):
            mess[key].append(val) 
        else:
            mess[key] = [val]
        return mess

    def run(self):
        try:
            self.select_run()
        finally:
            self.disconnect()
            self.server_sock.close()

            log.info(f'сокет сервера закрыт')


    def del_client(self, conn, error=False):
        if error:
            log.info(f'клиент отключился с ошибкой')
        else:
            log.info(f'клиент отключился')

        if conn in self.outputs:
            self.outputs.remove(conn)
        if conn in self.inputs:
            self.inputs.remove(conn)
        if conn in self.auth_list:
            self.auth_list.remove(conn)
        if self.ident.get(conn):
            del self.ident[conn]

        conn.close()

    def disconnect(self):
        for i in self.outputs:
            self.del_client(i)
        for i in self.inputs:
            self.del_client(i)
        for i in self.auth_list:
            self.del_client(i)
        self.ident.clear()

 

        

    def select_run(self):
        while self.inputs:
            reads, send, excepts = select.select(self.inputs, self.outputs, self.inputs)
                       
            for conn in reads:
                if conn == self.server_sock:  # если это сокет, принимаем подключение
                    new_conn, client_addr = conn.accept()
                    new_conn.setblocking(False)
                    # id = self.add_client(new_conn)
                    self.inputs.append(new_conn)
                    log.info(f'подключился новый клиент {client_addr}\nстарт аутентификации')
                    
                    auth_msg = os.urandom(32)
                    new_conn.send(auth_msg)
                    hash = hmac.new(server_prop.AUTH_KEY, auth_msg, hashlib.sha256)
                    digest = hash.digest()
                    sleep(1)
                    response = new_conn.recv(len(digest))
                    sleep(1)
                    if hmac.compare_digest(digest, response):
                        log.info(f'аутентификация пройдена {client_addr}')
                        self.auth_list.append(new_conn)
                    else:
                        self.del_client(new_conn)
                        log.info(f'аутентификация НЕ пройдена {client_addr}')

                else:
                    data = conn.recv(1024)
                    data = net_func.decoder(data)
                    if isinstance(data, dict) and data['status'] == 200 and conn in self.auth_list:
                        if conn not in self.outputs: # даем готовность к приему
                            self.outputs.append(conn)
                        log.info(f'начало обработки сообщения от клиента {data}')
                        # print(f'from {client_addr[0]}')
                        data['from'] = client_addr[0]
                        if self.ident.get(conn):
                            msg_redisign(data)
                        else:
                            res, login = identeficate(data)
                            if not res:
                                log.info('Переданое сообщение не распознано {data}')
                            elif res and not login:
                                pre_msg = net_func.Base_message('ident_false','для проведения действий необходима идентификация. залогиньтесь.')
                                msg = pre_msg()
                                msg['to'] = data['from']
                                msg['from'] = 'server'
                                conn.sendall(net_func.encoder(msg))
                                # self.server_sock.sendall(net_func.encoder(msg))
                            
                            else:
                                self.ident[conn] = login
                                pre_msg = net_func.Base_message('ident_ok', login)
                                msg = pre_msg()

                                conn.sendall(net_func.encoder(msg))

                    else:
                        log.info(f'Передан не словарь клиент отключен {data}')
                        self.del_client(conn)




            # elif conn in self.outputs:
            #     self.outputs.remove(conn)

   
            for conn in excepts:
                self.del_client(conn, error=False)


if __name__ == '__main__':
    M = Main(12538)
    M.run()
