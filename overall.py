import json

from property import PATH_LOGGING_CALL_FUNC

def decoder(it):
    it = it.decode('utf-8')
    it = json.loads(it)
    return dict(it)


def encoder(it):
    it = json.dumps(it)
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




class Check_port:
    def __init__(self) -> None:
        self.port = 7777

    def __get__(self):
        print(f'run get Checkport')
        if self.port == None:
            return 7777
        else:
            return self.port

    def __set__(self, instance, value):
        print(f'run set Checkport')
        if 0 > value or not isinstance(value, int):
            raise ValueError("Порт должен быть целым числом больше 0")
        setattr(instance, self.port, value)
