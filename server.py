import socket
from server_objects import check
from props import HOST, PORT


def main():
    SOC = socket.socket()  # Создание сокета

    SOC.bind((HOST, PORT))  # Для связывания сокета с адресом и номером порта

    SOC.listen(5)
    '''error = listen(s, qlength)
        где s это дескриптор сокета, а qlength это максимальное количество запросов на установление связи, которые могут стоять в очереди, ожидая обработки сервером; это количество может быть ограничено особенностями системы'''

    while True:

        client, addr = SOC.accept()
        print(f'соединение с {addr}')
        res = client.recv(1024)
        is_send, it_send = check(res)
        if is_send:
            client.send(it_send)
        client.close()

if __name__=='__main__':
    main()