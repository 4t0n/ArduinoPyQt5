from PyQt5 import QtWidgets, uic
from PyQt5.QtSerialPort import QSerialPort, QSerialPortInfo
from PyQt5.QtCore import QIODevice
from math import *
import sys
import time
import asyncio

app = QtWidgets.QApplication([])
ui = uic.loadUi('forArduino.ui')

serial = QSerialPort()
serial.setBaudRate(115200)
ports = QSerialPortInfo().availablePorts()
portlist = [port.portName() for port in ports]
ui.comboSerial.addItems(portlist)  # добавление в ComboBox(objectName = comboSerial) названий доступных портов


def on_read():
    # if not serial.canReadLine():
    #     return     # выходим если нечего читать
    rx = serial.readLine()
    rxs = str(rx, 'utf-8').strip()
    data = rxs.split(',')
    print(data)


def open_serial():  # подключение к порту, выбранному в ComboBox(objectName = comboSerial)
    serial.setPortName(ui.comboSerial.currentText())
    serial.open(QIODevice.ReadWrite)


def close_serial():  # отключение от порта, выбранного в ComboBox(objectName=comboSerial)
    serial.setPortName(ui.comboSerial.currentText())
    serial.close()


def serial_send(data):  # передача в порт строки на основе которой выполняются команды в блоке switch-case в Arduino
    txs = ''
    for val in data:
        txs += str(val)
        txs += ','
    txs = txs[:-1]
    txs += ';'
    serial.write(txs.encode())


def led_control(val):  # управление светодиодом
    if val == 2:
        val = 1
    serial_send([0, val])


def stepper1_up():  # вращение шагового двигателя против часовой стрелки
    serial_send([1])


def stepper1_down():  # вращение шагового двигателя по часовой стрелке
    serial_send([2])


def stepper1_stop():  # остановка шагового двигателя
    serial_send([3])


def target_launch():  # движение концевого захвата робота к координате, заданной в LineEdit (objectName=valueX)
    value_x = int(ui.valueX.displayText())
    stepper1_const = {'l01': 500, 'b1': 242.074, 'alpha': 0.903, 'length': 730, 'a1': 340, }
    stepper2_const = {'l02': 475, 'b2': 105, 'alpha': 0.903, 'length': 730, 'a2': 370, }
    steps_target = ((stepper1_const['l01'] - (stepper1_const['b1'] * sin(
        stepper1_const['alpha'] - asin(value_x / (2 * stepper1_const['length']))) + sqrt(
        pow(stepper1_const['b1'], 2) * pow(
            sin(stepper1_const['alpha'] - asin(value_x / (2 * stepper1_const['length']))), 2) - pow(
            stepper1_const['b1'], 2) + pow(stepper1_const['a1'], 2)))) / 1.75) * 800
    serial_send([4, str(int(steps_target))])


def target_reset():  # сброс положения робота в 0
    serial_send([5])


def change_border_color1(value):
    if value == 2:
        ui.border1.setStyleSheet(
            'color: red;'
        )
    else:
        ui.border1.setStyleSheet(
            'color: rgb(170, 85, 0);'
        )


def change_border_color2(value):
    if value == 2:
        ui.border2.setStyleSheet(
            'color: red;'
        )
    else:
        ui.border2.setStyleSheet(
            'color: rgb(170, 85, 0);'
        )


def change_border_color3(value):
    if value == 2:
        ui.border3.setStyleSheet(
            'color: red;'
        )
    else:
        ui.border3.setStyleSheet(
            'color: rgb(170, 85, 0);'
        )


def change_border_color4(value):
    if value == 2:
        ui.border4.setStyleSheet(
            'color: red;'
        )
    else:
        ui.border4.setStyleSheet(
            'color: rgb(170, 85, 0);'
        )


def start_working():
    checkbox_borders = [ui.checkBorder1, ui.checkBorder2, ui.checkBorder3, ui.checkBorder4]
    selected_borders = list(filter(lambda x: x.isChecked(), checkbox_borders))
    value_x = int(ui.valueLength.displayText())
    stepper1_const = {'l01': 500, 'b1': 242.074, 'alpha': 0.903, 'length': 730, 'a1': 340, }
    steps_target = ((stepper1_const['l01'] - (stepper1_const['b1'] * sin(
        stepper1_const['alpha'] - asin(value_x / (2 * stepper1_const['length']))) + sqrt(
        pow(stepper1_const['b1'], 2) * pow(
            sin(stepper1_const['alpha'] - asin(value_x / (2 * stepper1_const['length']))), 2) - pow(
            stepper1_const['b1'], 2) + pow(stepper1_const['a1'], 2)))) / 1.75) * 800
    serial_send([4, str(int(steps_target))])


serial.readyRead.connect(on_read)
ui.openSerial.clicked.connect(open_serial)  # действие при нажатии кнопки OPEN, PushButton (objectName=openSerial)
ui.closeSerial.clicked.connect(close_serial)  # действие при нажатии кнопки CLOSE, PushButton (objectName=closeSerial)

ui.checkLed.stateChanged.connect(led_control)  # действие при изменении состояния LED, CheckBox (objectName=checkLed)

# действие при изменении состояния выбора стороны детали №1 CheckBox (objectName=checkBorder1)
ui.checkBorder1.stateChanged.connect(change_border_color1)
# действие при изменении состояния выбора стороны детали №2 CheckBox (objectName=checkBorder2)
ui.checkBorder2.stateChanged.connect(change_border_color2)
# действие при изменении состояния выбора стороны детали №3 CheckBox (objectName=checkBorder3)
ui.checkBorder3.stateChanged.connect(change_border_color3)
# действие при изменении состояния выбора стороны детали №4 CheckBox (objectName=checkBorder4)
ui.checkBorder4.stateChanged.connect(change_border_color4)

ui.stepper1Up.clicked.connect(stepper1_up)  # действие при нажатии кнопки Вверх, PushButton (objectName=stepper1Up)
ui.stepper1Down.clicked.connect(stepper1_down)  # действие при нажатии кнопки Вниз, PushButton (objectName=stepper1Down)
ui.stepper1Stop.clicked.connect(stepper1_stop)  # действие при нажатии кнопки Стоп, PushButton (objectName=stepper1Stop)

ui.targetLaunch.clicked.connect(
    target_launch)  # действие при нажатии кнопки Запустить, PushButton (objectName=targetLaunch)
ui.resetTarget.clicked.connect(target_reset)  # действие при нажатии кнопки Сброс, PushButton (objectName=resetTarget)


ui.startButton.clicked.connect(
    start_working)  #

ui.show()
sys.exit(app.exec())
