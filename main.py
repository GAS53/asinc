from random import choice
import subprocess

from Server import server
# from Client import client



PORT = choice([x for x in range(12000, 19000)])

if __name__ == '__main__':
    # serv = subprocess.Popen(server,shell=True,args=(PORT,))
    server(PORT)
    # client(PORT)

