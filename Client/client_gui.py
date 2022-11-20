import sys
from threading import Lock, Thread
from queue import Queue
import socket
import logging.config
import hmac
import hashlib
import time

from PyQt6.QtWidgets import QInputDialog, QLabel, QApplication, QWidget, QLineEdit, QRadioButton, QTextEdit, QPushButton, QDialog, QComboBox
from PyQt6 import QtCore
import PyQt6.QtWidgets as Widgets

import client_prop
import net_func

logging.config.dictConfig(client_prop.client_log_config1)
log = logging.getLogger(f'client')



class MainWindow(QWidget):
    def __init__(self, port):
        super().__init__()
        self.init_socket(port)
        self.msg_for_send = Queue()
        self.msg_from_server = Queue()
        self.run_threads()

        self.setWindowTitle('Чат')
        self.resize(322, 320)



        self.textEdit = QLabel(self) #  QTextEdit(self)
        self.textEdit.setGeometry(QtCore.QRect(10, 10, 320, 161))
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
        # self.choice_user.addItems(get_my_frends())


        self.choice_chat = QComboBox(self)
        self.choice_chat.setGeometry(QtCore.QRect(200, 200, 100, 23))
        self.choice_chat.setObjectName("choice_chat")
        # self.choice_chat.addItems(get_my_chats())

        self.choice_request = QComboBox(self)
        self.choice_request.setGeometry(QtCore.QRect(200, 220, 100, 23))
        self.choice_request.setObjectName("choice_request")
        self.choice_request.addItems(net_func.get_requests(['ping', 'echo', 'get_chats',  'get_frends', 'add_chat', 'del_chat', 'im']))

   
        self.lineEdit = QLineEdit(self)
        self.lineEdit.setGeometry(QtCore.QRect(20, 250, 271, 22))
        self.lineEdit.setText("")


        self.button = Widgets.QPushButton('Отправить', self)
        self.button.setGeometry(QtCore.QRect(20, 280, 271, 22))
        self.button.setObjectName("pushButton")
        self.button.clicked.connect(self.clicked_send)

        # dlg = Widgets.QInputDialog()
        # dlg.getItem(self, 'title', 'prompt', , editable=False)
        # dlg.getText(self, 'Пароль', 'пароль')
        
        dlg_list = ['user1', 'user2', 'user3']
        self.im, _ = QInputDialog().getItem(self,'Выберите пользователя', 'Залогиниться под пользователем', dlg_list)
        pswd, _ = QInputDialog.getText(self, 'Пароль', 'пароль')
        tup_user = (self.im, pswd)

        hs_msg = net_func.Base_message('handshake', msg=tup_user)
        # self.msg_for_send.put(hs_msg())

        self.con_button = Widgets.QPushButton('Подключитсья', self)
        self.con_button.setGeometry(QtCore.QRect(20, 310, 271, 22))
        self.button.setObjectName("pushButton22")
        self.con_button.clicked.connect(self.con_click)



        self.show()

    def con_click(self):
        tup_user = 'test', 'best'
        hs_msg = net_func.Base_message('handshake', msg=tup_user)
        print(hs_msg())
        self.msg_for_send.put(hs_msg())





    
    def clicked_send(self):
        # print(f'{self.radioButton_1.isChecked()} {self.radioButton_2.isChecked()} {self.radioButton_3.isChecked()}')
        if not self.radioButton_1.isChecked() and not self.radioButton_2.isChecked() and not self.radioButton_3.isChecked():
            self.textEdit.setText('не выбрано сообщение/запрос')
        else:
            if self.radioButton_1.isChecked():  # сообщение пользователю
                self.textEdit.setText('пользователь')

            elif self.radioButton_2.isChecked():  # сообщение в чат
                self.textEdit.setText('чат')

            elif self.radioButton_3.isChecked():  # запрос
                if client_prop.MY_NONE == self.choice_request.currentText():
                    self.textEdit.setText('не выбран тип запроса')
                    

                elif 'ping' == self.choice_request.currentText():
                    msg = net_func.Base_message('ping')
                  

                elif 'echo' == self.choice_request.currentText():
                    
                    line = self.lineEdit.text()
                    line = line if line else 'пустой эхо запрос'
                    msg = net_func.Base_message('echo', msg=line)


                elif 'get_contacts' == self.choice_request.currentText():
                    msg = net_func.Base_message('get_contacts')

                            
                else:
                    command = self.choice_request.currentText()
                    line = self.lineEdit.text()
                    msg = net_func.Base_message(command, msg=line)

                self.textEdit.setText(f'отправлен запрос {self.choice_request.currentText()}')
                log.info(f'отправлено сообщение {msg()}')
                self.msg_for_send.put(msg())


    def run_threads(self):
        log.info('инициализация бекэнда')

        # time.sleep(1)
        data = self.SOC.recv(1024)
        hash = hmac.new(client_prop.AUTH_KEY, data, hashlib.sha256) # 
        digest = hash.digest()
        self.SOC.send(digest)


        time.sleep(1)
        th_get = Thread(target=self.send_msg)
        th_get.start()
        log.info('Запущен получающий клиент')
        # time.sleep(0.5)

        th_term = Thread(target=self.get_msg)
        th_term.start()
        log.info('Запущен отправляющий клиент')

    def send_msg(self):
        while True:
            mess = self.msg_for_send.get()
            print(f'mess {mess}')
            self.SOC.send(net_func.encoder(mess))

    def get_msg(self):
        while True:
            data = self.SOC.recv(1024)
            data = net_func.decoder(data)
            log.info(f'от сервера получено сообщение {data["message"]}' if data.get('message') else f'статус {data["status"]}')
            self.msg_from_server.put(data)


    def init_socket(self, port):
        self.SOC = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.SOC.connect((socket.gethostname(), port))
        log.info(f'инициализирован клиент')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    M = MainWindow(12595)
    sys.exit(app.exec())