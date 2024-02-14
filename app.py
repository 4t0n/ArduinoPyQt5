from PyQt5 import QtWidgets, QtGui
from forArduino import Ui_MainWindow  # импорт нашего сгенерированного файла
from modules import SerialPort
import sys
#  Конвертация .ui to .py pyuic5 forArduino.ui -o forArduino.py


class MyWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(MyWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ser = SerialPort(self.ui)
        self.ui.openSerial.clicked.connect(self.ser.open_serial)
        self.ui.closeSerial.clicked.connect(self.ser.close_serial)
        self.ui.checkLed.stateChanged.connect(self.ser.check_connect)


app = QtWidgets.QApplication([])
application = MyWindow()
application.show()
sys.exit(app.exec())
