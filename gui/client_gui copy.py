import sys
from PyQt6.QtWidgets import QApplication, QWidget, QRadioButton, QTextEdit, QDialog, QComboBox
from PyQt6 import QtCore


class MainWindow(QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.setWindowTitle('Чат')
        self.resize(322, 320)
        self.radioButton = QRadioButton(self)
        self.radioButton.setGeometry(QtCore.QRect(20, 180, 171, 21))
        self.radioButton.setObjectName("is_message")

        self.radioButton_2 = QRadioButton(self)
        self.radioButton_2.setGeometry(QtCore.QRect(20, 200, 171, 21))
        self.radioButton_2.setObjectName("is_request")


        self.textEdit = QTextEdit(self) #  QTextEdit(self)
        self.textEdit.setGeometry(QtCore.QRect(10, 10, 301, 161))
        self.textEdit.setObjectName("textEdit")

        self.chat_or_user = QComboBox(self)
        self.chat_or_user.setGeometry(QtCore.QRect(200, 180, 79, 23))
        self.chat_or_user.setObjectName("choice_chat_or_user")

        self.choice_request = QComboBox(self)
        self.choice_request.setGeometry(QtCore.QRect(200, 200, 79, 23))
        self.choice_request.setObjectName("choice_request")


        # # create a grid layout
        # layout = QVBoxLayout()
        # self.setLayout(layout)

        # label = QLabel('Выберите действие', self)

        # rb_android = QRadioButton('Отправить сообщение', self)
        # rb_android.toggled.connect(self.update)

        # rb_ios = QRadioButton('сделать запрос', self)
        # rb_ios.toggled.connect(self.update)

        # rb_windows = QRadioButton('Windows', self)
        # rb_windows.toggled.connect(self.update)

        # self.result_label = QLabel('', self)

        # layout.addWidget(label)
        # layout.addWidget(rb_android)
        # layout.addWidget(rb_ios)
        # layout.addWidget(rb_windows)
        # layout.addWidget(self.result_label)

        # show the window
        self.show()

    def update(self):
        # get the radio button the send the signal
        rb = self.sender()

        # check if the radio button is checked
        if rb.isChecked():
            self.result_label.setText(f'You selected {rb.text()}')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec())


