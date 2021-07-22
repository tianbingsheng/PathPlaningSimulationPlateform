import sys
from PyQt5.Qt import Qt
from PyQt5.QtWidgets import QWidget, QTableWidget, QTableWidgetItem, QHeaderView, QHBoxLayout
from SimuEnv.scene import Obstacle, Pair

class AttributeWidget(QWidget):

    pTabWidget = QTableWidget()
    def __init__(self):

        super(AttributeWidget, self).__init__()
        self.setupUI()

    def setupUI(self):

        pTabWidget = QTableWidget()
        pTabWidget.setColumnCount(2)
        headers = ['属性', '值']
        for i in range(len(headers)):
            item = QTableWidgetItem(headers[i])
            pTabWidget.setHorizontalHeaderItem(i, item)
        pTabWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        mainLayout = QHBoxLayout()
        mainLayout.addWidget(pTabWidget)
        self.setLayout(mainLayout)

    def slotShowAttribute(self, pObstacle):

        list = []
        self.pTabWidget.setRowCount(len(list))
        for i in range(len(list)):
            key = QTableWidgetItem(list[i].first)
            value = QTableWidgetItem(list[i].second)
            key.setFlags(key.flags() and (Qt.ItemIsEditable))
            value.setFlags(key.flags() and (Qt.ItemIsEditable))
            self.pTabWidget.setItem(i, 0, key)
            self.pTabWidget.setItem(i, 1, value)



