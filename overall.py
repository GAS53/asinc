import json

from property import PATH_LOGGING_CALL_FUNC

def decoder(it):
    it = it.decode('utf-8')
    it = json.loads(it)
    return dict(it)


def encoder(it):
    it = json.loads(it)
    it = it.encode('utf-8')
    return it



class Log:
    def __init__(self, in_put='terminal'):
        self.in_put = in_put
    
    def __call__(self, func):
        def wrapper(*args):
            if self.in_put == 'terminal':
                print(f'call func - {func.__name__} with arg {args} class {__class__.__name__}')
            elif self.in_put == 'file' :
                with open(PATH_LOGGING_CALL_FUNC, 'a') as file:
                    file.write(f'call func - {func.__name__} with arg {args} class {__class__.__name__}\n')
            else:
                raise TypeError('неверно задан параметр в функции Log должен быть "file" или "terminal"')

            res = func(*args)
            return res
        return wrapper