import bwb_model
from PyQt5 import QtWidgets
from PyQt5 import QtCore
from PyQt5 import QtGui
import sched
import time
import datetime
import threading

ID_NOT_SET = -1
BUTTON_WIDTH_IT = 28


class PracticeCompositeWidget(QtWidgets.QWidget):
    time_of_day_state_changed_signal = QtCore.pyqtSignal()

    def __init__(self):
        super().__init__()

        self.id_it = ID_NOT_SET
        self.scheduler = sched.scheduler(time.time, time.sleep)

        vbox = QtWidgets.QVBoxLayout()
        self.setLayout(vbox)
        vbox.setAlignment(QtCore.Qt.AlignTop)

        # ..for details
        ### self.details_ll = QtWidgets.QLabel("-----")
        ### self.details_ll.setWordWrap(True)
        self.question_ll = QtWidgets.QLabel("<h4>Question</h4>")
        vbox.addWidget(self.question_ll)
        self.question_le = QtWidgets.QLineEdit()
        self.question_le.textChanged.connect(self.on_question_text_changed)
        vbox.addWidget(self.question_le)

        self.time_of_day_label = QtWidgets.QLabel("<h4>Time of day</h4>")
        vbox.addWidget(self.time_of_day_label)

        hbox = QtWidgets.QHBoxLayout()
        vbox.addLayout(hbox)
        self.time_of_day_active_label = QtWidgets.QLabel("Active?")
        hbox.addWidget(self.time_of_day_active_label)
        self.time_of_day_active_qcb = QtWidgets.QCheckBox()
        self.time_of_day_active_qcb.stateChanged.connect(self.on_time_of_day_statechanged)
        hbox.addWidget(self.time_of_day_active_qcb)

        self.time_of_day_timeedit = QtWidgets.QTimeEdit()
        self.time_of_day_timeedit.setDisplayFormat("HH")
        self.time_of_day_timeedit.timeChanged.connect(self.on_time_of_day_changed)
        hbox.addWidget(self.time_of_day_timeedit)

        days_in_week_hbox = QtWidgets.QHBoxLayout()
        vbox.addLayout(days_in_week_hbox)

        self.monday_qpb = QtWidgets.QPushButton("Mo")
        self.monday_qpb.setCheckable(True)
        self.monday_qpb.setFixedWidth(BUTTON_WIDTH_IT)
        days_in_week_hbox.addWidget(self.monday_qpb)
        self.tuesday_qpb = QtWidgets.QPushButton("Tu")
        self.tuesday_qpb.setCheckable(True)
        self.tuesday_qpb.setFixedWidth(BUTTON_WIDTH_IT)
        days_in_week_hbox.addWidget(self.tuesday_qpb)
        self.wednesday_qpb = QtWidgets.QPushButton("We")
        self.wednesday_qpb.setCheckable(True)
        self.wednesday_qpb.setFixedWidth(BUTTON_WIDTH_IT)
        days_in_week_hbox.addWidget(self.wednesday_qpb)
        self.thursday_qpb = QtWidgets.QPushButton("Th")
        self.thursday_qpb.setCheckable(True)
        self.thursday_qpb.setFixedWidth(BUTTON_WIDTH_IT)
        days_in_week_hbox.addWidget(self.thursday_qpb)
        self.friday_qpb = QtWidgets.QPushButton("Fr")
        self.friday_qpb.setCheckable(True)
        self.friday_qpb.setFixedWidth(BUTTON_WIDTH_IT)
        days_in_week_hbox.addWidget(self.friday_qpb)
        self.saturday_qpb = QtWidgets.QPushButton("Sa")
        self.saturday_qpb.setCheckable(True)
        self.saturday_qpb.setFixedWidth(BUTTON_WIDTH_IT)
        days_in_week_hbox.addWidget(self.saturday_qpb)
        self.sunday_qpb = QtWidgets.QPushButton("Su")
        self.sunday_qpb.setCheckable(True)
        self.sunday_qpb.setFixedWidth(BUTTON_WIDTH_IT)
        days_in_week_hbox.addWidget(self.sunday_qpb)

        """
        button_group = QtWidgets.QButtonGroup()
        button_group.setExclusive(False)
        button_group.addButton(self.monday_qpb)
        button_group.addButton(self.tuesday_qpb)
        vbox.addWidget(button_group)
        """

    def on_time_of_day_statechanged(self, i_new_checked_state):
        self.update_db_time()

    def on_time_of_day_changed(self, i_qtime):
        self.update_db_time()

    def update_db_time(self):
        if self.id_it == ID_NOT_SET:
            return
        qtime = self.time_of_day_timeedit.time()
        if self.time_of_day_active_qcb.checkState() == QtCore.Qt.Checked:
            bwb_model.PracticesM.update_time_of_day(self.id_it, qtime.hour())

            # Set a scheduled task
            practice = bwb_model.PracticesM.get(self.id_it)
            self.set_reminder(qtime.hour(), practice.title)
        else:
            bwb_model.PracticesM.update_time_of_day(self.id_it, bwb_model.TIME_NOT_SET)
        self.time_of_day_state_changed_signal.emit()

    def set_reminder(self, i_hour_it, i_practice_title_sg):
        self.schedule_thread = threading.Thread(target=self.background_function, args=(i_hour_it, i_practice_title_sg), daemon=True)
        self.schedule_thread.start()

    def background_function(self, i_hour_it, i_practice_title_sg):
        now = time.time()
        reminder_time_qdatetime = QtCore.QDateTime.currentDateTime()
        reminder_time_qdatetime.setTime(QtCore.QTime(i_hour_it, 50))
        reminder_time_in_seconds_it = reminder_time_qdatetime.toMSecsSinceEpoch() / 1000
        print("reminder_time_in_seconds_it = " + str(reminder_time_in_seconds_it))
        self.scheduler.enterabs(reminder_time_in_seconds_it + 10, 1, self.popup_function, (i_practice_title_sg,))
        # -Several events can be scheduled, (the enterabs function adds an event rather than replacing)
        self.scheduler.run()  # blocking=False

    def popup_function(self, i_string):
        message_box = QtWidgets.QMessageBox.information(None, i_string, (i_string))


    def on_question_text_changed(self):
        if self.id_it == ID_NOT_SET:
            return
        bwb_model.PracticesM.update_question_text(
            self.id_it,
            self.question_le.text().strip()
        )

    def change_practice(self, i_practice_id_it):
        self.id_it = i_practice_id_it  # storing the id locally
        self.update_gui()

    def update_gui(self):
        time_of_day_cb_was_blocked_bl = self.time_of_day_active_qcb.blockSignals(True)
        time_of_day_timeedit_was_blocked_bl = self.time_of_day_timeedit.blockSignals(True)

        practice = bwb_model.PracticesM.get(self.id_it)
        ##self.details_ll.setText(practice.description)
        self.question_le.setText(practice.question)
        qtime = QtCore.QTime(0, 0)
        if practice.time_of_day != bwb_model.TIME_NOT_SET:
            qtime = QtCore.QTime(practice.time_of_day, 0)
            self.time_of_day_active_qcb.setCheckState(QtCore.Qt.Checked)
        else:
            self.time_of_day_active_qcb.setCheckState(QtCore.Qt.Unchecked)
        self.time_of_day_timeedit.setTime(qtime)  # move to update_gui???

        self.time_of_day_active_qcb.blockSignals(time_of_day_cb_was_blocked_bl)
        self.time_of_day_timeedit.blockSignals(time_of_day_timeedit_was_blocked_bl)
