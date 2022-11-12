from PyQt5.QtWidgets import QApplication
from PyQt5 import QtCore, QtGui, QtWidgets
import sys

class Ui_Dialog(object):
    def __init__(self):
        super().__init__()
        self.setupUi(QtWidgets)


    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(322, 289)
        self.radioButton = QtWidgets.QRadioButton(Dialog)
        self.radioButton.setGeometry(QtCore.QRect(20, 180, 171, 21))
        self.radioButton.setObjectName("radioButton")
        self.radioButton_2 = QtWidgets.QRadioButton(Dialog)
        self.radioButton_2.setGeometry(QtCore.QRect(20, 200, 171, 21))
        self.radioButton_2.setObjectName("radioButton_2")
        self.textEdit = QtWidgets.QTextEdit(Dialog)
        self.textEdit.setGeometry(QtCore.QRect(10, 10, 301, 161))
        self.textEdit.setObjectName("textEdit")
        self.check_chat_or_user = QtWidgets.QComboBox(Dialog)
        self.check_chat_or_user.setGeometry(QtCore.QRect(200, 180, 79, 23))
        self.check_chat_or_user.setObjectName("check_chat_or_user")
        self.type_request = QtWidgets.QComboBox(Dialog)
        self.type_request.setGeometry(QtCore.QRect(200, 200, 79, 23))
        self.type_request.setObjectName("type_request")
        self.lineEdit = QtWidgets.QLineEdit(Dialog)
        self.lineEdit.setGeometry(QtCore.QRect(20, 230, 271, 22))
        self.lineEdit.setText("")
        self.lineEdit.setObjectName("lineEdit")
        self.pushButton = QtWidgets.QPushButton(Dialog)
        self.pushButton.setGeometry(QtCore.QRect(10, 260, 291, 21))
        self.pushButton.setObjectName("pushButton")


        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)
        self.show()


    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "чат"))
        self.radioButton.setText(_translate("Dialog", "Отправить сообщение"))
        self.radioButton_2.setText(_translate("Dialog", "Сделать запрос"))
        self.pushButton.setText(_translate("Dialog", "Отправить"))


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Ui_Dialog()
    sys.exit(app.exec_())