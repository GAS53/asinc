import logging.config
import socket
import select
import os
import hmac
import hashlib

import server_prop
import net_func


logging.config.dictConfig(server_prop.server_log_config1)
log = logging.getLogger(f'server')



class Main:
    def __init__(self, port):
        self.inputs = []
        self.outputs = []
        self.innit_server(port)
        self.messages = {}
        self.auth_list = []
        


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

        conn.close()
 

        

    def select_run(self):
        while self.inputs:
            new_messages = None
            reads, send, excepts = select.select(self.inputs, self.outputs, self.inputs)
            # print(f'before 3x3 {len(reads)} {len(send)} {len(excepts)} --- {len(self.inputs)} {len(self.outputs)} {len(self.inputs)}\n')
            
            for conn in reads:
                if conn == self.server_sock:  # если это сокет, принимаем подключение
                    new_conn, client_addr = conn.accept()
                    new_conn.setblocking(False)
                    # id = self.add_client(new_conn)
                    self.inputs.append(new_conn)
                    log.info(f'подключился новый клиент {client_addr}\nстарт аутентификации')
                    
                    auth_msg = os.urandom(32)
                    new_conn.send(auth_msg)
                    hash = hmac.new(server_prop.AUTH_KEY, auth_msg, hashlib.sha1)
                    digest = hash.digest()
                    
                    response = new_conn.recv(len(digest))
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
                        
                        self.client_msg_redisign(data)                                                
                        
                    else:
                        print(f'Передан не словарь {data}')
                        self.del_client(conn)



            if new_messages:
                for message in new_messages:
                    res = f'сообщение {message["message"]} от {message["from"]} к {message["to"]}' if message.get('message') else f'статус {message["status"]}'
                    log.info(res)
                    send_to = message['to']
                    print(f' send to in new_messages {send_to}')
                    for id_recipient in send_to:
                        recip_sock = self.id_sock[id_recipient]
                        recip_sock.sendall(net_func.encoder(message))
 
                    del new_messages  
            elif conn in self.outputs:
                self.outputs.remove(conn)

   
            for conn in excepts:
                self.del_client(conn, error=False)


    def client_msg_redisign(self, msg):
        log.info(f'начало обработки сообщения от клиента {msg}')

if __name__ == '__main__':
    M = Main(12571)
    M.run()
