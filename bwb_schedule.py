import bwb_model
import bwb_date_time_dialog
import datetime
import time
from PyQt5 import QtWidgets
from PyQt5 import QtCore
from PyQt5 import QtGui

NUMBER_OF_COLUMNS = 2


class ScheduleCompositeWidget(QtWidgets.QWidget):

    def __init__(self):
        super().__init__()

        vbox = QtWidgets.QVBoxLayout()
        vbox.setAlignment(QtCore.Qt.AlignTop)
        self.setLayout(vbox)

        # Creating widgets
        scheulde_label = QtWidgets.QLabel("<h3>Schedule</h3>")
        vbox.addWidget(scheulde_label)

        self.table_widget = QtWidgets.QTableWidget()
        self.table_widget.setColumnCount(NUMBER_OF_COLUMNS)
        self.table_widget.setHorizontalHeaderLabels(["Practice", "Hour"])
        self.table_widget.setSelectionMode(QtWidgets.QTableWidget.NoSelection)
        self.table_widget.setSelectionBehavior(QtWidgets.QTableWidget.SelectRows)
        self.table_widget.setEditTriggers(QtWidgets.QTableWidget.NoEditTriggers)
        self.table_widget.verticalHeader().hide()
        vbox.addWidget(self.table_widget)

        self.update_gui()

    def update_gui(self):
        self.table_widget.clear()
        self.table_widget.setHorizontalHeaderLabels(["Hour", "Practice"])
        practices_list = bwb_model.PracticesM.get_all(True)
        filtered_practices_list = []
        for practice_item in practices_list:
            if practice_item.time_of_day != bwb_model.TIME_NOT_SET:
                filtered_practices_list.append(practice_item)
        row_count = 0
        for practice_item in filtered_practices_list:
            self.table_widget.setRowCount(len(filtered_practices_list))

            table_item_col0 = QtWidgets.QTableWidgetItem(str(practice_item.time_of_day))
            self.table_widget.setItem(row_count, 0, table_item_col0)

            table_item_col1 = QtWidgets.QTableWidgetItem(practice_item.title)
            self.table_widget.setItem(row_count, 1, table_item_col1)

            row_count += 1

        ###self.table_widget.sortItems(0)
        self.table_widget.resizeColumnsToContents()
