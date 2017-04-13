import bwb_global
import bwb_model
import bwb_date_time_dialog
import datetime
from PyQt5 import QtWidgets
from PyQt5 import QtCore
from PyQt5 import QtGui


MY_WIDGET_NAME = "test-name"
BACKGROUND_IMAGE_PATH_STR = "Gerald-G-Yoga-Poses-stylized-1-300px-CC0.png"
NO_ENTRY_CLICKED_INT = -1


class DiaryListCompositeWidget(QtWidgets.QWidget):
    """
    Inspiration for this class:
    http://stackoverflow.com/questions/20041385/python-pyqt-setting-scroll-area
    """

    context_menu_change_date_signal = QtCore.pyqtSignal()
    context_menu_delete_signal = QtCore.pyqtSignal()

    id_for_entry_last_clicked_it = NO_ENTRY_CLICKED_INT

    def __init__(self):
        super().__init__()

        self.vbox_l2 = QtWidgets.QVBoxLayout()
        self.scroll_area_w3 = QtWidgets.QScrollArea()
        self.scroll_area_w3.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        self.scroll_area_w3.setWidgetResizable(True)
        self.scroll_list_widget_w4 = QtWidgets.QWidget()
        self.scroll_list_widget_w4.setObjectName(MY_WIDGET_NAME)
        self.scroll_list_widget_w4.setStyleSheet("#" + MY_WIDGET_NAME
             + "{" + "background-image:url(\"" + BACKGROUND_IMAGE_PATH_STR
             + "\"); background-position:center; background-repeat:no-repeat" + "}")
        self.scroll_list_vbox_l5 = QtWidgets.QVBoxLayout()
        self.scroll_list_widget_w4.setLayout(self.scroll_list_vbox_l5)
        self.scroll_area_w3.setWidget(self.scroll_list_widget_w4)
        self.vbox_l2.addWidget(self.scroll_area_w3)
        self.setLayout(self.vbox_l2)

    # The same function is used for all the "rows"
    def on_custom_label_mouse_pressed(self, i_qmouseevent, i_diary_id_it):
        print("button clicked: " + str(i_qmouseevent.button()))
        print("diary id: " + str(i_diary_id_it))
        self.id_for_entry_last_clicked_it = i_diary_id_it

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
        clear_widget_and_layout_children(self.scroll_list_vbox_l5)
        if bwb_global.active_view_viewenum == bwb_global.ViewEnum.journal_monthly_view:
            qdate = QtCore.QDate(bwb_global.shown_year_it, bwb_global.shown_month_1to12_it, 1)
            qdatetime = QtCore.QDateTime(qdate)
            start_of_month_as_unix_time_it = qdatetime.toMSecsSinceEpoch() // 1000

            for diary_entry in bwb_model.DiaryM.get_all_for_journal_and_month(
                    bwb_global.active_journal_id_it, start_of_month_as_unix_time_it, qdate.daysInMonth()):
                label_text_sg = diary_entry.diary_text.strip()

                hbox_l6 = QtWidgets.QHBoxLayout()
                self.scroll_list_vbox_l5.addLayout(hbox_l6)

                journal_qlabel = QtWidgets.QLabel("-")
                hbox_l6.addWidget(journal_qlabel, stretch=1)

                listitem_cqll = CustomQLabel(label_text_sg, diary_entry.id)
                listitem_cqll.setWordWrap(True)
                listitem_cqll.mouse_pressed_signal.connect(self.on_custom_label_mouse_pressed)
                ###listitem_cqll.setFixedWidth(400)

                hbox_l6.addWidget(listitem_cqll, stretch=4)
                #hbox_l6.addStretch()

        elif bwb_global.active_view_viewenum == bwb_global.ViewEnum.diary_daily_overview:
            for diary_entry in bwb_model.DiaryM.get_all_for_active_day():
                label_text_sg = diary_entry.diary_text.strip()

                hbox_l6 = QtWidgets.QHBoxLayout()
                self.scroll_list_vbox_l5.addLayout(hbox_l6)

                journalm = bwb_model.JournalM.get(diary_entry.journal_ref_it)
                journal_sg = str(journalm.title_sg)
                journal_qlabel = QtWidgets.QLabel(journal_sg)
                hbox_l6.addWidget(journal_qlabel, stretch=1)

                listitem_cqll = CustomQLabel(label_text_sg, diary_entry.id)
                listitem_cqll.setWordWrap(True)
                listitem_cqll.mouse_pressed_signal.connect(self.on_custom_label_mouse_pressed)

                hbox_l6.addWidget(listitem_cqll, stretch=4)
        else:
            pass

        self.scroll_list_vbox_l5.addStretch()

        # TODO: Scroll to bottom


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
    # Please note that this is the event handler (not an event!)
    def mousePressEvent(self, i_qmouseevent):
        self.mouse_pressed_signal.emit(i_qmouseevent, self.diary_entry_id)
