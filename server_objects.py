import json
from base_objects import Standard_msg, Log, Ping, decoder
from props import term_or_file

IM = 'server'

@Log(term_or_file)
def check(di):
    di = decoder(di)

    if di['action'] == 'echo':
        sr = Standard_msg(IM)
        sr.send_to(di['from'])
        new_di = sr.run(msg=f'сервер переслал сообщение: {di["message"]}')
        return new_di

    elif di['action'] == 'ping':
        sr = Ping(IM)
        sr.send_to(di['from'])
        new_di = sr.run()
        return new_di

    elif di['action'] == 'user_user':
        sr = Standard_msg(IM)
        sr.send_to(di['from'])
        new_di = sr.run()
        return new_di

    elif di['action'] == 'all':
        sr = Standard_msg(IM)
        sr.send_to(di['action'])
        sr.from_not_server(di['from'])
        new_di = sr.run(msg=di["message"])
        return new_di

    

    


