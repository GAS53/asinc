

import select
import socket
import logging
import logging.config
from queue import Queue
import sys
from uuid import uuid1

from property import PORT, HOST, client_log_config
from overall import decoder, encoder




logging.config.dictConfig(client_log_config)
log = logging.getLogger(f'server_')


class Main():
    def __init__(self, port):
        self.port = int(port)
        self.inputs = []
        self.sock = self.innit_server()
        
        self.outputs = []
        self.messages = {}
        self.id_sock = {}
        self.sock_id ={}

    def innit_server(self):
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.setblocking(False)
        server.bind((HOST, self.port))
        server.listen(5)
        self.inputs.append(server)
        log.info(f'инициализирован сервер')
        return server

    def updater(self, mess, key, val):
        if mess.get(key, None):
            mess[key] = val
        else:
            mess[key].append(val)
        return mess

    def add_client(self, sock):
        id = uuid1()
        self.id_sock[id] = sock
        self.sock_id[sock] = id
        log.info(f'подключился клиент {id}')
        return id

    def del_client(self, conn, error=None):
        if conn in self.outputs:
            self.outputs.remove(conn)
        self.inputs.remove(conn)
        conn.close()
        del self.messages[conn]
        id =None
        id = self.sock_id.get(conn)
        del self.sock_id[conn]
        del self.id_sock[id]
        if error:
            log.info(f'клиент {id} отключился с ошибкой')
        else:
            log.info(f'клиент {id} отключился')

    def message_refactor(self):
        new_messages = {}
        for id, data in self.messages.items():
            if data['action'] == 'ping' or data['action'] == 'echo':
                new_messages = self.updater(new_messages, data, id)
            elif data['action'] == 'all':
                for id in self.id_sock.keys():
                    new_messages = self.updater(new_messages, data, id)
            elif "user_" in  data['action']:
                id = data['action'].replace("user_", "")
                self.updater(new_messages, data, id)
        self.messages.clear()
        return new_messages



    def run(self):
        while True:
            reads, send, excepts = select.select(self.inputs, self.outputs, self.inputs)
            for conn in reads:
                if conn == self.sock:  # если это сокет, принимаем подключение
                    new_conn, client_addr = conn.accept()
                    new_conn.setblocking(False)
                    self.inputs.append(new_conn)
                    id = self.add_client(new_conn)
                    log.info(f'подключился клиент {id} - {client_addr}')
                else:
                    data = conn.recv(1024)
                    if data:
                        data = decoder(data)
                        self.updater(self.messages, self.sock_id[conn], data)

                        if conn not in self.outputs: # даем готовность к приему
                            self.outputs.append(conn)

                    else:
                        self.del_client(conn)

            new_messages = self.message_refactor()

            if new_messages:
                for conn in send:
                    for data, li_recip in new_messages.items():
                        for id in li_recip:
                            if conn == self.id_sock[id]:
                                conn.send(encoder(data))  
                del new_messages  
            # else:
            #     self.outputs.remove(conn)

   
            for conn in excepts:
                self.del_client(conn, error=True)


           
        
if __name__ == '__main__':
    m = Main(sys.argv[1])
    m.run()