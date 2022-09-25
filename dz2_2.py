'''Задание на закрепление знаний по модулю json. Есть файл orders в формате JSON с информацией о заказах. Написать скрипт, автоматизирующий его заполнение данными. Для этого:
Создать функцию write_order_to_json(), в которую передается 5 параметров — товар (item), количество (quantity), цена (price), покупатель (buyer), дата (date). Функция должна предусматривать запись данных в виде словаря в файл orders.json. При записи данных указать величину отступа в 4 пробельных символа;
Проверить работу программы через вызов функции write_order_to_json() с передачей в нее значений каждого параметра'''

import json
import uuid

file_path = '/home/gas53/Documents/dz/sources/orders.json'

def write_order_to_json(item, quantity, price, buyer, date):
    with open(file_path, "r") as file:
        di = json.load(file)
        di['orders'].append({'товар':item, 'количество':quantity, 'цена':price, 'покупатель':buyer, 'дата': date})

    with open(file_path, "w") as write_file:
        json.dump(di, write_file)


write_order_to_json('bread', '2', '25', 'men', '12.12.2012')




