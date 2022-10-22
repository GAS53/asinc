import inspect

def f():
    print('test')


class Test_cl:
    def __repr__(self):
        return 'test'

    def test_error(self):
        frame = inspect.currentframe()
        print(frame.f_lineno, frame.f_trace)
        return 'error'

# for name, data in inspect.getmembers(Test_cl):
#     print(name, data)

t = Test_cl()
t.test_error()