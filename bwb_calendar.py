from PyQt5 import QtWidgets
from PyQt5 import QtCore
from PyQt5 import QtGui
import bwb_model


class CustomCalendarWidget(QtWidgets.QCalendarWidget):

    def __init__(self):
        super().__init__()

        self.setGridVisible(True)

        self.currentPageChanged.connect(self.on_current_page_changed)

    def update_gui(self):
        date_qtextcharformat = QtGui.QTextCharFormat()
        date_qtextcharformat.setFontWeight(QtGui.QFont.Bold)

        for diarym in bwb_model.DiaryM.get_all():
            qdatetime = QtCore.QDateTime.fromMSecsSinceEpoch(diarym.date_added_it * 1000)
            self.setDateTextFormat(qdatetime.date(), date_qtextcharformat)

    def on_current_page_changed(self, i_year_int, i_month_int):
        print("year: " + str(i_year_int) + " month: " + str(i_month_int))


