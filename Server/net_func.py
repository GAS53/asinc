import json
import datetime

from Crypto.Cipher import AES

from server_prop import AUTH_KEY


def decoder(it):
    try:
        it = cript(it, encoding=False)
        print(f'befor json {it}')
        it = json.loads(it)
        print(f'befor cript {it}')
        return dict(it)
    except ValueError:
        return False


def encoder(it):
    it = json.dumps(it)
    print(f'after json {it}')
    
    print(f'after cript {it}')
    it = it.encode('utf-8')

    it = cript(it, encoding=True)
    return it

def padding(it):
    print(f'it {it}')
    count_space = (16 - len(it) % 16) % 16
    res = it + b' '*count_space

    print(f'res {res}')
    return res

count_cript = 0

def cript(it, encoding=True):
    global count_cript
    count_cript +=1
    print(f'count_cript {count_cript}')
    key = padding(AUTH_KEY)
    it = padding(it)


    if encoding:
        
        
        cipher = AES.new(key, AES.MODE_CBC)
        it = cipher.iv + cipher.encrypt(it)
    else:

        cipher = AES.new(key, AES.MODE_CBC, iv=it[:16])
        it = cipher.decrypt(it[16:])

    return it