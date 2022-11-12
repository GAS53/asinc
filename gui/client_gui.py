# import sys
# from PyQt6.QtWidgets import QApplication, QWidget, QRadioButton, QLabel, QVBoxLayout
# from PyQt6.QtCore import Qt


# class MainWindow(QWidget):
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)

#         self.setWindowTitle('Чат')
#         self.setMinimumWidth(300)

#         # create a grid layout
#         layout = QVBoxLayout()
#         self.setLayout(layout)

#         label = QLabel('Выберите действие', self)

#         rb_android = QRadioButton('Отправить сообщение', self)
#         rb_android.toggled.connect(self.update)

#         rb_ios = QRadioButton('сделать запрос', self)
#         rb_ios.toggled.connect(self.update)

#         rb_windows = QRadioButton('Windows', self)
#         rb_windows.toggled.connect(self.update)

#         self.result_label = QLabel('', self)

#         layout.addWidget(label)
#         layout.addWidget(rb_android)
#         layout.addWidget(rb_ios)
#         layout.addWidget(rb_windows)
#         layout.addWidget(self.result_label)

#         # show the window
#         self.show()

#     def update(self):
#         # get the radio button the send the signal
#         rb = self.sender()

#         # check if the radio button is checked
#         if rb.isChecked():
#             self.result_label.setText(f'You selected {rb.text()}')


# if __name__ == '__main__':
#     app = QApplication(sys.argv)
#     window = MainWindow()
#     sys.exit(app.exec())


from PyQt6 import QtWidgets, uic
import sys


app = QtWidgets.QApplication(sys.argv)
window = uic.loadUi('/home/gas53/Documents/asinc/gui/chat.ui')
window.btnQuit.clicked.connect(app.quit)
window.show()
sys.exit(app.exec_())