from PyQt5 import QtWidgets
from PyQt5 import QtCore
from PyQt5 import QtGui


class CustomCalendarWidget(QtWidgets.QCalendarWidget):


    def __init__(self):
        super().__init__()

        self.setGridVisible(True)

    def update_gui(self):
        date_qtextcharformat = QtGui.QTextCharFormat()
        date_qtextcharformat.setFontWeight(QtGui.QFont.Bold)
        self.setDateTextFormat(QtCore.QDate(2017, 4, 27), date_qtextcharformat)


