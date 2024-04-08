from PyQt5 import QtWidgets
from math import sin, asin, sqrt, pow


class CoordinatesCalculation(QtWidgets.QMainWindow):
    def __init__(self, ui):
        QtWidgets.QWidget.__init__(self)
        self.ui = ui
        self.value = int(self.ui.valueX.displayText())
        self.all_width = 1000
        self.stepper_const = {1: {'l0': 500,
                                  'b': 242.074,
                                  'alpha': 0.903,
                                  'length': 730,
                                  'a': 340,
                                  }
                              }

    def get_target(self, stepper_number=1):
        return ((self.stepper_const[stepper_number]['l0'] -
                (self.stepper_const[stepper_number]['b'] *
                sin(self.stepper_const[stepper_number]['alpha'] -
                    asin(int(self.ui.valueX.displayText()) /
                         (2 * self.stepper_const[stepper_number]['length']))) +
                 sqrt(pow(self.stepper_const[stepper_number]['b'], 2) *
                 pow(sin(self.stepper_const[stepper_number]['alpha'] -
                         asin(int(self.ui.valueX.displayText()) /
                              (2 * self.stepper_const[stepper_number]
                               ['length']))), 2) -
                    pow(self.stepper_const[stepper_number]['b'], 2) +
                    pow(self.stepper_const[stepper_number]['a'], 2)))) /
                1.75) * 2048

    def get_cycle_target(self, stepper_number=1):
        # length_value = int(self.ui.valueLength.displayText())
        width_value = int(self.ui.valueWidth.displayText()) / 2
        target_width = self.all_width - width_value
        return ((self.stepper_const[stepper_number]['l0'] -
                (self.stepper_const[stepper_number]['b'] *
                sin(self.stepper_const[stepper_number]['alpha'] -
                    asin(target_width /
                         (2 * self.stepper_const[stepper_number]['length']))) +
                 sqrt(pow(self.stepper_const[stepper_number]['b'], 2) *
                 pow(sin(self.stepper_const[stepper_number]['alpha'] -
                         asin(target_width /
                              (2 * self.stepper_const[stepper_number]
                               ['length']))), 2) -
                    pow(self.stepper_const[stepper_number]['b'], 2) +
                    pow(self.stepper_const[stepper_number]['a'], 2)))) /
                1.75) * 2048
