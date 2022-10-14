import select
import socket
import logging
import logging.config
# from queue import Queue
from random import choices
import sys
from uuid import uuid1


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

        if conn in self.outputs:
            self.outputs.remove(conn)
        self.inputs.remove(conn)
        conn.close()
        del self.messages[conn]
        id = None
        id = self.sock_id.get(conn)
        del self.sock_id[conn]
        del self.id_sock[id]

        if error:
            log.info(f'клиент {id} отключился с ошибкой')
        else:
            log.info(f'клиент {id} отключился')

    def message_router(self):
        new_messages = []
        for id, dataset in self.messages.items():
            
            for data in dataset:
                if data['action'] == 'ping' or data['action'] == 'echo':
                    data = self.updater(data, 'to', id)

                elif data['action'] == 'all':
                    for to_id in self.id_sock.keys():
                        data = self.updater(data, 'to', to_id)

                elif data['action'] == 'user':
                    data['to'] = [data['to']]

                
                elif data['action'] == "who":
                    users = list(self.id_sock.keys())
                    data = self.updater(data, 'to', id)
                    data['message'] = users

                data['from'] = id   
                new_messages.append(data)
        self.messages.clear()
        return new_messages



    def run(self):
        try:
            self.select_run()
        finally:
            self.sock.close()

    def select_run(self):
        while self.inputs:
            new_messages = None
            reads, send, excepts = select.select(self.inputs, self.outputs, self.inputs)
            # print(f'before 3x3 {len(reads)} {len(send)} {len(excepts)} --- {len(self.inputs)} {len(self.outputs)} {len(self.inputs)}\n')
            
            for conn in reads:
                if conn == self.sock:  # если это сокет, принимаем подключение
                    new_conn, client_addr = conn.accept()
                    new_conn.setblocking(False)
                    id = self.add_client(new_conn)
                    self.inputs.append(new_conn)
                    log.info(f'подключился новый клиент {id} - {client_addr}')
                else:
                    data = conn.recv(1024)
                    if data:
                        data = decoder(data)
                        self.updater(self.messages, self.sock_id[conn], data)
                        if conn not in self.outputs: # даем готовность к приему
                            self.outputs.append(conn)

                        new_messages = self.message_router()
                        
                    else:
                        self.del_client(conn)



            if new_messages:
                for message in new_messages:
                    res = f'сообщение {message["message"]} от {message["from"]} к {message["to"]}' if message.get('message') else f'статус {message["status"]}'
                    log.info(res)
                    send_to = message['to']
                    print(f' send to in new_messages {send_to}')
                    for id_recipient in send_to:
                        recip_sock = self.id_sock[id_recipient]
                        recip_sock.sendall(encoder(message))
 
                    del new_messages  
            elif conn in self.outputs:  # remove  ???????????
                self.outputs.remove(conn)

   
            for conn in excepts:
                self.del_client(conn, error=True)


           
        
if __name__ == '__main__':
    m = Main(sys.argv[1])
    m.run()