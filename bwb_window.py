from PyQt5 import QtWidgets
from PyQt5 import QtGui
from PyQt5 import QtCore

import bwb_model
import bwb_central_tabs
import bwb_practice_details
import bwb_practices
import bwb_wisdom
import bwb_help
import bwb_calendar
import bwb_global

import enum
import sys


class EventSource(enum.Enum):
    undefined = -1
    obs_selection_changed = 1
    obs_current_row_changed = 2
    practice_details = 3


class WellBeingWindow(QtWidgets.QMainWindow):
    """
    View and controller
    Suffix explanation:
    _w: widget
    _l: layout
    _# (number): The level in the layout stack
    """
    # noinspection PyArgumentList,PyUnresolvedReferences
    def __init__(self):
        super().__init__()

        # Initializing window
        self.setGeometry(40, 30, 1100, 700)
        self.showMaximized()
        self.setWindowTitle("Buddhist Practice Diary [BWB prototype 3]")
        self.setWindowIcon(QtGui.QIcon("icon.png"))

        # Setup of widgets..

        # ..calendar
        calendar_dock_qw2 = QtWidgets.QDockWidget("Calendar", self)
        self.custom_calendar_w3 = bwb_calendar.CustomCalendarWidget()
        self.custom_calendar_w3.setFixedHeight(200)
        calendar_dock_qw2.setWidget(self.custom_calendar_w3)
        self.addDockWidget(QtCore.Qt.LeftDockWidgetArea, calendar_dock_qw2)
        calendar_dock_qw2.setAllowedAreas(QtCore.Qt.LeftDockWidgetArea)
        self.custom_calendar_w3.selectionChanged.connect(self.on_calendar_selection_changed)

        # TODO: Next day with entry, previous day with entry, TODAY

        # Setup of widgets..
        """
        # ..habits/practices
        practices_dock_qw2 = QtWidgets.QDockWidget("Practices", self)
        practices_dock_qw2.setFeatures(
            QtWidgets.QDockWidget.DockWidgetMovable |
            QtWidgets.QDockWidget.DockWidgetFloatable)
        self.practice_composite_w3 = bwb_practices.PracticeCompositeWidget()
        self.practice_composite_w3.item_selection_changed_signal.connect(self.on_practice_item_selection_changed)
        self.practice_composite_w3.current_row_changed_signal.connect(self.on_practice_current_row_changed)
        self.practice_composite_w3.new_practice_button_pressed_signal.connect(
            self.on_practice_new_button_pressed_signal)
        practices_dock_qw2.setWidget(self.practice_composite_w3)
        self.addDockWidget(QtCore.Qt.LeftDockWidgetArea, practices_dock_qw2)
        """

        """
        # ..practice details
        practice_details_dock_qw2 = QtWidgets.QDockWidget("Journal Details", self)
        self.practice_details_composite_w3 = bwb_practice_details.PracticeCompositeWidget()
        practice_details_dock_qw2.setWidget(self.practice_details_composite_w3)
        self.addDockWidget(QtCore.Qt.LeftDockWidgetArea, practice_details_dock_qw2)
        self.practice_details_composite_w3.time_of_day_state_changed_signal.connect(
            self.on_practice_details_time_of_day_state_changed)
        """

        # ..quotes
        # TODO: A stackedwidget, perhaps with two arrows above for going back and fwd (or just one to switch randomly)

        """
        # ..help
        help_dock_qw2 = QtWidgets.QDockWidget("Help", self)
        self.help_composite_w3 = bwb_help.HelpCompositeWidget()
        help_dock_qw2.setWidget(self.help_composite_w3)
        self.addDockWidget(QtCore.Qt.LeftDockWidgetArea, help_dock_qw2)
        """

        # ..diary
        ####self.diary_composite_w3 = bwb_diary.DiaryListCompositeWidget()
        self.central_w3 = bwb_central_tabs.CustomTabWidget()
        self.setCentralWidget(self.central_w3)

        # ..wisdom
        wisdom_dock_qw2 = QtWidgets.QDockWidget("Wisdom", self)
        self.wisdom_composite_w3 = bwb_wisdom.WisdomCompositeWidget()
        wisdom_dock_qw2.setWidget(self.wisdom_composite_w3)
        self.addDockWidget(QtCore.Qt.RightDockWidgetArea, wisdom_dock_qw2)
        wisdom_dock_qw2.setAllowedAreas(QtCore.Qt.RightDockWidgetArea)

        # ..blessings
        blessings_dock_qw2 = QtWidgets.QDockWidget("Blessings", self)
        self.blessings_qlw = QtWidgets.QListWidget()
        blessings_lt = []
        blessings_lt.append("Not to associate with fools")
        blessings_lt.append("To associate with the wise")
        blessings_lt.append("To pay respects where they are due")
        blessings_lt.append("To reside in a suitable location")
        blessings_lt.append("To have previously done meritorious deeds")
        blessings_lt.append("To be heading in the right direction")
        blessings_lt.append("To have much learning")
        blessings_lt.append("To be skilled and knowledgeable")
        blessings_lt.append("To be restrained by a moral code")
        blessings_lt.append("To have beautiful speech")
        blessings_lt.append("To be a support for your parents")
        blessings_lt.append("The cherishing of wife")
        blessings_lt.append("The cherishing of children")
        blessings_lt.append("To make one's livelihood without difficulty")
        blessings_lt.append("To make gifts")
        blessings_lt.append("To live in accord with the Dhamma")
        blessings_lt.append("To cherish one's relatives")
        blessings_lt.append("To do blameless actions")
        blessings_lt.append("To cease and abstain from evil")
        blessings_lt.append("To refrain from intoxicants")
        blessings_lt.append("Not to be heedless of the Dhamma")
        blessings_lt.append("To be respectful")
        blessings_lt.append("To be humble")
        blessings_lt.append("To be content")
        blessings_lt.append("To have gratitude")
        blessings_lt.append("To hear the Dhamma at the right time")
        blessings_lt.append("To have patience")
        blessings_lt.append("To be easy to admonish")
        blessings_lt.append("The sight of monks")
        blessings_lt.append("To discuss the Dhamma at a suitable time")
        blessings_lt.append("To practice austerities")
        blessings_lt.append("To lead the Holy Life")
        blessings_lt.append("Seeing the Noble Truths")
        blessings_lt.append("The realization of Nibbana")
        blessings_lt.append("A mind unshaken by contact with the world")
        blessings_lt.append("Sorrowlessness")
        blessings_lt.append("Stainlessness")
        blessings_lt.append("Secure")
        self.blessings_qlw.addItems(blessings_lt)
        ###["number " + str(x) for x in range(1, 39)]
        ###self.qstack.addItem(self.blessings_qlw, "Blessings")
        ###self.blessings_composite_w3 = bwb_wisdom.BlessingsCompositeWidget()
        blessings_dock_qw2.setWidget(self.blessings_qlw)
        self.addDockWidget(QtCore.Qt.LeftDockWidgetArea, blessings_dock_qw2)

        """
        # ..image
        image_qll = QtWidgets.QLabel()
        image_qll.setPixmap(QtGui.QPixmap("Gerald-G-Yoga-Poses-stylized-1-300px-CC0.png"))
        image_dock_qw2 = QtWidgets.QDockWidget("Image", self)
        image_dock_qw2.setWidget(image_qll)
        self.addDockWidget(QtCore.Qt.RightDockWidgetArea, image_dock_qw2)
        """

        # Creating the menu bar..
        # ..setup of actions
        export_qaction = QtWidgets.QAction("Export", self)
        export_qaction.triggered.connect(bwb_model.export_all)
        exit_qaction = QtWidgets.QAction("Exit", self)
        exit_qaction.triggered.connect(lambda x: sys.exit())
        redraw_qaction = QtWidgets.QAction("Redraw", self)
        redraw_qaction.triggered.connect(self.update_gui)
        about_qaction = QtWidgets.QAction("About", self)
        about_qaction.triggered.connect(self.show_about_box)
        manual_qaction = QtWidgets.QAction("Manual", self)
        ###manual_qaction.triggered.connect()
        inline_help_qaction = QtWidgets.QAction("Inline help", self)
        ###inline_help_qaction.triggered.connect()
        backup_qaction = QtWidgets.QAction("Backup db", self)
        backup_qaction.triggered.connect(bwb_model.backup_db_file)
        wisdom_window_qaction = wisdom_dock_qw2.toggleViewAction()
        # ..adding menu items
        self.menu_bar = self.menuBar()
        file_menu = self.menu_bar.addMenu("&File")
        debug_menu = self.menu_bar.addMenu("Debu&g")
        help_menu = self.menu_bar.addMenu("&Help")
        window_menu = self.menu_bar.addMenu("&Window")
        file_menu.addAction(export_qaction)
        file_menu.addAction(exit_qaction)
        debug_menu.addAction(redraw_qaction)
        debug_menu.addAction(backup_qaction)
        help_menu.addAction(about_qaction)
        help_menu.addAction(manual_qaction)
        help_menu.addAction(inline_help_qaction)
        window_menu.addAction(wisdom_window_qaction)

        self.update_gui()
        self.show()

    def on_calendar_selection_changed(self):
        print(str(self.custom_calendar_w3.selectedDate()))
        bwb_global.active_date_qdate = self.custom_calendar_w3.selectedDate()
        self.update_gui()

    def on_practice_details_time_of_day_state_changed(self):
        self.update_gui(EventSource.practice_details)

    def on_practice_current_row_changed(self, i_current_practice_row_it):
        self.update_gui(EventSource.obs_current_row_changed)

        if i_current_practice_row_it == -1:
            return

        current_practice_qlistitem = self.practice_composite_w3.list_widget.item(i_current_practice_row_it)
        practice_id_it = current_practice_qlistitem.data(QtCore.Qt.UserRole)
        self.practice_details_composite_w3.change_practice(practice_id_it)

        practice = bwb_model.ReminderM.get(practice_id_it)
        self.central_w3.qtabwidget.widget(0).question_label.setText(practice.question)  ## TODO: Fix .widget(0)

    def on_practice_item_selection_changed(self):
        pass
        ###self.update_gui(EventSource.obs_selection_changed)  # Showing habits for practice etc

    def on_practice_new_button_pressed_signal(self, i_practice_text_sg):
        bwb_model.ReminderM.add(i_practice_text_sg)
        self.update_gui()


    def show_about_box(self):
        message_box = QtWidgets.QMessageBox.about(
            self, "About Buddhist Well-Being",
            ("Concept and programming by _____\n"
            'Photography (for icons) by Torgny Dellsén - <a href="torgnydellsen.zenfolio.com">asdf</a><br>'
            "Software License: GPLv3\n"
            "Art license: CC BY-SA 4.0")
        )

    def update_gui(self, i_event_source = EventSource.undefined):
        if i_event_source == EventSource.practice_details:
            return
        if i_event_source != EventSource.obs_current_row_changed:
            pass
            ##self.practice_composite_w3.update_gui()

        self.central_w3.update_gui()

        self.custom_calendar_w3.update_gui()
