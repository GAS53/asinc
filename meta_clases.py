import dis



class ServerVerifier(type):
    def __init__(self, cls, base, clsdict):
        methods = []
        attrs = []

        for func in clsdict:
            try:
                instructions = dis.get_instructions(clsdict[func])
            except TypeError:
                pass
            else:
                for instruction in instructions:
                    if instruction.opname == 'LOAD_METHOD':
                        if instruction.argrepr not in methods:
                            methods.append(instruction.argrepr)
                    elif instruction.opname == 'LOAD_GLOBAL':
                        if instruction.argrepr not in attrs:
                            attrs.append(instruction.argrepr)

        if 'connect' in methods:
            raise TypeError('В классе Server нельзя использовать метод connect!')
        if not ('SOCK_STREAM' in attrs and 'AF_INET' in attrs):
            raise TypeError('Инициализация сокета не соответствует TCP')



class ClientVerifier(type):
    def __init__(self, cls, base, clsdict):
        methods = []
        attrs = []

        for func in clsdict:
            try:
                instructions = dis.get_instructions(clsdict[func])
            except TypeError:
                pass
            else:
                for instruction in instructions:
                    if instruction.opname == 'LOAD_METHOD':
                        if instruction.argrepr not in methods:
                            methods.append(instruction.argrepr)
                    elif instruction.opname == 'LOAD_GLOBAL':
                        if instruction.argrepr not in attrs:
                            attrs.append(instruction.argrepr)

        if ['accept', 'listen'] in methods :
            raise TypeError('В классе Server нельзя использовать метод connect!')
        if not ('SOCK_STREAM' in attrs and 'AF_INET' in attrs):
            raise TypeError('Инициализация сокета не соответствует TCP')
