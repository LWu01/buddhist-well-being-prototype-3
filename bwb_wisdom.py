from PyQt5 import QtWidgets
from PyQt5 import QtGui
from PyQt5 import QtCore


class WisdomCompositeWidget(QtWidgets.QWidget):
    time_of_day_state_changed_signal = QtCore.pyqtSignal()

    def __init__(self):
        super().__init__()

        self.qtoolbox = QtWidgets.QToolBox()
        vbox = QtWidgets.QVBoxLayout()
        vbox.addWidget(self.qtoolbox)
        self.setLayout(vbox)

        self.four_est_mindfulness_qlw = QtWidgets.QListWidget()
        self.four_est_mindfulness_qlw.addItems(["Body", "Feelings", "Mind", "Objects of Mind"])
        self.qtoolbox.addItem(self.four_est_mindfulness_qlw, "Four Est. of Mindfulness")

        self.four_immeasurable_minds_qlw = QtWidgets.QListWidget()
        self.four_immeasurable_minds_qlw.addItems(["Loving Kindness", "Compassion", "Sympathetic Joy", "Equanimity"])
        self.qtoolbox.addItem(self.four_immeasurable_minds_qlw, "Four Immeasurable Minds")

        self.noble_eightfold_path_qlw = QtWidgets.QListWidget()
        self.noble_eightfold_path_qlw.addItems(
            ["Right View", "Right Thinking (Intention)", "Right Speech", "Right Action",
             "Right Livelihood", "Right Diligence (Effort)", "Right Mindfulness", "Right Concentration"])
        self.qtoolbox.addItem(self.noble_eightfold_path_qlw, "Noble Eightfold Path")

        self.four_noble_truths_qlw = QtWidgets.QListWidget()
        self.four_noble_truths_qlw.addItems(
            ["Suffering", "Causes of Suffering", "Cessation of Suffering", "Path to the Cessaction of Suffering"])
        self.qtoolbox.addItem(self.four_noble_truths_qlw, "Four Noble Truths")

        self.householder_wellbeing_qlw = QtWidgets.QListWidget()
        self.householder_wellbeing_qlw.addItems(["Faith", "Virtue", "Generosity", "Wisdom"])
        self.qtoolbox.addItem(self.householder_wellbeing_qlw, QtGui.QIcon("icon.png"),
            "Spiritual Progress for Householders")

        self.factors_awakening_qlw = QtWidgets.QListWidget()
        self.factors_awakening_qlw.addItems(["Mindfulness", "Investigation of Mind Objects", "Energy",
            "Joy", "Tranquility", "Concentration", "Equanimity"])
        self.qtoolbox.addItem(self.factors_awakening_qlw, "Seven Factors of Awakening")

        self.powers_qlw = QtWidgets.QListWidget()
        self.powers_qlw.addItems(["Faith", "Diligence (Effort)", "Mindfulness",
            "Concentration", "Insight / Understanding / Wisdom"])
        self.qtoolbox.addItem(self.powers_qlw, "<b>Five Powers</b>")
