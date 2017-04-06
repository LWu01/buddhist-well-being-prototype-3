
import bwb_diary

import datetime
import time

from PyQt5 import QtWidgets
from PyQt5 import QtCore
from PyQt5 import QtGui


class CentralWidget(QtWidgets.QWidget):

    def __init__(self):
        super().__init__()

        self.qtabwidget = QtWidgets.QTabWidget()
        self.qtabwidget.setTabPosition(QtWidgets.QTabWidget.North)
        ##self.qtabwidget.setTabShape(QtWidgets.QTabWidget.Triangular)
        vbox_qtw = QtWidgets.QVBoxLayout(self)
        vbox_qtw.addWidget(self.qtabwidget)
        self.setLayout(vbox_qtw)
        diary_widget = bwb_diary.DiaryListCompositeWidget()

        self.qtabwidget.addTab(diary_widget, "All")
        self.qtabwidget.addTab(QtWidgets.QWidget(), "Gratitude")

        """
        self.qtabwidget.addTab(diary_widget, "Living situation etc")
        self.qtabwidget.addTab(QtWidgets.QWidget(), "Gratitude \"Happy Snail\"")
        self.qtabwidget.addTab(QtWidgets.QWidget(), "Natural world")
        self.qtabwidget.addTab(QtWidgets.QWidget(), "Successes")
        self.qtabwidget.addTab(QtWidgets.QWidget(), "Music")
        self.qtabwidget.addTab(QtWidgets.QWidget(), "Self-compassion")
        """

        """
        self.qtabwidget.addTab(diary_widget, "Practices")
        self.qtabwidget.addTab(QtWidgets.QWidget(), "Insights")
        self.qtabwidget.addTab(QtWidgets.QWidget(), "Gratitude")
        self.qtabwidget.addTab(QtWidgets.QWidget(), "Dharma talks")
        self.qtabwidget.addTab(QtWidgets.QWidget(), "Meditation")
        self.qtabwidget.addTab(QtWidgets.QWidget(), "Suffering and (self-)compassion")  # most difficult thing during the day
        """
        # Happiness

        ###self.qtabwidget.addTab(QtWidgets.QWidget(), "_Sangha_")  # Sangha meetings
        # -bold face or other marking once it has been filled in for today or this week


        ### self.qtabwidget.addTab(diary_widget, "Diary 1234567890")

