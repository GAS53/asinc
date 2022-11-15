import sys
from PyQt6.QtWidgets import QLabel, QApplication, QWidget, QLineEdit, QRadioButton, QTextEdit, QPushButton, QDialog, QComboBox
from PyQt6 import QtCore
import socket
from socket import AF_INET, SOCK_STREAM
import logging.config
from threading import Lock, Thread
from queue import Queue
# from pathlib import Path
# BASE_DIR = Path(__file__).resolve().parent.parent
# import sys
# sys.path.append(BASE_DIR)
# i


from db_func import get_my_frends, get_requests, get_my_chats
from message_type import Ok_response
from property import client_log_config
from overall import decoder, Check_port
from property import HOST, MY_NONE, PORT


class MainWindow(QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.setWindowTitle('Чат')
        self.resize(322, 320)


        self.textEdit = QLabel(self) #  QTextEdit(self)
        self.textEdit.setGeometry(QtCore.QRect(10, 10, 301, 161))
        self.textEdit.setObjectName("textEdit")
        self.textEdit.setStyleSheet("border: 3px solid grey;")




        self.radioButton_1 = QRadioButton('написать пользователю', self)
        self.radioButton_1.setGeometry(QtCore.QRect(20, 180, 191, 21))
                

        self.radioButton_2 = QRadioButton('написать в чат', self)
        self.radioButton_2.setGeometry(QtCore.QRect(20, 200, 191, 21))


        self.radioButton_3 = QRadioButton('сделать запрос', self)
        self.radioButton_3.setGeometry(QtCore.QRect(20, 220, 191, 21))
                

        self.choice_user = QComboBox(self)
        self.choice_user.setGeometry(QtCore.QRect(200, 180, 100, 23))
        self.choice_user.setObjectName("choice_user")
        self.choice_user.addItems(get_my_frends())


        self.choice_chat = QComboBox(self)
        self.choice_chat.setGeometry(QtCore.QRect(200, 200, 100, 23))
        self.choice_chat.setObjectName("choice_chat")
        self.choice_chat.addItems(get_my_chats())

        self.choice_request = QComboBox(self)
        self.choice_request.setGeometry(QtCore.QRect(200, 220, 100, 23))
        self.choice_request.setObjectName("choice_request")
        self.choice_request.addItems(get_requests(['ping', 'echo', 'get_contacts', 'add_chat', 'del_chat']))

   
        self.lineEdit = QLineEdit(self)
        self.lineEdit.setGeometry(QtCore.QRect(20, 250, 271, 22))
        self.lineEdit.setText("")


        self.button = QPushButton('Отправить', self)
        self.button.setGeometry(QtCore.QRect(20, 280, 271, 22))
        self.button.setObjectName("pushButton")
        self.button.clicked.connect(self.clicked)
            

        self.show()

        self.innit_logger()
        self.term_lock = Lock()
        self.send_queue = Queue()
        self.init_socket()


    def clicked(self):
        # print(f'{self.radioButton_1.isChecked()} {self.radioButton_2.isChecked()} {self.radioButton_3.isChecked()}')
        if not self.radioButton_1.isChecked() and not self.radioButton_2.isChecked() and not self.radioButton_3.isChecked():
            self.textEdit.setText('не выбрано сообщение/запрос')
        else:
            if self.radioButton_1.isChecked():  # сообщение пользователю
                self.textEdit.setText('пользователь')

            elif self.radioButton_2.isChecked():  # сообщение в чат
                self.textEdit.setText('чат')

            elif self.radioButton_3.isChecked():  # запрос
                if MY_NONE == self.choice_request.currentText():
                    self.textEdit.setText('не выбран тип запроса')
                    

                elif 'ping' == self.choice_request.currentText():
                    bm = Ok_response('ping')
                    msg = bm.run()

                elif 'echo' == self.choice_request.currentText():
                    bm = Ok_response('echo')
                    line = self.lineEdit.text()
                    line = line if line else 'пустой эхо запрос'
                    msg = bm.run(msg=line)

                elif 'get_contacts' == self.choice_request.currentText():
                    bm = Ok_response('get_contacts')
                    msg = bm.run()
                            
                else:
                    command = self.choice_request.currentText()
                    bm = Ok_response(command)
                    line = self.lineEdit.text()
                    msg = bm.run(msg=line)
                self.textEdit.setText(f'отправлен запрос {self.choice_request.currentText()}')
                self.send_queue.put(msg)


                       

    def innit_logger(self):
        logging.config.dictConfig(client_log_config)
        self.log = logging.getLogger(f'client')


    def init_socket(self):
        Cp = Check_port(PORT)
        self.SOC = socket.socket(AF_INET, SOCK_STREAM)
        self.SOC.connect((HOST, PORT))

    def run(self):
        th_get = Thread(target=self.get_msg)
        th_get.start()
        self.log.info('Запущен получающий клиент')
 

        th_send = Thread(target=self.send_msg)
        th_send.start()
        self.log.info('Запущен отправляющий клиент')

        

        





    def get_msg(self):
        while True:
            data = self.SOC.recv(1024)
            # with self.term_lock:
            data = decoder(data)
            res = f'сообщение: {data["message"]}' if data.get('message') else f'статус: {data["status"]}'
            self.textEdit.setText(f'{res}')

    def send_msg(self):
        while True:
            mess = self.send_queue.get()
            self.SOC.send(mess)






if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.run()

    sys.exit(app.exec())


