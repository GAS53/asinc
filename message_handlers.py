from overall import decoder
import message_type

IM = 'server'


def check(di):
    di = decoder(di)

    if di['action'] == 'echo':
        sr = message_type.Standard_msg(IM)
        sr.send_to(di['from'])
        new_di = sr.run(msg=f'сервер переслал сообщение: {di["message"]}')
        return new_di

    elif di['action'] == 'ping':
        sr = message_type.Ping(IM)
        sr.send_to(di['from'])
        new_di = sr.run()
        return new_di

    elif di['action'] == 'user_user':# user_uid....
        sr = message_type.Standard_msg(IM)
        sr.send_to(di['from'])
        new_di = sr.run()
        return new_di

    elif di['action'] == 'all':
        sr = message_type.Standard_msg(IM)
        sr.send_to(di['action'])
        sr.from_not_server(di['from'])
        new_di = sr.run(msg=di["message"])
        return new_di
