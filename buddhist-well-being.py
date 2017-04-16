import sqlite3
import sys

import PyQt5
from bwb import bwb_model
from PyQt5 import Qt
from PyQt5 import QtCore
from PyQt5 import QtGui
from PyQt5 import QtWidgets

from bwb import bwb_window

######################
#
# Main
#
######################

BWB_APPLICATION_VERSION_STR = "prototype 3"
#BWB_APPLICATION_VERSION_INT = 1

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    main_window = bwb_window.WellBeingWindow()

    # System tray
    tray_icon = QtWidgets.QSystemTrayIcon(QtGui.QIcon("icon.png"), app)
    tray_menu = QtWidgets.QMenu()
    tray_restore_action = QtWidgets.QAction("Restore")
    tray_restore_action.triggered.connect(main_window.show)
    tray_menu.addAction(tray_restore_action)
    tray_quit_action = QtWidgets.QAction("Quit")
    tray_quit_action.triggered.connect(sys.exit)
    tray_menu.addAction(tray_quit_action)
    tray_icon.setContextMenu(tray_menu)
    tray_icon.show()

    print("===== Starting Buddhist Well-Being - prototype 3 =====")
    print("Python version: " + str(sys.version))
    print("SQLite version: " + str(sqlite3.sqlite_version))
    print("PySQLite (Python module) version: " + str(sqlite3.version))
    print("Qt version: " + str(QtCore.qVersion()))
    print("PyQt (Python module) version: " + str(PyQt5.Qt.PYQT_VERSION_STR))
    print("Buddhist Well-Being application version: " + str(BWB_APPLICATION_VERSION_STR))
    db_conn = bwb_model.DbHelperM.get_db_connection()
    print("Buddhist Well-Being database schema version: " + str(bwb_model.get_schema_version(db_conn)))
    print("=====")

    sys.exit(app.exec_())
