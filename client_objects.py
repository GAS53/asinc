from base_objects import Base_message
import json

def check(it):
    it = it.decode('utf-8')
    # print(f'json decode {it}')
    j_di = json.loads(it)
    di = dict(j_di)
    if di['action'] == 'serv_response':
        print(f'Ответ с сервера: {di["message"]} ')  # di {di}


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




        


class echo(Base_message):

    def chose_message_type(self):
        return 'echo'



