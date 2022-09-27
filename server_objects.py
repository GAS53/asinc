import json
from base_objects import Base_message

class Response(Base_message):
    def chose_message_type(self):
        return 'serv_response'

def check(it):
    it = it.decode('utf-8')
    # print(f'json decode {it}')
    j_di = json.loads(it)
    di = dict(j_di)
    if di['action'] == 'echo':
        return echo(di)

def echo(di):
    # print(f'echo func {di}')
    is_response = True
    res = f'сервер переслал сообщение: {di["message"]}'
    print(res)
    sr = Response()
    new_di = sr.run(res)
    

    

    return is_response, new_di

