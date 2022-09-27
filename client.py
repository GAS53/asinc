import socket

from client_objects import echo

SOC = socket.socket()
HOST = socket.gethostname()
PORT = 12345
IM = 'client_1'

SOC.connect((HOST, PORT))

msg = 'my message'

SOC.send(echo.run(msg))
print(SOC.recv(1024))
SOC.close()
