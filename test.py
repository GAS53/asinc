import json
import string
import unittest
import os
import json
import datetime

import client_objects
import client_1
import server



class MyTest(unittest.TestCase):
    def setUp(self):
        default_cl = client_objects.ping_server()
        self.byte_di = default_cl.run()
        str_di = self.byte_di.decode('utf-8')
        self.di = json.loads(str_di)
        # res_date = datetime.datetime.strftime(self.di['time'])
        # print(self.di['time'])


    def test_client_return_byte(self):
        self.assertIsInstance(self.byte_di, bytes)

    def test_client_return_dict(self):
        self.assertIsInstance(self.di, dict)

    def test_client_ping(self):
        self.assertEqual(self.di['action'], 'ping')

    def test_ok_200(self):
        self.assertEqual(self.di['status'], '200')

    # def test_client_return_dict(self):
    #     res_date = datetime.datetime.strftime(self.di['time'])
    #     print(res_date)
    #     self.assertIsInstance(res_date, datetime.datetime)


    # def tearDown(self):
    #     ...


if __name__ == '__main__':
    unittest.main()