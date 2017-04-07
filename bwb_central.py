
from PyQt5 import QtWidgets
from PyQt5 import QtCore
from PyQt5 import QtGui
import enum
import bwb_diary
import bwb_model


class CustomTabWidget(QtWidgets.QTabWidget):

    def __init__(self):
        super().__init__()

        #########active_journal_tab_it =
        ###journalm_list.insert(0, "All")


        self.update_gui()

    def update_gui(self):
        journalm_list = bwb_model.JournalM.get_all()
        diary_widget = bwb_diary.DiaryListCompositeWidget()
        self.addTab(diary_widget, "All")
        for journalm in journalm_list:
            self.addTab(QtWidgets.QWidget(), journalm.title_sg)

        ###self.setCurrentIndex()

        # for active_journal_tab_it update gui:
        self.currentWidget().update_gui()

