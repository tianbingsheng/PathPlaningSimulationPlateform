from PyQt5.QtWidgets import QDialog, QTableWidget, QLabel, QLineEdit,QPushButton,QTextEdit, QComboBox, QRadioButton, QGridLayout, QVBoxLayout, QHBoxLayout, QMessageBox, QFileDialog
from SimuEnv.template import *

class NewSceneDilog(QDialog):

    templateLable = QLabel()
    remarksLable = QLabel()
    StoreLable = QLabel()
    scaleLable = QLabel()
    scaleEdit = QLineEdit()
    okButton = QPushButton()
    cancelButton = QPushButton()
    templateLineEdit = QLineEdit()
    storeComboBox = QComboBox()
    textEdit = QTextEdit()
    PhysicsType =QRadioButton()
    PixelType = QRadioButton()

    pTemplate = Template()

    def __init__(self, pTemplate):
        super(NewSceneDilog, self).__init__()
        self.pTemplate = pTemplate
        self.setWindowTitle('增加场景模板')
        mainlayout = QVBoxLayout()

        hblayout = QHBoxLayout()
        self.templateLable = QLabel('模板名称', self)
        self.templateLineEdit = QLineEdit(self)
        hblayout.addWidget(self.templateLable, 1)
        hblayout.addWidget(self.templateLineEdit, 3)
        mainlayout.addLayout(hblayout)

        hblayout = QHBoxLayout()
        self.PhysicsType = QRadioButton('物理坐标模式')
        self.PixelType = QRadioButton('像素坐标模式')
        self.PixelType.setChecked(True)
        hblayout.addWidget(self.PhysicsType, 1)
        hblayout.addWidget(self.PixelType, 2)
        mainlayout.addLayout(hblayout)

        hblayout = QHBoxLayout()
        self.scaleLable = QLabel('比例尺：像素/米', self)
        self.scaleLable.setVisible(self.PhysicsType.isCheckable())
        self.scaleEdit = QLineEdit(self)
        # self.scaleEdit.setValidator(QDoubleValidator)
        self.scaleEdit.setText('25')
        self.scaleEdit.setVisible(self.PhysicsType.isCheckable())
        hblayout.addWidget(self.scaleLable, 1)
        hblayout.addWidget(self.scaleEdit, 2)
        mainlayout.addLayout(hblayout)

        hblayout = QHBoxLayout()
        self.okButton = QPushButton('确定')
        self.cancelButton = QPushButton('取消')
        hblayout.addStretch()
        hblayout.addWidget(self.okButton)
        hblayout.addWidget(self.cancelButton)
        mainlayout.addLayout(hblayout)
        self.setLayout(mainlayout)
        self.createConnections()
        self.okButton.setFocus()

    def createConnections(self):

        self.okButton.clicked.connected(self.slotOKButtonDown)
        self.cancelButton.clicked.connected(self.slotCancelButton)
        self.PhysicsType.toggled.connected(self.slotSetUnHidden)

    def slotSetUnHidden(self):

        if self.PhysicsType.isChecked():
            self.scaleLable.setVisible(True)
            self.scaleEdit.setVisible(True)
        else:
            self.scaleLable.setVisible(False)
            self.scaleEdit.setVisible(False)

    def slotOKButtonDown(self):

        if self.templateLineEdit.text() == '':
            QMessageBox.information(self, '提示', '模板名不能为空')
            return
        self.pTemplate.setTemplateName(self.templateLineEdit.text())
        self.pTemplate.setRemark(self.textEdit.toPlainText())
        if self.PixelType.isChecked():
            self.pTemplate.setMode(Template.MODE_PIXEL)
        else:
            self.pTemplate.setMode(Template.MODE_PHYSIC)
        self.pTemplate.setScale(self.scaleEdit.text())

    def slotCancelButton(self):

        self.templateLineEdit.clear()
        self.textEdit.clear()
        self.PixelType.setChecked(True)
        self.scaleEdit.setText('25')
        self.close()