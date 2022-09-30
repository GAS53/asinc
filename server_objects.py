import json
from base_objects import Ok_response

class Response(Ok_response):
    def chose_message_type(self):
        return 'ping'

class Echo(Ok_response):
    def chose_message_type(self):
        return 'echo'

def check(it):
    
    it = it.decode('utf-8')
    j_di = json.loads(it)
    di = dict(j_di)
    if di['action'] == 'echo':
        sr = Echo()
        new_di = sr.run(msg=f'сервер переслал сообщение: {di["message"]}')
        return True, new_di
    elif di['action'] == 'ping':
        sr = Response()
        new_di = sr.run()
        return True, new_di


    

    


