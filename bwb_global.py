
"""
Module comments:
Global vars are used for storing some of the global application states. Please don't use global vars for
storing other types of values
"""


from PyQt5 import QtWidgets
from PyQt5 import QtCore
from PyQt5 import QtGui

import enum

import bwb_model


class ViewEnum(enum.Enum):
    diary_daily_overview = 0
    journal_monthly_view = 1


active_view_viewenum = ViewEnum.diary_daily_overview
active_date_qdate = QtCore.QDate.currentDate()
active_journal_id_it = 1  # -TODO: Change this


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
