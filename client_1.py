import socket
import sys
from unicodedata import name

from client_objects import echo, ping_server, check
from props import HOST, PORT


def main():

    SOC = socket.socket()


    SOC.connect((HOST, PORT))

    if len(sys.argv) == 1:
        # print('ping server')
        ping_cl = ping_server()
        # print(ping_cl.run())
        SOC.send(ping_cl.run())

    elif sys.argv[1]:
        msg = sys.argv[1]
        # print(f'echo server {msg}')
        
        echo_cl = echo()
        # print(echo_cl.run(msg))
        SOC.send(echo_cl.run(msg))
        
        



    recv = SOC.recv(1024)
    check(recv)
    SOC.close()

if __name__=='__main__':
    main()
