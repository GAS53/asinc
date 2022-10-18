import subprocess

from property import PORT

count_clients = 3

if __name__ == '__main__':
    print(f'port {PORT}')
    sub_sr = subprocess.run(['gnome-terminal', "-x", "sh", "-c", f'python server.py {PORT}'], shell=False)
    for _ in range(count_clients):
        subprocess.run(['gnome-terminal', "-x", "sh", "-c", f'python client.py {PORT}'], shell=False)
