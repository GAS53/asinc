import subprocess

from Server.server import Main as Server
from client import Main as Client
from property import PORT
import os

p_list = []
count = 2

os.system("gnome-terminal -e 'bash -c \"/home/gas53/.pyenv/versions/3.10.3/bin/python /home/gas53/Documents/asinc/server.py {PORT}; exec bash\"'")



# for _ in range(count):
#     client_command = [f'python /home/gas53/Documents/asinc/client.py {PORT}']
#     subprocess.call(client_command)
#     # p_list.append(subprocess.run('python /home/gas53/Documents/asinc/client.py', shell=True))
#     Client(PORT)
    

