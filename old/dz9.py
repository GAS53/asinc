'''Написать функцию host_ping(), в которой с помощью утилиты ping будет проверяться
доступность сетевых узлов. Аргументом функции является список, в котором каждый сетевой
узел должен быть представлен именем хоста или ip-адресом. В функции необходимо
перебирать ip-адреса и проверять их доступность с выводом соответствующего сообщения
(«Узел доступен», «Узел недоступен»). При этом ip-адрес сетевого узла должен создаваться с
помощью функции ip_address().'''

import subprocess
import ipaddress
import tabulate

def check_ip(res, ip):
    if res:
        print(f'Узел {ip} не доступен')
        return False, ip
    else:
        print(f'Узел {ip} доступен')
        return True, ip

    

def ip_address(band):
    start = '192.168.1.1'
    ipz = ipaddress.ip_address(start)
    ips = []
    for i in range(band):
        ips.append(str(ipz + i))
    return ips



def host_ping(li):
    di = {}
    di[True] = []
    di[False] = []
    for ip in li:
        res = subprocess.call(['ping', "-c", "1", ip], stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
        is_true, ip = check_ip(res, ip)
        di[is_true].append(ip)
    return di


ips = ip_address(5)
host_ping(ips)

''' Написать функцию host_range_ping() для перебора ip-адресов из заданного диапазона.
Меняться должен только последний октет каждого адреса. По результатам проверки должно
выводиться соответствующее сообщение.'''

def host_range_ping():
    subnet = ipaddress.ip_network('80.0.1.0/28')
    ips = [str(ip) for ip in list(subnet.hosts())]
    di = host_ping(ips)
    return di

print('*'*10)
host_range_ping()




'''Написать функцию host_range_ping_tab(), возможности которой основаны на функции из
примера 2. Но в данном случае результат должен быть итоговым по всем ip-адресам,
представленным в табличном формате (использовать модуль tabulate). Таблица должна
состоять из двух колонок и выглядеть примерно так:'''

def host_range_ping_tab():
    # di = host_range_ping()
    di = {True: ['80.0.1.1'], False: ['80.0.1.2', '80.0.1.3', '80.0.1.4', '80.0.1.5', '80.0.1.6', '80.0.1.7', '80.0.1.8', '80.0.1.9', '80.0.1.10', '80.0.1.11', '80.0.1.12', '80.0.1.13', '80.0.1.14']}
    print(tabulate.tabulate(di, headers= ['Reachable', 'Unreachable'], tablefmt="grid", stralign="center"))

print('*'*10)
host_range_ping_tab()