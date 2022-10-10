import json
import logging
from props import term_or_file
from base_objects import Log, decoder

@Log(term_or_file)
def check(di):
    di = decoder(di)
    if di['action'] == 'msg':
        
        logging.info(f'Ответ с сервера: {di["message"]} ') 
    elif di['action'] == 'ping':
        logging.info(f'Cтатус проверки связи {di["status"]}')
    # elif di['action'] == 'msg':
    #     logging.info(f'Ответ с сервера: {di["message"]}') 






# autentification = {
# "action": "authenticate",
# "time": datetime.datetime.now()
# "user": {
# "account_name": "C0deMaver1ck",
# "password": "CorrectHorseBatteryStaple"
# }
# }

# input_user = {
    
# "action": "presence",
# "time": datetime.datetime.now()
# "type": "status",
# "user": {
# "account_name": "C0deMaver1ck",
# "status": "Yep, I am here!"
# }

# }





# def user_chat(im, id_chat, msg):
#     di = {

#     "action": "msg",
#     "time": datetime.datetime.now()
#     "to": f'{id_chat}',
#     "from": f'{im}',
#     "message": f{msg}
#     }
#     return di






