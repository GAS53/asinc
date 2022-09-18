'''1 Каждое из слов «разработка», «сокет», «декоратор» представить в строковом формате и
проверить тип и содержание соответствующих переменных. Затем с помощью
онлайн-конвертера преобразовать строковые представление в формат Unicode и также
проверить тип и содержимое переменных'''

from base64 import decode, encode


DEVELOP  = 'разработка'
SOCKET = 'сокет'
DECORATOR = 'декоратор'

def get_type(it):
    print(f'{it} type - {type(it)} len {len(it)}')



get_type(DEVELOP)     # разработка type - <class 'str'> 10
get_type(SOCKET)      # сокет type - <class 'str'> len 5
get_type(DECORATOR)   # декоратор type - <class 'str'> len 9

DEVELOP_U = '\u0440\u0430\u0437\u0440\u0430\u0431\u043e\u0442\u043a\u0430'
SOCKET_U = '\u0441\u043e\u043a\u0435\u0442'
DECORATOR_U = '\u0434\u0435\u043a\u043e\u0440\u0430\u0442\u043e\u0440'


get_type(DEVELOP_U)     # разработка type - <class 'str'> 10
get_type(SOCKET_U)      # сокет type - <class 'str'> len 5
get_type(DECORATOR_U)   # декоратор type - <class 'str'> len 9

'''2 Каждое из слов «class», «function», «method» записать в байтовом типе без преобразования в
последовательность кодов (не используя методы encode и decode) и определить тип,
содержимое и длину соответствующих переменных'''

CL = b'class' 
FU = b'function'
ME = b'method'


get_type(CL)  # b'class' type - <class 'bytes'> len 5
get_type(FU)  # b'function' type - <class 'bytes'> len 8
get_type(ME)  # b'method' type - <class 'bytes'> len 6


'''3. Определить, какие из слов «attribute», «класс», «функция», «type» невозможно записать в
байтовом типе'''

print(b'attribute')
# print(b'класс»')  # SyntaxError: bytes can only contain ASCII literal characters
# print(b'функция') # SyntaxError: bytes can only contain ASCII literal characters
print(b'type')


'''4. Преобразовать слова «разработка», «администрирование», «protocol», «standard» из
строкового представления в байтовое и выполнить обратное преобразование (используя
методы encode и decode).'''

ADMINISTRATION = 'администрирование'
PROTOCOL = 'protocol'
STANDARD = 'standard'



def to_byte_and_back(it):
    get_type(it)
    it = it.encode()
    get_type(it)
    it = it.decode()
    get_type(it)

to_byte_and_back(DEVELOP)
to_byte_and_back(PROTOCOL)
to_byte_and_back(STANDARD)

'''5 Выполнить пинг веб-ресурсов yandex.ru, youtube.com и преобразовать результаты из
байтовового в строковый тип на кириллице.'''

import requests

def get_ping(it):
    res = requests.get(it)  # <Response [200]>
    print(res.encoding)  # utf-8
    print(res.text) # <body></body><script nonce='0655570626aafa31d2 ...


get_ping('http://yandex.ru')
get_ping('http://www.youtube.com')  # есть кирилица ... {"accessibility":{"accessibilityData":{"label":"3,5 миллиона просмотров"}...


'''6. Создать текстовый файл test_file.txt, заполнить его тремя строками: «сетевое
программирование», «сокет», «декоратор». Проверить кодировку файла по умолчанию.
Принудительно открыть файл в формате Unicode и вывести его содержимое.'''

'''тип файла текстовый файл
откртие в кодировке utf-8 на прикрепленном скриншоте
вывод: ничего не поменялось т.к. по умолчанию для тектового файла кодировка utf-8'''