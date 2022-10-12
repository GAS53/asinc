

from email import message
import select
import socket
import logging
import logging.config
from queue import Queue
from random import choices
import sys
from uuid import uuid1
from xml.etree.ElementPath import prepare_parent

from property import PORT, HOST, client_log_config
from overall import decoder, encoder




logging.config.dictConfig(client_log_config)
log = logging.getLogger(f'server')


class Main():
    def __init__(self, port):
        self.port = int(port)
        self.inputs = []
        self.sock = self.innit_server()
        self.outputs = []
        self.messages = {}
        self.id_sock = {}
        self.sock_id ={}
        print(f'innit self.id_sock {self.id_sock}')

    def innit_server(self):
        server = socket.socket()  #socket.AF_INET, socket.SOCK_STREAM)
        server.bind((HOST, self.port))
        server.listen(5)
        server.setblocking(False)
        self.inputs.append(server)
        log.info(f'инициализирован сервер')
        return server

    def updater(self, mess, key, val):
        if mess.get(key, None):
            mess[key].append(val) 
        else:
            mess[key] = [val]
        return mess

    def generate_id(self):
        while True:
            id =''.join(choices([str(i) for i in range(9) ], k=3))
            # id = str(uuid1())
            if id not in self.id_sock.keys():
                return id


    def add_client(self, sock):
        id = self.generate_id()
        self.sock_id[sock] = id
        self.id_sock[id] = sock
        return id

    def del_client(self, conn, error=None):
        print(f'del conn {conn}')
        if conn in self.outputs:
            self.outputs.remove(conn)
        self.inputs.remove(conn)
        conn.close()
        del self.messages[conn]
        id = None
        id = self.sock_id.get(conn)
        del self.sock_id[conn]
        del self.id_sock[id]
        print(f'del conn {conn}')
        if error:
            log.info(f'клиент {id} отключился с ошибкой')
        else:
            log.info(f'клиент {id} отключился')

    def message_router(self):
        new_messages = []
        print(f'self.id_sock {self.id_sock}')
        for id, dataset in self.messages.items():
            
            for data in dataset:
                
                print(f'id {id}')
                if data['action'] == 'ping' or data['action'] == 'echo':
                    print('ping or echo')
                    data = self.updater(data, 'to', id)

                elif data['action'] == 'all':
                    print(f'user - all')
                    # print(f'keys {self.id_sock}')
                    # print(f'data {data}')
                    for to_id in self.id_sock.keys():
                        data = self.updater(data, 'to', to_id)

                elif "user_" in  data['action']:
                    to_id = data['action'].replace("user_", "")
                    data = self.updater(data, 'to', to_id)

                data['from'] = id   
                new_messages.append(data)
        self.messages.clear()
        return new_messages



    def run(self):
        test = 1
        while self.inputs:
            print(test)
            test += 1
            new_messages = None
            reads, send, excepts = select.select(self.inputs, self.outputs, self.inputs)
            print(f'before 3x3 {len(reads)} {len(send)} {len(excepts)} --- {len(self.inputs)} {len(self.outputs)} {len(self.inputs)}\n')
            
            for conn in reads:
                if conn == self.sock:  # если это сокет, принимаем подключение
                    new_conn, client_addr = conn.accept()
                    new_conn.setblocking(False)
                    id = self.add_client(new_conn)
                    # print(f'innit_server self.id_sock {self.id_sock}')
                    self.inputs.append(new_conn)
                    log.info(f'подключился новый клиент {id} - {client_addr}')
                else:
                    data = conn.recv(1024)
                    if data:
                        
                        data = decoder(data)
                        # print(f'data {data}')
                        self.updater(self.messages, self.sock_id[conn], data)
                        # print(f'self.messages {self.messages}')
                        if conn not in self.outputs: # даем готовность к приему
                            self.outputs.append(conn)
                            # print(f'append outputs {self.outputs}')

                        new_messages = self.message_router()
                        
                        print(f'self.messages CLEAR {self.messages}')
                    else:
                        print(f'клиент отключился')
                        self.del_client(conn)

            # print(f'self id_sock {self.id_sock}')

            if new_messages:
                for message in new_messages:
                    print(f'new_messages {new_messages}')
                    send_to = message['to']
                    for id_recipient in send_to:
                        print(f'id to send {id_recipient}')
                        recip_sock = self.id_sock[id_recipient]
                        print(f'recip sock {recip_sock}')
                        recip_sock.sendall(encoder(message))
                    # print(f'new_messages {new_messages}')
                    
                    # for recip, li_data in new_messages.items():
                    #     for data in li_data:
                    #         send_sock = self.id_sock[recip]
                    #         send_sock.send(encoder(data))  
                    #         print(f'send id - {recip}') # message {data}')
                    del new_messages  
            elif conn in self.outputs:  # remove  ???????????
                self.outputs.remove(conn)

   
            for conn in excepts:
                self.del_client(conn, error=True)
            # print(f'after 3x3 {len(reads)} {len(send)} {len(excepts)} --- {len(self.inputs)} {len(self.outputs)} {len(self.inputs)}\n')


           
        
if __name__ == '__main__':
    m = Main(sys.argv[1])
    m.run()