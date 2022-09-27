import socket
import sys

from client_objects import echo, check
from props import HOST, PORT


SOC = socket.socket()


SOC.connect((HOST, PORT))

if not sys.argv[1] == None:
    msg = sys.argv[1]
else:
    msg = 'my message'


echo_cl = echo()

SOC.send(echo_cl.run(msg))
recv = SOC.recv(1024)
check(recv)
SOC.close()
