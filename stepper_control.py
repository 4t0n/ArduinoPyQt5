from PyQt5 import QtWidgets

from coordinates_calculation import CoordinatesCalculation
from serialport import SerialPort


class StepperControl(QtWidgets.QMainWindow):
    def __init__(self,
                 serial: SerialPort,
                 ui,
                 up_button: QtWidgets.QPushButton,
                 down_button: QtWidgets.QPushButton,
                 target_button: QtWidgets.QPushButton,
                 stepper_number=1,
                 ):
        QtWidgets.QWidget.__init__(self)
        self.ui = ui
        self.serial = serial
        self.stepper_number = stepper_number
        self.up_button = up_button
        self.down_button = down_button
        self.target_button = target_button
        self.coordinate = CoordinatesCalculation(self.ui)

    def stepper_up(self):
        if self.up_button.isChecked():
            self.serial.serial_send([1, self.stepper_number, 1])
        else:
            self.serial.serial_send([1, self.stepper_number, 3])

    def stepper_down(self):
        if self.down_button.isChecked():
            self.serial.serial_send([1, self.stepper_number, 2])
        else:
            self.serial.serial_send([1, self.stepper_number, 3])

    def stepper_stop(self):
        self.serial.serial_send([1, self.stepper_number, 3])

    def stepper_go_target(self):
        if self.target_button.isChecked():
            self.serial.serial_send([
                2,
                self.stepper_number,
                self.coordinate.get_target(self.stepper_number)
            ])
        else:
            self.serial.serial_send([1, self.stepper_number, 3])

    def stepper_go_target_cycle(self):
        self.serial.serial_send([
            2,
            self.stepper_number,
            self.coordinate.get_cycle_target(self.stepper_number)
        ])

    def stepper_go_home(self):
        self.serial.serial_send([
            2,
            self.stepper_number,
            0
        ])

    def stepper_target_reset(self):
        self.serial.serial_send([3, self.stepper_number])

    def start_cycle(self):
        self.serial.serial_send([4, self.coordinate.
                                 get_cycle_target(self.stepper_number)])

    def stop_cycle(self):
        self.serial.serial_send([5])
