import sys

from PyQt5 import QtWidgets

from coordinates_calculation import CoordinatesCalculation
from element_steel import ElementColor
from forArduino import Ui_MainWindow
from serialport import SerialPort
from stepper_control import StepperControl

# Конвертация .ui to .py pyuic5 forArduino.ui -o forArduino.py


class MyWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(MyWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.on_cycle = False
        self.serial_port = SerialPort(self.ui)
        self.stepper_1 = StepperControl(self.serial_port,
                                        self.ui,
                                        self.ui.stepper1Up,
                                        self.ui.stepper1Down,
                                        self.ui.targetLaunch,
                                        1,
                                        )
        self.frame1 = ElementColor(self.ui.border1, 'red', 'rgb(170, 85, 0)')
        self.frame2 = ElementColor(self.ui.border2, 'red', 'rgb(170, 85, 0)')
        self.frame3 = ElementColor(self.ui.border3, 'red', 'rgb(170, 85, 0)')
        self.frame4 = ElementColor(self.ui.border4, 'red', 'rgb(170, 85, 0)')
        self.operation1 = ElementColor(self.ui.operation1, 'yellow', 'green')
        self.operation2_1 = ElementColor(self.ui.operation2_1,
                                         'yellow',
                                         'green')
        self.operation2_2 = ElementColor(self.ui.operation2_2,
                                         'yellow',
                                         'green')
        self.operation3 = ElementColor(self.ui.operation3, 'yellow', 'green')
        self.coordinate = CoordinatesCalculation(self.ui)
        # self.cycle = MainCycle(self.ui, 1, self.ui.checkBorder1,
        #                        self.ui.checkBorder2,
        #                        self.ui.checkBorder3, self.ui.checkBorder4)
        self.ui.openSerial.clicked.connect(self.serial_port.open_serial)
        self.ui.closeSerial.clicked.connect(self.serial_port.close_serial)
        self.serial_port.serial.readyRead.connect(self.on_read)
        self.ui.stepper1Up.clicked.connect(self.stepper_1.stepper_up)
        self.ui.stepper1Up.clicked.connect(self.stepper_down_off)
        self.ui.stepper1Up.clicked.connect(self.target_launch_off)
        self.ui.stepper1Down.clicked.connect(self.stepper_1.stepper_down)
        self.ui.stepper1Down.clicked.connect(self.stepper_up_off)
        self.ui.stepper1Down.clicked.connect(self.target_launch_off)
        self.ui.stepper1Stop.clicked.connect(self.stepper_1.stepper_stop)
        self.ui.stepper1Stop.clicked.connect(self.stepper_up_off)
        self.ui.stepper1Stop.clicked.connect(self.stepper_down_off)
        self.ui.stepper1Stop.clicked.connect(self.target_launch_off)
        self.ui.targetLaunch.clicked.connect(self.stepper_1.stepper_go_target)
        self.ui.targetLaunch.clicked.connect(self.stepper_up_off)
        self.ui.targetLaunch.clicked.connect(self.stepper_down_off)
        self.ui.resetTarget.clicked.connect(self.stepper_1.
                                            stepper_target_reset)
        self.ui.stopButton.clicked.connect(self.start_off)
        self.ui.checkBorder1.stateChanged.connect(self.frame1.change_color)
        self.ui.checkBorder2.stateChanged.connect(self.frame2.change_color)
        self.ui.checkBorder3.stateChanged.connect(self.frame3.change_color)
        self.ui.checkBorder4.stateChanged.connect(self.frame4.change_color)
        # self.ui.checkBorder1.stateChanged.connect(self.cycle.check_print)
        self.ui.startButton.clicked.connect(self.stepper_1.start_cycle)
        self.ui.startButton.clicked.connect(self.set_on_cycle)
        self.ui.stopButton.clicked.connect(self.stepper_1.stop_cycle)
        self.ui.mode_slider.valueChanged.connect(self.mode_change)

    def mode_change(self):
        self.stepper_1.stepper_stop()
        if self.ui.mode_slider.value() == 1:
            self.ui.startButton.setChecked(False)
            self.ui.startButton.setEnabled(False)
            self.ui.stopButton.setEnabled(False)
            self.ui.targetLaunch.setEnabled(True)
            self.ui.targetLaunch_3.setEnabled(True)
            self.ui.targetLaunch_4.setEnabled(True)
            self.ui.resetTarget.setEnabled(True)
            self.ui.resetTarget_3.setEnabled(True)
            self.ui.resetTarget_4.setEnabled(True)
            self.ui.stepper1Up.setEnabled(True)
            self.ui.stepper1Down.setEnabled(True)
            self.ui.stepper1Stop.setEnabled(True)
            self.ui.stepper2Up.setEnabled(True)
            self.ui.stepper2Down.setEnabled(True)
            self.ui.stepper2Stop.setEnabled(True)
            self.ui.stepper3Up.setEnabled(True)
            self.ui.stepper3Down.setEnabled(True)
            self.ui.stepper3Stop.setEnabled(True)
        else:
            self.ui.stepper1Up.setChecked(False)
            self.ui.stepper1Down.setChecked(False)
            self.ui.targetLaunch.setChecked(False)
            self.ui.startButton.setEnabled(True)
            self.ui.stopButton.setEnabled(True)
            self.ui.targetLaunch.setEnabled(False)
            self.ui.targetLaunch_3.setEnabled(False)
            self.ui.targetLaunch_4.setEnabled(False)
            self.ui.resetTarget.setEnabled(False)
            self.ui.resetTarget_3.setEnabled(False)
            self.ui.resetTarget_4.setEnabled(False)
            self.ui.stepper1Up.setEnabled(False)
            self.ui.stepper1Down.setEnabled(False)
            self.ui.stepper1Stop.setEnabled(False)
            self.ui.stepper2Up.setEnabled(False)
            self.ui.stepper2Down.setEnabled(False)
            self.ui.stepper2Stop.setEnabled(False)
            self.ui.stepper3Up.setEnabled(False)
            self.ui.stepper3Down.setEnabled(False)
            self.ui.stepper3Stop.setEnabled(False)

    def stepper_up_off(self):
        self.ui.stepper1Up.setChecked(False)

    def stepper_down_off(self):
        self.ui.stepper1Down.setChecked(False)

    def target_launch_off(self):
        self.ui.targetLaunch.setChecked(False)

    def start_off(self):
        self.ui.startButton.setChecked(False)

    def set_on_cycle(self):
        self.on_cycle = True

    def set_off_cycle(self):
        self.on_cycle = False

    def on_read(self):
        # if not serial.canReadLine():
        #     return     # выходим если нечего читать
        rx = self.serial_port.serial.readLine()
        try:
            rxs = str(rx, 'utf-8').strip()
            data = list(map(str, rxs.split(',')))
            print(data)
            if self.on_cycle:
                match data[0]:
                    case '0':
                        self.operation1.change_color_progress()
                    case '2':
                        self.operation1.change_color_finished()
                        self.operation2_1.change_color_progress()
                    case '4':
                        self.operation2_1.change_color_finished()
                        self.operation2_2.change_color_progress()
                    case '6':
                        self.operation2_2.change_color_finished()
                        self.operation3.change_color_progress()
                    case '7':
                        self.operation3.change_color_finished()
                        self.on_cycle = False

        except (UnicodeDecodeError, ValueError):
            print(f'Ошибка при передаче данных: {rx}')


app = QtWidgets.QApplication([])
application = MyWindow()
application.show()
sys.exit(app.exec())
