import bwb_model
import bwb_date_time_dialog
import datetime
import time
from PyQt5 import QtWidgets
from PyQt5 import QtCore
from PyQt5 import QtGui

ADD_NEW_HEIGHT_IT = 50


class DiaryListCompositeWidget(QtWidgets.QWidget):
    """
    Inspiration for this class:
    http://stackoverflow.com/questions/20041385/python-pyqt-setting-scroll-area
    """

    add_text_to_diary_button_pressed_signal = QtCore.pyqtSignal(str, int)
    context_menu_change_date_signal = QtCore.pyqtSignal()
    context_menu_delete_signal = QtCore.pyqtSignal()

    id_for_entry_last_clicked_it = None

    def __init__(self):
        super().__init__()

        self.vbox_l2 = QtWidgets.QVBoxLayout(self)
        self.setLayout(self.vbox_l2)

        hbox_l3 = QtWidgets.QHBoxLayout(self)
        self.vbox_l2.addLayout(hbox_l3)
        diary_label = QtWidgets.QLabel("<h3>Diary</h3>")
        hbox_l3.addWidget(diary_label)
        # -strange but we have to set a min width to avoid seeing the horizontal scrollbar

        self.my_widget_w4 = QtWidgets.QWidget()
        self.scroll_area_w3 = QtWidgets.QScrollArea()
        self.scroll_area_w3.setWidget(self.my_widget_w4)
        self.scroll_area_w3.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        self.scroll_area_w3.setWidgetResizable(True)
        self.scroll_list_vbox_l5 = QtWidgets.QVBoxLayout(self)
        self.my_widget_w4.setLayout(self.scroll_list_vbox_l5)
        self.vbox_l2.addWidget(self.scroll_area_w3)

        MY_WIDGET_NAME = "test-name"
        self.my_widget_w4.setObjectName(MY_WIDGET_NAME)
        self.my_widget_w4.setStyleSheet("#" + MY_WIDGET_NAME + "{" + "background-image:url(\"Gerald-G-Yoga-Poses-stylized-1-300px-CC0.png\"); background-position:center; background-repeat:no-repeat" + "}")

        """
        background_qpm = QtGui.QPixmap("Gerald-G-Yoga-Poses-stylized-1-300px-CC0.png")
        background_qpm = background_qpm.scaled(self.my_widget_w4.size(), QtCore.Qt.KeepAspectRatioByExpanding)
        palette_qpe = QtGui.QPalette()
        palette_qpe.setBrush(QtGui.QPalette.Background, QtGui.QBrush(background_qpm))
        self.my_widget_w4.setPalette(palette_qpe)
        """

        ###self.list_widget.itemPressed.connect(self.on_item_pressed)  # Clicked doesn't work
        ###self.list_widget.setSelectionMode(QtWidgets.QAbstractItemView.NoSelection)
        ###self.list_widget.setVerticalScrollMode(QtWidgets.QAbstractItemView.ScrollPerPixel)

        # Adding new diary entry..
        # ..descriptive label
        diary_entry_label = QtWidgets.QLabel("<h4>New diary entry</h4>")
        self.vbox_l2.addWidget(diary_entry_label)
        # ..question
        self.question_label = QtWidgets.QLabel()
        self.vbox_l2.addWidget(self.question_label)
        # ..
        edit_diary_entry_hbox_l5 = QtWidgets.QHBoxLayout()
        self.vbox_l2.addLayout(edit_diary_entry_hbox_l5)
        # ..text area
        self.adding_text_to_diary_textedit_w6 = QtWidgets.QTextEdit()
        edit_diary_entry_hbox_l5.addWidget(self.adding_text_to_diary_textedit_w6)
        self.adding_text_to_diary_textedit_w6.setFixedHeight(ADD_NEW_HEIGHT_IT)
        edit_diary_entry_vbox_l6 = QtWidgets.QVBoxLayout()
        edit_diary_entry_hbox_l5.addLayout(edit_diary_entry_vbox_l6)
        self.adding_to_diary_date_datetimeedit_w6 = QtWidgets.QDateTimeEdit()
        self.adding_to_diary_date_datetimeedit_w6.setDisplayFormat("dddd")
        self.adding_to_diary_date_datetimeedit_w6.setCalendarPopup(True)
        self.update_gui_date()
        edit_diary_entry_vbox_l6.addWidget(self.adding_to_diary_date_datetimeedit_w6)
        self.adding_to_diary_now_button = QtWidgets.QPushButton("Now/Today")
        self.adding_to_diary_now_button.pressed.connect(self.on_today_button_pressed)
        edit_diary_entry_vbox_l6.addWidget(self.adding_to_diary_now_button)

        self.adding_diary_entry_bn_w5 = QtWidgets.QPushButton("Add new diary entry")
        self.vbox_l2.addWidget(self.adding_diary_entry_bn_w5)
        self.adding_diary_entry_bn_w5.clicked.connect(self.on_add_text_to_diary_button_clicked)



    def on_custom_label_mouse_pressed(self, i_qmouseevent, i_diary_id_it):
        print("button clicked: " + str(i_qmouseevent.button()))
        print("diary id: " + str(i_diary_id_it))
        self.id_for_entry_last_clicked_it = i_diary_id_it


    def on_item_pressed(self, i_qmouseevent):
        print("button clicked: " + str(i_qmouseevent.button()))

        ##self.row_last_clicked
        ###asdf

        """
        row_index_it = i_listwidgetitem.listWidget().row(i_listwidgetitem)
        print("cell clicked -- row = " + str(row_index_it))
        self.row_last_clicked = i_listwidgetitem
        """

    def contextMenuEvent(self, i_QContextMenuEvent):
        """
        Overridden
        Docs: http://doc.qt.io/qt-5/qwidget.html#contextMenuEvent
        """
        self.right_click_menu = QtWidgets.QMenu()
        rename_action = QtWidgets.QAction("Rename")
        rename_action.triggered.connect(self.on_context_menu_rename)
        self.right_click_menu.addAction(rename_action)
        delete_action = QtWidgets.QAction("Delete")
        delete_action.triggered.connect(self.on_context_menu_delete)
        self.right_click_menu.addAction(delete_action)
        change_date_action = QtWidgets.QAction("Change date")
        change_date_action.triggered.connect(self.on_context_menu_change_date)
        self.right_click_menu.addAction(change_date_action)
        self.right_click_menu.exec_(QtGui.QCursor.pos())

    def on_context_menu_delete(self):
        message_box_reply = QtWidgets.QMessageBox.question(
            self, "Remove diary entry?", "Are you sure that you want to remove this diary entry?"
        )
        if message_box_reply == QtWidgets.QMessageBox.Yes:
            bwb_model.DiaryM.remove(int(self.id_for_entry_last_clicked_it))
            self.update_gui()
            self.context_menu_delete_signal.emit()
        else:
            pass  # -do nothing

    def on_context_menu_rename(self):
        """
        Docs: http://doc.qt.io/qt-5/qinputdialog.html#getText
        """
        last_clicked_row_dbkey_it = int(self.id_for_entry_last_clicked_it)
        diary_entry = bwb_model.DiaryM.get(last_clicked_row_dbkey_it)
        text_input_dialog = QtWidgets.QInputDialog()
        new_text_qstring = text_input_dialog.getText(
            self, "Rename dialog", "New name: ", text=diary_entry.diary_text)
        if new_text_qstring[0]:
            print("new_text_qstring = " + str(new_text_qstring))
            bwb_model.DiaryM.update_note(last_clicked_row_dbkey_it, new_text_qstring[0])
            self.update_gui()
        else:
            pass  # -do nothing

    def on_context_menu_change_date(self):
        last_clicked_row_dbkey_it = int(self.id_for_entry_last_clicked_it)
        diary_item = bwb_model.DiaryM.get(last_clicked_row_dbkey_it)
        updated_time_unix_time_it = bwb_date_time_dialog.DateTimeDialog.get_date_time_dialog(diary_item.date_added_it)
        if updated_time_unix_time_it != -1:
            bwb_model.DiaryM.update_date(diary_item.id, updated_time_unix_time_it)
            self.update_gui()
            self.context_menu_change_date_signal.emit()
        else:
            pass  # -do nothing

    def update_gui(self):

        # Clearing
        ###self.list_widget.clear()
        while self.scroll_list_vbox_l5.count():
            child_qlayoutitem = self.scroll_list_vbox_l5.takeAt(0)
            if child_qlayoutitem.widget():
                child_qlayoutitem.widget().deleteLater()

        prev_diary_entry = None

        for diary_entry in bwb_model.DiaryM.get_all_for_today():
            # Setting up the underlying data
            practice_for_diaryentry = bwb_model.PracticesM.get_for_diary_id(diary_entry.practice_ref_it)

            delimiter_sg = ", "
            if (prev_diary_entry is None) or (not is_same_day(prev_diary_entry.date_added_it, diary_entry.date_added_it)):
                t_date_as_weekday_sg = datetime.datetime.fromtimestamp(diary_entry.date_added_it).strftime("%A")
                listitem_cqll = CustomQLabel("     " + t_date_as_weekday_sg.title())
                ##########listitem_cqll.setFlags(listitem_cqll.flags() & ~ QtCore.Qt.ItemIsSelectable & QtCore.Qt.ItemIsUserCheckable)
                self.scroll_list_vbox_l5.addWidget(listitem_cqll)
            karma_title_sg = ""
            label_text_sg = karma_title_sg\
                + "[" + practice_for_diaryentry.title.strip(delimiter_sg) + "] "\
                + diary_entry.diary_text.strip()

            # Setting up the display
            listitem_cqll = CustomQLabel(label_text_sg, diary_entry.id)
            listitem_cqll.setWordWrap(True)
            listitem_cqll.mouse_pressed_signal.connect(self.on_custom_label_mouse_pressed)

            self.scroll_list_vbox_l5.addWidget(listitem_cqll)

            prev_diary_entry = diary_entry  # -used for the weekday labels
        self.scroll_list_vbox_l5.addStretch()
        #####self.scroll_list_vbox.scrollToBottom() asdf

    def update_gui_date(self, i_unix_time_it = time.time()):
        """
        Not like other update_gui_ functions, this one is not called from the bwb_window.WellBeingWindow.update_gui
        function.
        """
        qdatetime = QtCore.QDateTime()
        qdatetime.setMSecsSinceEpoch(i_unix_time_it * 1000)
        self.adding_to_diary_date_datetimeedit_w6.setDateTime(qdatetime)

    def on_today_button_pressed(self):
        self.update_gui_date(time.time())

    def on_add_text_to_diary_button_clicked(self):
        notes_sg = self.adding_text_to_diary_textedit_w6.toPlainText().strip()
        time_qdatetime = self.adding_to_diary_date_datetimeedit_w6.dateTime()
        unix_time_it = time_qdatetime.toMSecsSinceEpoch() // 1000
        self.add_text_to_diary_button_pressed_signal.emit(notes_sg, unix_time_it)

def is_same_day(i_first_date_it, i_second_date_it):
    first_date = datetime.datetime.fromtimestamp(i_first_date_it)
    second_date = datetime.datetime.fromtimestamp(i_second_date_it)
    return first_date.date() == second_date.date()  # - == operator works for "datetime" type


class CustomQLabel(QtWidgets.QLabel):
    NO_DIARY_ENTRY_SELECTED = -1
    diary_entry_id = NO_DIARY_ENTRY_SELECTED
    mouse_pressed_signal = QtCore.pyqtSignal(QtGui.QMouseEvent, int)

    def __init__(self, i_text_sg, i_diary_entry_id = NO_DIARY_ENTRY_SELECTED):
        super().__init__(i_text_sg)
        self.diary_entry_id = i_diary_entry_id

    # Overridden
    # Please note that this is not an event, but the event handler!
    def mousePressEvent(self, i_qmouseevent):
        self.mouse_pressed_signal.emit(i_qmouseevent, self.diary_entry_id)



