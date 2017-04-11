from PyQt5 import QtWidgets
from PyQt5 import QtGui
from PyQt5 import QtCore


class WisdomCompositeWidget(QtWidgets.QWidget):

    def __init__(self):
        super().__init__()

        self.qtreewidget = QtWidgets.QTreeWidget()
        vbox = QtWidgets.QVBoxLayout()
        vbox.addWidget(self.qtreewidget)
        self.setLayout(vbox)

        self.qtreewidget.setColumnCount(2)
        self.qtreewidget.setHeaderLabels(["Wisdom"])
        self.qtreewidget.setItemsExpandable(True)

        efforts_qtwi = QtWidgets.QTreeWidgetItem(self.qtreewidget, ["Four Right Efforts"])
        efforts_first_qtwi = QtWidgets.QTreeWidgetItem(efforts_qtwi, ["First"])
        efforts_second_qtwi = QtWidgets.QTreeWidgetItem(efforts_qtwi, ["Second"])

        self.qtreewidget.setItemWidget(efforts_first_qtwi, 1, QtWidgets.QPushButton("Filter"))

        four_est_mindfulness_qtwi = QtWidgets.QTreeWidgetItem(self.qtreewidget, ["Four Est. of Mindfulness"])
        four_est_mindfulness_body_qtwi = QtWidgets.QTreeWidgetItem(four_est_mindfulness_qtwi, ["Body"])
        four_est_mindfulness_feelings_qtwi = QtWidgets.QTreeWidgetItem(four_est_mindfulness_qtwi, ["Feelings"])
        four_est_mindfulness_mind_qtwi = QtWidgets.QTreeWidgetItem(four_est_mindfulness_qtwi, ["Mind"])
        four_est_mindfulness_objects_qtwi = QtWidgets.QTreeWidgetItem(four_est_mindfulness_qtwi, ["Objects of Mind"])

        four_immeasurable_minds_qtwi = QtWidgets.QTreeWidgetItem(self.qtreewidget, ["Four Immeasurable Minds"])
        four_immeasurable_kindness_qtwi = QtWidgets.QTreeWidgetItem(four_immeasurable_minds_qtwi, ["Loving Kindness"])
        four_immeasurable_compassion_qtwi = QtWidgets.QTreeWidgetItem(four_immeasurable_minds_qtwi, ["Compassion"])
        four_immeasurable_joy_qtwi = QtWidgets.QTreeWidgetItem(four_immeasurable_minds_qtwi, ["Sympathetic Joy"])
        four_immeasurable_equanimity_qtwi = QtWidgets.QTreeWidgetItem(four_immeasurable_minds_qtwi, ["Equanimity"])

        noble_eightfold_path_qtwi = QtWidgets.QTreeWidgetItem(self.qtreewidget, ["Noble Eightfold Path"])
        noble_eightfold_path_view_qtwi = QtWidgets.QTreeWidgetItem(noble_eightfold_path_qtwi, ["Right View"])
        noble_eightfold_path_thinking_qtwi = QtWidgets.QTreeWidgetItem(noble_eightfold_path_qtwi, ["Right Thinking"])
        noble_eightfold_path_speech_qtwi = QtWidgets.QTreeWidgetItem(noble_eightfold_path_qtwi, ["Right Speech"])
        noble_eightfold_path_action_qtwi = QtWidgets.QTreeWidgetItem(noble_eightfold_path_qtwi, ["Right Action"])
        noble_eightfold_path_livelihood_qtwi = QtWidgets.QTreeWidgetItem(noble_eightfold_path_qtwi, ["Right Livelihood"])
        noble_eightfold_path_effort_qtwi = QtWidgets.QTreeWidgetItem(noble_eightfold_path_qtwi, ["Right Effort (Diligence)"])
        noble_eightfold_path_mindfulness_qtwi = QtWidgets.QTreeWidgetItem(noble_eightfold_path_qtwi, ["Right Mindfulness"])
        noble_eightfold_path_concentration_qtwi = QtWidgets.QTreeWidgetItem(noble_eightfold_path_qtwi, ["Right Concentration"])

        four_noble_truths_qtwi = QtWidgets.QTreeWidgetItem(self.qtreewidget, ["Four Noble Truths"])
        four_noble_truths_suffering_qtwi = QtWidgets.QTreeWidgetItem(four_noble_truths_qtwi, ["Suffering"])
        four_noble_truths_causes_qtwi = QtWidgets.QTreeWidgetItem(four_noble_truths_qtwi, ["Causes of Suffering"])
        four_noble_truths_cessation_qtwi = QtWidgets.QTreeWidgetItem(four_noble_truths_qtwi, ["Cessation of Suffering"])
        four_noble_truths_path_qtwi = QtWidgets.QTreeWidgetItem(four_noble_truths_qtwi, ["Path to the Cessaction of Suffering"])

        self.qtreewidget.expandAll()
        self.qtreewidget.resizeColumnToContents(0)
        self.qtreewidget.resizeColumnToContents(1)

        self.qtoolbox = QtWidgets.QToolBox()

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
