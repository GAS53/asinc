import socket

SOC = socket.socket()  # Создание сокета
'''s = socket(domain, type, protocol)
    domain - AF_INET (Internet протоколы)
    socket -
    SOCK_STREAM - Этот тип обеспечивает последовательный, надежный, ориентированный на установление двусторонней связи поток байтов
    SOCK_DGRAM - поддерживает двусторонний поток данных. Не гарантируется, что этот поток будет последовательным, надежным, и что данные не будут дублироваться. Важной характеристикой данного сокета является то, что границы записи данных предопределены.
    Raw socket - обеспечивает возможность пользовательского доступа к низлежащим коммуникационным протоколам, поддерживающим сокет-абстракции. Такие сокеты обычно являются датаграм- ориентированными.
     
    s = socket(AF_INET, SOCK_STREAM, 0) Для создания сокета типа stream с протоколом TCP, обеспечивающим коммуникационную поддержку, вызов функции socket должен быть следующим:   
    '''


HOST = socket.gethostname()
PORT = 12345

SOC.bind((HOST, PORT))  # Для связывания сокета с адресом и номером порта

SOC.listen(5)
'''error = listen(s, qlength)
    где s это дескриптор сокета, а qlength это максимальное количество запросов на установление связи, которые могут стоять в очереди, ожидая обработки сервером; это количество может быть ограничено особенностями системы'''

while True:
    client, addr = SOC.accept()
    # newsock = accept(s, clientaddr, clientaddrlen)
    # Сокет, ассоциированный клиентом, и сокет, который был возвращен функцией accept, используются для установления связи между сервером и клиентом
    data = client.recv(1024)
    res = data.decode('utf-8')
    
    print(f'Message {res}')
    resp = f'Эхо ответ - {res}'
    client.send(b'responce')
    client.close()