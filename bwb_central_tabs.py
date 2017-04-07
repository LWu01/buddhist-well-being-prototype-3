
from PyQt5 import QtWidgets
from PyQt5 import QtCore
from PyQt5 import QtGui
import bwb_diary
import bwb_model
import bwb_global
import bwb_date_time_dialog
import enum
import datetime
import time


class CustomTabWidget(QtWidgets.QTabWidget):

    def __init__(self):
        super().__init__()

        #########active_journal_tab_it =
        ###journalm_list.insert(0, "All")

        self.setTabPosition(self.South)

        journalm_list = bwb_model.JournalM.get_all()
        self.clear()

        for journalm in journalm_list:
            another_widget = bwb_diary.DiaryListCompositeWidget(journalm.id_it)
            self.addTab(another_widget, journalm.title_sg)
            another_widget.add_text_to_diary_button_pressed_signal.connect(self.on_diary_add_entry_button_pressed)
            another_widget.context_menu_change_date_signal.connect(self.on_diary_context_menu_change_date)
            another_widget.context_menu_delete_signal.connect(self.on_diary_context_menu_delete)

        self.currentChanged.connect(self.update_gui)

        self.update_gui()

    def update_gui(self):
        if self.currentWidget() is not None:
            self.currentWidget().update_gui()

    def rebuild_tabs(self):
        #remove all tabs
        #add all tabs (including new ones)

        self.update_gui()

        ##old_block_state_bl = self.blockSignals(True)
        ##self.blockSignals(old_block_state_bl)


    def on_diary_add_entry_button_pressed(self, i_text_sg, i_unix_time_it):

        print("t_unix_time_it = " + str(i_unix_time_it))


        bwb_model.DiaryM.add(i_unix_time_it, i_text_sg, self.currentWidget().journal_id_it)  # TODO: Change from currentIndex
        self.currentWidget().adding_text_to_diary_textedit_w6.clear()
        self.update_gui()

    def on_diary_context_menu_change_date(self):
        self.update_gui()

    def on_diary_context_menu_delete(self):
        self.update_gui()

