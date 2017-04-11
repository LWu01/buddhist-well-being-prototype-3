from PyQt5 import QtWidgets
from PyQt5 import QtCore
from PyQt5 import QtGui


class CustomCalendarWidget(QtWidgets.QCalendarWidget):


    def __init__(self):
        super().__init__()

        self.setGridVisible(True)

        self.currentPageChanged.connect(self.on_current_page_changed)

    def update_gui(self):
        date_qtextcharformat = QtGui.QTextCharFormat()
        date_qtextcharformat.setFontWeight(QtGui.QFont.Bold)
        self.setDateTextFormat(QtCore.QDate(2017, 4, 27), date_qtextcharformat)

    def on_current_page_changed(self, i_year_int, i_month_int):
        print("year: " + str(i_year_int) + " month: " + str(i_month_int))

