import socket
from server_objects import check
from props import HOST, PORT


def main():
    SOC = socket.socket()

    SOC.bind((HOST, PORT))
    SOC.listen(5)

    while True:

        client, addr = SOC.accept()
        print(f'соединение с {addr}')
        res = client.recv(1024)
        it_send = check(res)
        if it_send:
            client.send(it_send)
        client.close()

if __name__=='__main__':
    main()