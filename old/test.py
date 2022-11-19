import json
import unittest
import json



import base_objects
import server



class MyTest(unittest.TestCase):
    def setUp(self):
        default_cl = base_objects.Ping()

        self.byte_di = default_cl.run()
        str_di = self.byte_di.decode('utf-8')
        self.di = json.loads(str_di)



    def test_client_return_byte(self):
        self.assertIsInstance(self.byte_di, bytes)

    def test_client_return_dict(self):
        self.assertIsInstance(self.di, dict)

    def test_client_ping(self):
        self.assertEqual(self.di['action'], 'ping')

    def test_ok_200(self):
        self.assertEqual(self.di['status'], '200')

    def test_connection(self):
        serv = server.main()




    # def tearDown(self):
    #     ...


if __name__ == '__main__':
    unittest.main()