import bwb_global
import bwb_model
import bwb_date_time_dialog
import datetime
import time
from PyQt5 import QtWidgets
from PyQt5 import QtCore
from PyQt5 import QtGui

ADD_NEW_HEIGHT_IT = 75


class DiaryListCompositeWidget(QtWidgets.QWidget):
    """
    Inspiration for this class:
    http://stackoverflow.com/questions/20041385/python-pyqt-setting-scroll-area
    """

    add_text_to_diary_button_pressed_signal = QtCore.pyqtSignal(str, int)
    context_menu_change_date_signal = QtCore.pyqtSignal()
    context_menu_delete_signal = QtCore.pyqtSignal()

    id_for_entry_last_clicked_it = None

    def __init__(self, i_journal_id_it: int):
        super().__init__()

        self.journal_id_it = i_journal_id_it  # This is the db key

        self.vbox_l2 = QtWidgets.QVBoxLayout()
        self.setLayout(self.vbox_l2)

        hbox_l3 = QtWidgets.QHBoxLayout()
        self.vbox_l2.addLayout(hbox_l3)
        journalm = bwb_model.JournalM.get(i_journal_id_it)
        diary_label = QtWidgets.QLabel("<h3>" + journalm.title_sg + " Journal</h3>")
        hbox_l3.addWidget(diary_label)

        hbox_l3.addStretch()
        self.day_view_qrb = QtWidgets.QRadioButton("Diary daily view")
        self.day_view_qrb.setChecked(True)
        hbox_l3.addWidget(self.day_view_qrb)
        self.filter_view_qrb = QtWidgets.QRadioButton("Journal filter view")
        hbox_l3.addWidget(self.filter_view_qrb)
        self.lock_view_qpb = QtWidgets.QPushButton("Lock view")
        self.lock_view_qpb.setCheckable(True)
        hbox_l3.addWidget(self.lock_view_qpb)

        self.my_widget_w5 = QtWidgets.QWidget()
        self.scroll_area_w3 = QtWidgets.QScrollArea()
        self.scroll_area_w3.setWidget(self.my_widget_w5)
        #hbox_l4.addStretch()
        self.scroll_area_w3.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        self.scroll_area_w3.setWidgetResizable(True)
        self.scroll_list_vbox_l6 = QtWidgets.QVBoxLayout()
        self.my_widget_w5.setLayout(self.scroll_list_vbox_l6)
        ###self.my_widget_w5.setMaximumWidth(300)
        self.vbox_l2.addWidget(self.scroll_area_w3)

        MY_WIDGET_NAME = "test-name"
        self.my_widget_w5.setObjectName(MY_WIDGET_NAME)
        self.my_widget_w5.setStyleSheet("#" + MY_WIDGET_NAME +"{" + "background-image:url(\"Gerald-G-Yoga-Poses-stylized-1-300px-CC0.png\"); background-position:center; background-repeat:no-repeat" + "}")

        # Adding new diary entry..
        # ..descriptive label
        diary_entry_label = QtWidgets.QLabel("<h4>New diary entry </h4>")
        hbox_l3 = QtWidgets.QHBoxLayout()
        self.vbox_l2.addLayout(hbox_l3)
        hbox_l3.addWidget(diary_entry_label)
        ##hbox_l3.addStretch()
        # ..question
        self.question_label = QtWidgets.QLabel()
        hbox_l3.addWidget(self.question_label)
        hbox_l3.addStretch()
        # ..journals
        journal_label_list = ["Self-compassion", "Gratitude", "Social"]
        JOURNAL_BUTTON_GROUP_ID_INT = 1
        journal_qbuttongroup = QtWidgets.QButtonGroup(self)  # -the parent has to be set for exclusive to work
        journal_qbuttongroup.setExclusive(True)
        for journal_label_str in journal_label_list:
            journal_button_qpb = QtWidgets.QPushButton(journal_label_str)
            journal_button_qpb.setFlat(True)
            journal_button_qpb.setCheckable(True)
            journal_qbuttongroup.addButton(journal_button_qpb, JOURNAL_BUTTON_GROUP_ID_INT)
            hbox_l3.addWidget(journal_button_qpb)
        # ..
        hbox_l3 = QtWidgets.QHBoxLayout()
        self.vbox_l2.addLayout(hbox_l3)

        # ..text area
        self.adding_text_to_diary_textedit_w6 = QtWidgets.QTextEdit()
        hbox_l3.addWidget(self.adding_text_to_diary_textedit_w6)
        self.adding_text_to_diary_textedit_w6.setFixedHeight(ADD_NEW_HEIGHT_IT)

        # .."add new buttons"
        edit_diary_entry_vbox_l4 = QtWidgets.QVBoxLayout()
        hbox_l3.addLayout(edit_diary_entry_vbox_l4)

        self.add_bn_w3 = QtWidgets.QPushButton("Add new diary entry")
        edit_diary_entry_vbox_l4.addWidget(self.add_bn_w3)
        self.add_bn_w3.clicked.connect(self.on_add_text_to_diary_button_clicked)

        self.next_qbn_w3 = QtWidgets.QPushButton("Next journal")
        edit_diary_entry_vbox_l4.addWidget(self.next_qbn_w3)

        self.add_and_next_qbn_w3 = QtWidgets.QPushButton("Add and Next")
        edit_diary_entry_vbox_l4.addWidget(self.add_and_next_qbn_w3)

    # The same function is used for all the "rows"
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
        clear_widget_and_layout_children(self.scroll_list_vbox_l6)  # -clearing

        for diary_entry in bwb_model.DiaryM.get_all_for_active_day_and_journal(self.journal_id_it):
            label_text_sg = diary_entry.diary_text.strip()

            hbox_l6 = QtWidgets.QHBoxLayout()
            self.scroll_list_vbox_l6.addLayout(hbox_l6)

            journalm = bwb_model.JournalM.get(diary_entry.journal_ref_it)
            journal_sg = str(journalm.title_sg)
            journal_qlabel = QtWidgets.QLabel(journal_sg)
            hbox_l6.addWidget(journal_qlabel, stretch=1)

            listitem_cqll = CustomQLabel(label_text_sg, diary_entry.id)
            listitem_cqll.setWordWrap(True)
            listitem_cqll.mouse_pressed_signal.connect(self.on_custom_label_mouse_pressed)
            ###listitem_cqll.setFixedWidth(400)

            hbox_l6.addWidget(listitem_cqll, stretch=4)
            #hbox_l6.addStretch()

        self.scroll_list_vbox_l6.addStretch()
        #####self.scroll_list_vbox.scrollToBottom() asdf

    def on_add_text_to_diary_button_clicked(self):
        notes_sg = self.adding_text_to_diary_textedit_w6.toPlainText().strip()
        if bwb_global.active_date_qdate == QtCore.QDate.currentDate():
            time_qdatetime = QtCore.QDateTime.currentDateTime()
            unix_time_it = time_qdatetime.toMSecsSinceEpoch() // 1000
        else:
            unix_time_it = bwb_global.qdate_to_unixtime(bwb_global.active_date_qdate)
        self.add_text_to_diary_button_pressed_signal.emit(notes_sg, unix_time_it)


def is_same_day(i_first_date_it, i_second_date_it):
    first_date = datetime.datetime.fromtimestamp(i_first_date_it)
    second_date = datetime.datetime.fromtimestamp(i_second_date_it)
    return first_date.date() == second_date.date()  # - == operator works for "datetime" type


def clear_widget_and_layout_children(qlayout_or_qwidget):
    if qlayout_or_qwidget.widget():
        qlayout_or_qwidget.widget().deleteLater()
    elif qlayout_or_qwidget.layout():
        while qlayout_or_qwidget.layout().count():
            child_qlayoutitem = qlayout_or_qwidget.takeAt(0)
            clear_widget_and_layout_children(child_qlayoutitem)  # Recursive call


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



