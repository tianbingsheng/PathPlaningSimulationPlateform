import matplotlib
matplotlib.use('Qt5Agg')
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir)))
from SimuEnv.mainwindow import MainWindow
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
import numpy as np
import itertools
import copy

import matplotlib.pyplot as plt
import math

class SimulationPara:

    def __init__(self):
        self.out_d = None
        self.in_d = None
        self.out_cl = None
        self.in_cl = None
        self.is_finished = False

class SimulationEnv1(MainWindow):

    def __init__(self):
        super().__init__()
        self.current_value = []
        self.next_value = []
        self.simulationPara = []

        self.learn_action1 = QAction('学习参数', self)
        self.learn_action1.triggered.connect(self.slot_startlearningPara)
        self.m_pFileMenu.addAction(self.learn_action1)
        self.m_pToolBar.addAction(self.learn_action1)





    def slot_startlearningPara(self):
        pass




if __name__ == '__main__':
    app = QApplication(sys.argv)
    print('0000000000000000000')
    env1 = SimulationEnv1()
    print('1111111111111111111')
    env1.showMaximized()
    sys.exit(app.exec_())