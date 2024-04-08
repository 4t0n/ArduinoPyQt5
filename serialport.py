from PyQt5 import QtWidgets
from PyQt5.QtCore import QIODevice
from PyQt5.QtSerialPort import QSerialPort, QSerialPortInfo

# from stepper_control import StepperControl
# from coordinates_calculation import CoordinatesCalculation


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
        # self.stepper_1 = StepperControl(self.serial, self.ui, 1)
        # self.coordinate = CoordinatesCalculation(self.ui)

    def open_serial(self):
        try:
            self.serial.setPortName(self.ui.comboSerial.currentText())
            if self.serial.open(QIODevice.ReadWrite):
                self.ui.serial_status.setStyleSheet(
                    'background-color: green;'
                    'border: 2px solid black;'
                )
            else:
                raise Exception
        except Exception:
            print('Не удалось подключиться.')

    def close_serial(self):
        self.serial.setPortName(self.ui.comboSerial.currentText())
        self.serial.close()
        self.ui.serial_status.setStyleSheet(
            'background-color: red;'
            'border: 2px solid black;'
        )

    def serial_send(self, data):
        data_str = ','.join(list(map(str, data))) + ';'
        if self.serial.write(data_str.encode()) == -1:
            print('Подключите оборудование.')
        print(data_str.encode())

    def check_connect(self, value):
        if value == 2:
            value = 1
        self.serial_send([0, value])
