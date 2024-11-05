from PyQt5 import QtWidgets


class ElementColor(QtWidgets.QMainWindow):
    def __init__(self, element: QtWidgets.QPushButton, color1, color2):
        QtWidgets.QWidget.__init__(self)
        self.element = element
        self.color1 = color1
        self.color2 = color2

    def change_color(self, value):
        if value == 2:
            self.element.setStyleSheet(f'color: {self.color1};')
        else:
            self.element.setStyleSheet(f'color: {self.color2};')

    def change_color_progress(self):
        self.element.setStyleSheet(f'background-color: {self.color1};')

    def change_color_finished(self):
        self.element.setStyleSheet(f'background-color: {self.color2};')
