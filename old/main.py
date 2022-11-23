import subprocess

from property import PORT
from client_gui import run
from Server.server import Main as Server

count_clients = 3

'''sudo apt-get install gnome-terminal'''

if __name__ == '__main__':
    # print(f'port {PORT}')
    # sub_sr = subprocess.run(['gnome-terminal', "-x", "sh", "-c", f'python server.py {PORT}'], shell=False)
    # for _ in range(count_clients):
    #     subprocess.run(['gnome-terminal', "-x", "sh", "-c", f'python client.py {PORT}'], shell=False)
    s = Server()
    s.run()
    run()
