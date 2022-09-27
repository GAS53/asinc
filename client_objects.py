from base64 import decode
import datetime
import json
import sys
from abc import abstractclassmethod

MESSAGE_TYPE = {"echo":'echo_msg'}

# ok = { 
# "response": 200,
# "alert":"Необязательноесообщение/уведомление"
# }

# wrong_account = {
# "response": 402,
# "error": "wrong password or no account with that name"
# }

# alredy_connected = {
# "response": 409,
# "error": "Someone is already connected with the given user name"

# }

# close_connection = {
#     "action": "quit"
# }


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

# probe = {
#     "action": "probe",
# "time": datetime.datetime.now(),

# }

# def user_user(im, hi, msg):
#     di = {
#     "action": "msg",
#     "time": datetime.datetime.now()
#     "to": hi,
#     "from": im,
#     "encoding": "ascii",
#     "message": f"{msg}"
#     }
#     return di

# def user_chat(im, id_chat, msg):
#     di = {

#     "action": "msg",
#     "time": datetime.datetime.now()
#     "to": f'{id_chat}',
#     "from": f'{im}',
#     "message": f{msg}
#     }
#     return di

# def connect_chat(id_chat):
#     di = {
#         "action": "join",
# "time": datetime.datetime.now()
# "room": f'{id_chat}',

#     }
#     return di


class Base_message():
    def __init__(self):
        self.di = {}
        self.di['time'] = datetime.datetime.now().strftime('%c')
        self.di["action"] = self.chose_message_type()
        self.di['error'] = None
        self.di['im'] = sys.argv[0].split('/')[-1]

    @abstractclassmethod
    def chose_message_type(self):
        print('необходимо выбрать тип сообщения в chose_message_type')


    def run(self, msg):
        if msg:
            self.di['message'] = msg
        j_di = json.dumps(self.di)
        # print(j_di)
        return j_di

        


class echo(Base_message):

    def chose_message_type(self):
        return 'echo'



# us = User_server()
# us.run()
# print(datetime.datetime.now().strftime('%c'))    
    


# print(user_server('test'))
# print(sys.argv[0].split('/')[-1])