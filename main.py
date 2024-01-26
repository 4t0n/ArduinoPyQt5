from PyQt5 import QtWidgets, uic
from PyQt5.QtSerialPort import QSerialPort, QSerialPortInfo
from PyQt5.QtCore import QIODevice
import sys
app = QtWidgets.QApplication([])
ui = uic.loadUi('forArduino.ui')

serial = QSerialPort()
serial.setBaudRate(115200)
ports = QSerialPortInfo().availablePorts()
portlist = [port.portName() for port in ports]
ui.comboSerial.addItems(portlist)


def on_read():
    rx = serial.readLine()
    rx_str = str(rx).strip()
    print(rx_str)


def open_serial():
    serial.setPortName(ui.comboSerial.currentText())
    serial.open(QIODevice.ReadWrite)


def close_serial():
    serial.setPortName(ui.comboSerial.currentText())
    serial.close()


def serial_send(data):
    txs = ''
    for val in data:
        txs += str(val)
        txs += ','
    txs = txs[:-1]
    txs += ';'
    serial.write(txs.encode())


def led_control(val):
    if val == 2:
        val = 1
    serial_send([0, val])


def stepper1_up():
    serial_send([1])


def stepper1_down():
    serial_send([2])


def stepper1_stop():
    serial_send([3])


def target_launch():
    serial_send([4, ui.valueX.displayText()])


def target_reset():
    serial_send([5])


serial.readyRead.connect(on_read)
ui.openSerial.clicked.connect(open_serial)
ui.closeSerial.clicked.connect(close_serial)
ui.checkLed.stateChanged.connect(led_control)
ui.stepper1Up.clicked.connect(stepper1_up)
ui.stepper1Down.clicked.connect(stepper1_down)
ui.stepper1Stop.clicked.connect(stepper1_stop)
ui.targetLaunch.clicked.connect(target_launch)
ui.resetTarget.clicked.connect(target_reset)

ui.show()
sys.exit(app.exec())
