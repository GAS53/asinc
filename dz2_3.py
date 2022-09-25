'''3. Задание на закрепление знаний по модулю yaml. Написать скрипт, автоматизирующий сохранение данных в файле YAML-формата. Для этого:
Подготовить данные для записи в виде словаря, в котором первому ключу соответствует список, второму — целое число, третьему — вложенный словарь, где значение каждого ключа — это целое число с юникод-символом, отсутствующим в кодировке ASCII (например, €);
Реализовать сохранение данных в файл формата YAML — например, в файл file.yaml. При этом обеспечить стилизацию файла с помощью параметра default_flow_style, а также установить возможность работы с юникодом: allow_unicode = True;
Реализовать считывание данных из созданного файла и проверить, совпадают ли они с исходными.'''


import yaml
from yaml import Loader

file_path = '/home/gas53/Documents/dz/sources/file.yaml'

def func():
    di = {}
    di['li'] = []
    di['int'] = 0
    inner_di = {}
    inner_di[1] = '€'
    di['di'] = inner_di
    print(di)
    with open(file_path, 'w') as file:
        yaml.dump(di ,file, default_flow_style=False, allow_unicode=True)

    with open(file_path, 'r') as file:
        res = file.read()
        print(res)
func()