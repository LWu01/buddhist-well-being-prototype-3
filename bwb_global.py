
from PyQt5 import QtWidgets
from PyQt5 import QtCore
from PyQt5 import QtGui

import bwb_model


active_date_qdate = QtCore.QDate.currentDate()



def qdate_to_unixtime(i_qdate: QtCore.QDate) -> int:
    qdatetime = QtCore.QDateTime(i_qdate)
    unixtime_it = qdatetime.toMSecsSinceEpoch() // 1000
    return unixtime_it


"""
def get_active_date():
    global active_date
    return active_date
def set_active_date(i_qdate):
    global active_date
    active_date = i_qdate
"""
