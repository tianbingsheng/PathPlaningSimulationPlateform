from SimuEnv.scene import *
from SimuEnv.sysinclude import *

from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

class pathEditDialog(QDialog):

    m_pPathNameLablel = None
    m_pPathNameEdit = None
    m_pStartLabel = None
    m_pStartCBox = None
    m_pEndLabel = None
    m_pEndCBox = None
    m_pOKButton = None
    m_pCancelButton = None
    m_pMainLayout = None
    m_pMainWidget = None
    m_pButtonLayout =None
    m_pScene = None
    m_pView = None
    m_pSplitter = None
    m_pDialogLayout = None

    m_EORMap = {}
    m_obstacle = []
    m_occupied = []
    m_EsMap = {}

    def __init__(self):
        
        super(pathEditDialog, self).__init__()
        self.createUI()
        self.createConnections()

    def createUI(self):

        self.m_pPathNameLablel = QLabel('路径名称：')
        self.m_pPathNameEdit = QLineEdit()

        self.m_pStartLabel = QLabel('起始位置：')
        self.m_pStartCBox = QComboBox()
        self.m_pStartCBox.setCurrentIndex(-1)

        self.m_pEndLabel = QLabel('终止位置：')
        self.m_pEndCBox = QComboBox()
        self.m_pEndCBox.setCurrentIndex(-1)

        self.m_pOKButton = QPushButton('确定')
        self.m_pCancelButton = QPushButton('取消')

        self.m_pMainLayout = QGridLayout()
        self.m_pMainLayout.addWidget(self.m_pPathNameLablel, 0, 0, 1, 1)
        self.m_pMainLayout.addWidget(self.m_pPathNameEdit, 0, 1, 1, 1)
        self.m_pMainLayout.addWidget(self.m_pStartLabel, 1, 0, 1, 1)
        self.m_pMainLayout.addWidget(self.m_pStartCBox, 1, 1, 1, 1)
        self.m_pMainLayout.addWidget(self.m_pEndLabel, 2, 0, 1, 1)
        self.m_pMainLayout.addWidget(self.m_pEndCBox, 2, 1, 1, 1)

        self.m_pButtonLayout = QGridLayout()
        self.m_pButtonLayout.setColumnStretch(0, 1)
        self.m_pButtonLayout.setColumnStretch(1, 1)
        self.m_pButtonLayout.setColumnStretch(2, 1)
        self.m_pButtonLayout.setColumnStretch(3, 1)
        self.m_pButtonLayout.addWidget(self.m_pOKButton, 0, 1)
        self.m_pButtonLayout.addWidget(self.m_pCancelButton, 0, 2)
        self.m_pMainLayout.addLayout(self.m_pButtonLayout, 3, 0, 1, 2)

        self.m_pMainWidget = QWidget()
        self.m_pMainWidget.setLayout(self.m_pMainLayout)

        self.m_pView = QGraphicsView()
        self.m_pView.setRenderHint(QPainter.Antialiasing)
        self.m_pView.setCacheMode(QGraphicsView.CacheBackground)
        self.m_pView.setViewportUpdateMode(QGraphicsView.BoundingRectViewportUpdate)

        self.m_pSplitter = QSplitter(Qt.Horizontal)
        self.m_pSplitter.addWidget(self.m_pMainWidget)
        self.m_pSplitter.addWidget(self.m_pView)
        self.m_pSplitter.setStretchFactor(1, 1)

        self.m_pDialogLayout = QGridLayout()
        self.m_pDialogLayout.addWidget(self.m_pSplitter)
        self.setLayout(self.m_pDialogLayout)

        self.resize(800, 600)
        self.setWindowFlags(self.windowFlags()|Qt.WindowMaximizeButtonHint)

    def createConnections(self):

        self.m_pCancelButton.clicked.connect(self.slotCancelDialog)
        self.m_pOKButton.clicked.connect(self.slotOKDialog)
        # self.m_pStartCBox.currentIndexChanged[int].connect(self.slotSelectStartItem)
        # self.m_pEndCBox.currentIndexChanged[int].connect(self.slotSelectEndItem)

    def slotSelectStartItem(self):

        id = self.m_pStartCBox.itemData(self.m_pStartCBox.currentIndex())
        pEOR = self.m_EORMap.get(id)
        pEOR.setColor(Qt.green)
        pEOR.scene().update()
        # self.defalutESColor(Qt.red)

        # if not pEOR:
        #     pEOR.setColor(Qt.green)
        #     pEOR.scene().update()

    def slotSelectEndItem(self):

        id = self.m_pEndCBox.itemData(self.m_pEndCBox.currentIndex())
        pEOR = self.m_EORMap.get(id)
        pEOR.setColor(Qt.red)
        pEOR.scene().update()
        # self.defalutESColor(Qt.green)

        # if not pEOR:
        #     pEOR.setColor(Qt.red)
        #     pEOR.scene().update()

    def slotCancelDialog(self):

        self.reject()
        self.close()

    def defalutESColor(self, color):

        for pEOR in list(self.m_EORMap.values()):

            if pEOR.getColor() != color:
                pEOR.setColor(lightBlue)
                # pEOR.setColor(color)
                pEOR.scene().update()

    def slotOKDialog(self):

        if self.m_pStartCBox.currentIndex() == self.m_pEndCBox.currentIndex():
            QMessageBox.warning(self, '警告', '起点与终点不能相同！')
            return
        elif (self.m_pStartCBox.currentIndex() == -1) or (self.m_pEndCBox.currentIndex() == -1):
            QMessageBox.warning(self, '警告', '站位信息不能空！')
            return
        elif (self.m_pPathNameEdit.text() == ''):
            QMessageBox.warning(self, '警告', '路径名称不能为空！')
            return

        start_id = self.m_pStartCBox.itemData(self.m_pStartCBox.currentIndex())
        end_id = self.m_pEndCBox.itemData(self.m_pEndCBox.currentIndex())
        pStart_EOR = self.m_EORMap.get(start_id)
        pEnd_EOR = self.m_EORMap.get(end_id)
        pStart_ES = self.m_EsMap.get(start_id)
        pEnd_ES = self.m_EsMap.get(end_id)
        pStart_ES.setRotation(pStart_EOR.rotation())
        pEnd_ES.setRotation(pEnd_ES.rotation())
        self.accept()
        self.close()

    def getPathName(self):

        return self.m_pPathNameEdit.text()

    def getStartSite(self):

        return self.m_EsMap.get(self.m_pStartCBox.itemData(self.m_pStartCBox.currentIndex()))

    def getEndSite(self):

        return self.m_EsMap.get(self.m_pEndCBox.itemData(self.m_pEndCBox.currentIndex()))

    def setScene(self, pScene):

        self.m_pScene = Scene()

        for pItem in pScene.items():
            if pItem.data(Qt.UserRole) == ITEM_RECT:
                pRO = pItem
                pRO_ = RectObstacle(pRO.width(), pRO.height())
                self.m_pScene.addItem(pRO_)
                pRO_.setPos(pRO.pos())
                pRO_.setRotation(pRO.rotation())
                pRO_.setFlag(QGraphicsItem.ItemIsMovable, False)
                pRO_.setFlag(QGraphicsItem.ItemIsSelectable, False)
                self.m_obstacle.append(pRO_)
            elif pItem.data(Qt.UserRole) == ITEM_RECT_OCCUPIED:
                pRO = pItem
                pRO_ = RectOccupied(pRO.width(), pRO.height())
                self.m_pScene.addItem(pRO_)

                pRO_.setPos(pRO.pos())
                pRO_.setRotation(pRO.rotation())
                pRO_.setFlag(QGraphicsItem.ItemIsMovable, False)
                pRO_.setFlag(QGraphicsItem.ItemIsSelectable, False)

                self.m_occupied.append(pRO_)
            elif pItem.data(Qt.UserRole) == ITEM_ECLIPSE:
                pEO = pItem
                pEO_ = EclipseObstacle(pEO.radiusX(), pEO.radiusY())
                self.m_pScene.addItem(pEO_)
                pEO_.setPos(pEO.pos())
                pEOR_.setRotation(pEO.rotation())
                pEO_.setFlag(QGraphicsItem.ItemIsMovable, False)
                pEO_.setFlag(QGraphicsItem.ItemIsSelectable, False)
                self.m_obstacle.append(pEO_)
            elif pItem.data(Qt.UserRole) == ITEM_POLYGON:
                pPO = pItem
                pPO_ = PolygonObstacle(pPO.polygonF())
                self.m_pScene.addItem(pPO_)
                pPO_.setPos(pPO.pos())
                pPO_.setRotation(pPO.rotation())
                pPO_.setFlag(QGraphicsItem.ItemIsMovable, False)
                pPO_.setFlag(QGraphicsItem.ItemIsSelectable, False)
                # self.m_pScene.addItem(pPO_)
                self.m_obstacle.append(pPO_)
            elif pItem.data(Qt.UserRole) == ITEM_POLYGON_EDGE:
                pPEO = pItem
                pPEO_ = PolygonEdgeObstacle(pPEO.polygonF())
                self.m_pScene.addItem(pPEO_)
                pPEO_.setPos(pPEO.pos())
                pPEO_.setFlag(QGraphicsItem.ItemIsMovable, False)
                pPEO_.setFlag(QGraphicsItem.ItemIsSelectable, False)
                # self.m_pScene.addItem(pPEO_)
                self.m_obstacle.append(pPEO_)
            elif pItem.data(Qt.UserRole) == ITEM_ECLIPSE_SITE:
                pES = pItem
                pEOR_ = EclipseObstacle_Rotation(pES.radiusX(), pES.radiusY())
                self.m_pScene.addItem(pEOR_)
                pEOR_.setPos(pES.pos())
                pEOR_.setRotation(pES.rotation())
                pEOR_.setId(pES.id())
                self.m_obstacle.append(pEOR_)
                self.m_EORMap[pEOR_.id()] = pEOR_
                self.m_EsMap[pES.id()] = pES

        self.m_pView.setScene(self.m_pScene)
        sizes = [200, 800]
        self.m_pSplitter.setSizes(sizes)
        self.setStartEndInfo(self.m_EORMap)


    def setStartEndInfo(self, eorMap):

        sorted(eorMap)

        for key, value in eorMap.items():
            itemName = '站位'
            itemName += str(key)
            self.m_pStartCBox.addItem(itemName, key)
            self.m_pEndCBox.addItem(itemName, key)

        if len(list(eorMap.keys())) > 1:
            self.m_pStartCBox.setCurrentIndex(0)
            self.slotSelectStartItem()

            self.m_pEndCBox.setCurrentIndex(1)
            self.slotSelectEndItem()





if __name__ == '__main__':
    app = QApplication(sys.argv)
    print('0000000000000000000')
    # main = pathEditDialog()
    print('1111111111111111111')
    # main.showMaximized()
    sys.exit(app.exec_())





