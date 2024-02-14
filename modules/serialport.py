from PyQt5.QtSerialPort import QSerialPort, QSerialPortInfo
from PyQt5 import QtWidgets
from PyQt5.QtCore import QIODevice


class SerialPort(QtWidgets.QMainWindow):
    def __init__(self, ui):
        QtWidgets.QWidget.__init__(self)
        self.serial = QSerialPort()
        self.serial.setBaudRate(115200)
        self.ports = QSerialPortInfo().availablePorts()
        self.portlist = [port.portName() for port in self.ports]
        # Добавление в ComboBox(objectName = comboSerial)
        # названий доступных портов.
        self.ui = ui
        ui.comboSerial.addItems(self.portlist)
        print('+++')

    def open_serial(self):
        self.serial.setPortName(self.ui.comboSerial.currentText())
        self.serial.open(QIODevice.ReadWrite)

    def close_serial(self):
        self.serial.setPortName(self.ui.comboSerial.currentText())
        self.serial.close()

    def serial_send(self, data):
        txs = ''
        for val in data:
            txs += str(val)
            txs += ','
        txs = txs[:-1]
        txs += ';'
        self.serial.write(txs.encode())

    def check_connect(self, value):
        if value == 2:
            value = 1
        self.serial_send([0, value])
