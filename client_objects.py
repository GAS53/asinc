import json



def check(it):
    it = it.decode('utf-8')
    j_di = json.loads(it)
    di = dict(j_di)
    if di['action'] == 'echo':
        print(f'Ответ с сервера: {di["message"]} ') 
    elif di['action'] == 'ping':
        print(f'Cтатус проверки связи {di["status"]}')






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






