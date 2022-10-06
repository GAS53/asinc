import json
from base_objects import Standard_msg, Log
from props import term_or_file

IM = 'server'

@Log(term_or_file)
def check(it):
    it = it.decode('utf-8')
    j_di = json.loads(it)
    di = dict(j_di)

    if di['action'] == 'echo':
        sr = Standard_msg(IM)
        sr.send_to(di['from'])
        new_di = sr.run(msg=f'сервер переслал сообщение: {di["message"]}')
        return new_di

    elif di['action'] == 'ping':
        sr = Standard_msg(IM)
        sr.send_to(di['from'])
        new_di = sr.run()
        return new_di

    elif di['action'] == 'user_user':
        
        sr = Standard_msg(IM)
        sr.send_to(di['from'])
        new_di = sr.run()
        return new_di


    

    


