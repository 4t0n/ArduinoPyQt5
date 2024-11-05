from PyQt5 import QtWidgets

from coordinates_calculation import CoordinatesCalculation as CoordCalc

# from stepper_control import StepperControl


class MainCycle(QtWidgets.QMainWindow):
    def __init__(
        self,
        ui,
        stepper_number=1,
        *elements,
    ):
        QtWidgets.QWidget.__init__(self)
        self.ui = ui
        self.elements = elements
        self.stepper_number = stepper_number
        self.border_list = []
        # self.stepper1 = StepperControl()
        self.coordinate = CoordCalc(self.ui)

    def check_print(self):
        self.border_list = [el.isChecked() for el in self.elements]
        print(self.border_list)

    def set_on_cycle(self):
        self.on_cycle = True
        self.stepper_1.stepper_go_target_cycle()

    def set_off_cycle(self):
        self.on_cycle = False
