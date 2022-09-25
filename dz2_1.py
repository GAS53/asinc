
import os
import re
import csv

cwd = os.getcwd()
source_path = f'{cwd}/sources'
main_res_path = f'{cwd}/main_data.txt'
csv_res_path = f'{cwd}/main_data.csv'



def get_list(file_data, str_name):
    li = []
    for line in file_data:
        prod = re.match(f'{str_name}', line)
        if prod:
            res = line.split(':')[1].strip()
            li.append(res)
    return li




def make_main_li(a,b,c,d):
    li = []
    for i in range(len(a)):
        li.append([a[i], b[i], c[i], d[i]])
    return li


def get_data(end):
    os_prod_list = []
    os_name_list = []
    os_code_list = []
    os_type_list = []
    

    
    files = os.listdir(source_path)
    for file in files:
        if file.endswith(end):
            full_path = f'{source_path}/{file}'
            print(full_path)
            with open(full_path, 'r') as file:
                file_data = file.readlines()
                os_prod_list.extend(get_list(file_data, 'Изготовитель системы:'))
                os_name_list.extend(get_list(file_data, 'Название ОС:'))
                os_code_list.extend(get_list(file_data, 'Код продукта:'))
                os_type_list.extend(get_list(file_data, 'Тип системы:'))

    return make_main_li(os_prod_list, os_name_list, os_code_list, os_type_list)


def write_to_csv():
    res = get_data('.txt')
    print(res)

    with open(csv_res_path, 'w') as f_n:
        f_n_writer = csv.writer(f_n, quoting=csv.QUOTE_NONNUMERIC)
        f_n_writer.writerows(res)




write_to_csv()