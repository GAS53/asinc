import subprocess

from server import Main as Server
from client import Main as Client
from property import PORT

p_list = []
count = 2

# Server(PORT)
server_command = [f'python /home/gas53/Documents/asinc/server.py {PORT}']
subprocess.call(server_command)




for _ in range(count):
    client_command = [f'python /home/gas53/Documents/asinc/client.py {PORT}']
    subprocess.call(client_command)
    # p_list.append(subprocess.run('python /home/gas53/Documents/asinc/client.py', shell=True))
    Client(PORT)
    

