import sys
from PyQt5 import QtWidgets

class MyWindow(QtWidgets.QWidget):
    def __init__(self, parent=None):
        QtWidgets.QWidget.__init__(self, parent)
        self.ui = py_form.Ui_TestForm()
        self.ui.setupUi(self)
        self.ui.btnQuit.clicked.connect(QtWidgets.qApp.quit)

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = MyWindow()
    window.show()
    sys.exit(app.exec_())