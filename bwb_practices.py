
from PyQt5 import QtWidgets
from PyQt5 import QtGui
from PyQt5 import QtCore
import datetime
import logging
import time
import bwb_model


class PracticeCompositeWidget(QtWidgets.QWidget):
    item_selection_changed_signal = QtCore.pyqtSignal()
    current_row_changed_signal = QtCore.pyqtSignal(int)
    new_practice_button_pressed_signal = QtCore.pyqtSignal(str)

    def __init__(self):
        super().__init__()

        vbox = QtWidgets.QVBoxLayout()
        self.setLayout(vbox)

        # Creating widgets
        # ..for ten practices (left column)
        habits_label = QtWidgets.QLabel("<h3>Habits/Practices</h3>")
        vbox.addWidget(habits_label)
        self.list_widget = QtWidgets.QListWidget()
        self.list_widget.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        vbox.addWidget(self.list_widget)
        self.list_widget.currentItemChanged.connect(self.on_current_row_changed)
        self.list_widget.itemPressed.connect(self.on_item_selection_changed)
        # -itemClicked didn't work, unknown why (it worked on the first click but never when running in debug mode)
        # -currentItemChanged cannot be used here since it is activated before the list of selected items is updated
        # ..for adding new habit
        self.adding_new_practice_ey = QtWidgets.QLineEdit()
        vbox.addWidget(self.adding_new_practice_ey)
        self.adding_new_practice_bn = QtWidgets.QPushButton("Add new practice")
        vbox.addWidget(self.adding_new_practice_bn)
        self.adding_new_practice_bn.clicked.connect(self.on_add_new_practice_button_pressed)


    def on_add_new_practice_button_pressed(self):
        text_sg = self.adding_new_practice_ey.text().strip()  # strip is needed to remove a newline at the end (why?)
        if not (text_sg and text_sg.strip()):
            return
        #######self.list_widget.setCurrentRow(-1)  # -experimental
        self.new_practice_button_pressed_signal.emit(text_sg)
        self.adding_new_practice_ey.clear()

    def on_current_row_changed(self):
        self.current_row_changed_signal.emit(self.list_widget.currentRow())

    def on_item_selection_changed(self, i_qlistwidget_item):
        logging.debug("self.list_widget.currentRow() = " + str(self.list_widget.currentRow()))
        logging.debug("len(self.list_widget.selectedItems()) = " + str(len(self.list_widget.selectedItems())))

        current_row_it = self.list_widget.currentRow()
        if current_row_it == -1:
            # We might get here when a karma item has been clicked
            return

        self.item_selection_changed_signal.emit()

    def update_gui(self):
        """
        Signs to use for showing observance:
        ☐ ☑ (Ballot ____, )
        ✓
        ◯ ⬤ (Large Circle, Black Large Circle)
        ○ ● (White Circle, Black Circle (Please note that medium white/black cirlce is smaller than these))
        More here:
        https://unicode-table.com/en/blocks/geometric-shapes/
        https://unicode-table.com/en/blocks/miscellaneous-symbols/
        """
        self.list_widget.clear()
        counter = 0
        for practice_item in bwb_model.PracticesM.get_all():
            # Important: "Alternatively, if you want the widget to have a fixed size based on its contents,
            # you can call QLayout::setSizeConstraint(QLayout::SetFixedSize);"
            # https://doc.qt.io/qt-5/qwidget.html#setSizePolicy-1

            row_i6 = QtWidgets.QListWidgetItem()
            row_layout_l7 = QtWidgets.QVBoxLayout()

            # Updating frequency
            total_number_week_list = []
            today_date = datetime.date.today()
            start_of_today_datetime = datetime.datetime(
                year=today_date.year, month=today_date.month, day=today_date.day)
            ####today_weekday_nr_it = datetime.datetime.now().weekday()
            #start_weekday_it = today_weekday_nr_it  # (Ex: Monday in Sweden, Sunday in the US)
            total_number_for_week_it = 0
            for day_weekday_nr_it in range(0, 7):
                check_box_sign_sg = "○"
                start_of_day_datetime = start_of_today_datetime\
                    - datetime.timedelta(days=today_date.weekday())\
                    + datetime.timedelta(days=day_weekday_nr_it)
                start_of_day_unixtime_it = int(start_of_day_datetime.timestamp())
                t_diary_filtered_list = bwb_model.DiaryM.get_all_for_practice_and_day(
                    practice_item.id, start_of_day_unixtime_it)
                total_number_for_day_it = len(t_diary_filtered_list)
                if total_number_for_day_it > 0:
                    check_box_sign_sg = "●"
                    total_number_for_week_it = total_number_for_week_it + 1
                weekday_one_char_sg = datetime.datetime.fromtimestamp(start_of_day_unixtime_it).strftime("%A")[0:1]
                total_number_week_list.append(check_box_sign_sg)  # t_weekday_one_char_sg.capitalize() +


            # Experimental:
            weekly_goal_reached_sg = ""
            if total_number_for_week_it > 1:
                weekly_goal_reached_sg = " ✔"


            observance_short_formatted_sg = "" + practice_item.title + ""
            row_label_w8 = QtWidgets.QLabel(
                observance_short_formatted_sg
                + "<br>" + ' '.join(x for x in total_number_week_list)
                + weekly_goal_reached_sg
            )

            row_label_w8.adjustSize()
            row_layout_l7.addWidget(row_label_w8)
            row_layout_l7.setContentsMargins(0, 3, 0, 3)
            row_layout_l7.setSpacing(2)

            row_w6 = QtWidgets.QWidget()
            row_w6.setLayout(row_layout_l7)
            row_w6.setSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Minimum)
            row_w6.adjustSize()

            row_i6.setData(QtCore.Qt.UserRole, practice_item.id)

            #my_size = QtCore.QSize(-1, row_w6.height())

            row_i6.setSizeHint(row_w6.sizeHint())
            # - Please note: If we set the size hint to (-1, height) we will get overflow towards the bottom
            self.list_widget.addItem(row_i6)
            self.list_widget.setItemWidget(row_i6, row_w6)

            counter += 1

    def get_selected_id_list(self, i_curr_item=None):
        obs_selected_item_list = self.list_widget.selectedItems()
        ret_obs_selected_id_list = []
        if i_curr_item is not None and i_curr_item.isSelected():
            obs_selected_item_list.append(i_curr_item)
        if obs_selected_item_list is not None:
            ret_obs_selected_id_list = [x.data(QtCore.Qt.UserRole) for x in obs_selected_item_list]
        return ret_obs_selected_id_list

