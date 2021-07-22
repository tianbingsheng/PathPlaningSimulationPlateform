import sys
import os
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtXml import QDomDocument, QDomElement
from PyQt5.QtGui import *

# from SimuEnv.AllPremise import *

# #from SimuEnv import sysinclude, scene, scenewidget, template, patheditdialog, obstacle, util, lineitem, anchoritem
# #from SimuEnv import scene
# #from SimuEnv import scenewidget
# from SimuEnv.template import *
from SimuEnv.sysinclude import *
from SimuEnv.scene import *
from SimuEnv.patheditdialog import *
# from SimuEnv.obstacle import *
from SimuEnv.path import *
from SimuEnv.util import *


class TreeItem(QTreeWidgetItem):

    def __init__(self, itemName, pPath):
        super(TreeItem, self).__init__()
        self.setText(0, itemName)
        self.m_pPaths = pPath

    def getPath(self):
        return self.m_pPaths


class MainWindow(QMainWindow):


    m_siteMap = {}
    m_pView = None
    m_pScene = pyqtSignal()


    def __init__(self):

        super(MainWindow, self).__init__()
        super(QWidget, self).__init__()
        self.m_pTemplate = Template()
        self.m_pBoundary = None
        self.tempTreeItem = None
        self.createUI()
        self.createConnections()

    def createUI(self):

        self.createMenuBar()
        self.createToolBar()
        self.createToolBox()
        self.createScene()
        self.createPathTreeWidget()
        self.createPathParaWidget()
        self.createCentralWidget()

    def createMenuBar(self):

        self.m_pFileMenu = QMenu('文件')
        self.m_pHelpMenu = QMenu('帮助')

        self.m_pFileMenu.addAction('新建')
        self.m_pFileMenu.addAction('打开')
        self.m_pFileMenu.addAction('保存')
        self.m_pFileMenu.addAction('清空窗口')
        self.m_pFileMenu.addSeparator()
        self.m_pFileMenu.addAction('最近打开列表')
        self.m_pFileMenu.addSeparator()
        self.m_pFileMenu.addAction('清除最近打开列表')
        self.m_pFileMenu.addSeparator()
        self.m_pFileMenu.addAction('退出')

        self.m_pHelpMenu.addAction('关于')

        self.menuBar().addMenu(self.m_pFileMenu)
        self.menuBar().addMenu(self.m_pHelpMenu)

    def createToolBar(self):

        self.m_pToolBar = QToolBar()
        self.m_pToolBar.addAction(self.findActionbyString('新建'))
        self.m_pToolBar.addAction(self.findActionbyString('打开'))
        self.m_pToolBar.addAction(self.findActionbyString('保存'))
        self.m_pToolBar.addAction(self.findActionbyString('清空窗口'))
        self.m_pToolBar.addSeparator()
        self.m_pToolBar.addAction(self.findActionbyString('退出'))

        self.addToolBar(self.m_pToolBar)

    def createToolBox(self):

        self.m_pToolBox = QToolBox()
        self.m_pButtonGroup = QButtonGroup()
        self.m_pButtonGroup.setExclusive(False)

        pItemWidget = QWidget()
        pLayout = QVBoxLayout()
        pLayout.addWidget(self.createCellWidget('多边形边界', ITEM_POLYGON_EDGE))
        pItemWidget.setLayout(pLayout)
        self.m_pToolBox.addItem(pItemWidget, '边界')

        pItemWidget = QWidget()
        pLayout = QVBoxLayout()
        pLayout.addWidget(self.createCellWidget('矩形', ITEM_RECT_OCCUPIED))
        pItemWidget.setLayout(pLayout)
        self.m_pToolBox.addItem(pItemWidget, '站位')

        pItemWidget = QWidget()
        pLayout = QVBoxLayout()
        pLayout.addWidget(self.createCellWidget('矩形', ITEM_RECT))
        pLayout.addWidget(self.createCellWidget('椭圆', ITEM_ECLIPSE))
        pLayout.addWidget(self.createCellWidget('多边形', ITEM_POLYGON))
        pItemWidget.setLayout(pLayout)
        self.m_pToolBox.addItem(pItemWidget, '障碍物')

        pItemWidget = QWidget()
        pLayout = QVBoxLayout()
        pLayout.addWidget(self.createCellWidget('起/终点标志', ITEM_ECLIPSE_SITE))
        pItemWidget.setLayout(pLayout)
        self.m_pToolBox.addItem(pItemWidget, '起/终点')


    def createCellWidget(self, text, itemType):

        icon = QIcon(self.makeIcon(itemType))
        pButton = QToolButton()
        pButton.setIcon(icon)
        pButton.setIconSize(QSize(100, 100))
        pButton.setCheckable(True)
        self.m_pButtonGroup.addButton(pButton, int(itemType))

        pLayout = QGridLayout()
        pLayout.addWidget(pButton, 0, 0, Qt.AlignCenter)

        pWidget = QGroupBox(text)
        pWidget.setAlignment(Qt.AlignCenter)
        pWidget.setLayout(pLayout)

        return pWidget


    def makeIcon(self, type):

        pixmap = QPixmap(300, 300)
        pixmap.fill(Qt.transparent)
        painter = QPainter(pixmap)
        painter.setPen(QPen(Qt.black, 8))
        painter.translate(150, 150)
        if type == ITEM_RECT:
            # painter.setPen(QPen(Qt.DotLine))
            rect = QRect(-100, -100, 200, 200)
            painter.drawRect(rect)
        elif type == ITEM_RECT_OCCUPIED:
            rect = QRect(-100, -100, 200, 200)
            painter.drawRect(rect)
        elif type == ITEM_ECLIPSE:
            painter.drawEllipse(QPointF(0.0, 0.0), 100, 50)
        elif type == ITEM_POLYGON:
            points1 = [QPoint(-50, -90), QPoint(50, -90), QPoint(100, 0), QPoint(50, 90), QPoint(-50, 90), QPoint(-100, 0)]
            painter.drawPolygon(QPolygon(points1))
        elif type == ITEM_POLYGON_EDGE:
            points2 = [QPoint(-90, -80), QPoint(90, -80), QPoint(120, -40), QPoint(150, -40), QPoint(150, 40), QPoint(120, 40), QPoint(100, 80), QPoint(-115, 80), QPoint(-115, 70), QPoint(-120, 70), QPoint(-120, -60),QPoint(-110, -60)]
            painter.drawPolygon(QPolygon(points2))
        elif type == ITEM_ECLIPSE_SITE:
            painter.drawEllipse(QPointF(0.0, 0.0), 100, 100)

        return pixmap


    def createPathTreeWidget(self):

        self.m_pAddPathAction = QAction('添加路径')


        self.m_pPathTreeWidget = QTreeWidget()
        self.m_pPathTreeWidget.headerItem().setHidden(True)

        self.m_pPathTreeRootItem = QTreeWidgetItem()
        self.m_pPathTreeRootItem.setText(0, '路径列表')
        self.m_pPathTreeWidget.addTopLevelItem(self.m_pPathTreeRootItem)

    def createPathParaWidget(self):

        self.pathParaWidget = QWidget()
        self.pPathNameLabel = QLabel('路径名称：')
        self.pPathNameValue = QLineEdit()
        self.pStartLabel = QLabel('起始位置：')
        self.pStartValue = QLineEdit()
        self.pEndLabel = QLabel('终止位置：')
        self.pEndValue = QLineEdit()

        self.pWeight1Label = QLabel('weight1长度权重：')
        self.pWeight1Edit = QLineEdit()
        self.pWeight2Label = QLabel('weight2站位权重：')
        self.pWeight2Edit = QLineEdit()
        self.pWeight3Label = QLabel('weight3曲率权重：')
        self.pWeight3Edit = QLineEdit()

        self.pOutdLabel = QLabel('出站位d值：')
        self.pOutdEdit = QLineEdit()
        self.pIndLabel = QLabel('入站位d值：')
        self.pIndEdit = QLineEdit()
        self.pOutclLabel= QLabel('出站位cl值：')
        self.pOutclEdit = QLineEdit()
        self.pInclLabel = QLabel('入站位cl值：')
        self.pInclEdit = QLineEdit()

        self.pOKButton = QPushButton('确定')
        self.pCancelButton = QPushButton('取消')

        self.pMainLayout = QGridLayout()
        self.pMainLayout.addWidget(self.pPathNameLabel, 0, 0, 1, 1)
        self.pMainLayout.addWidget(self.pPathNameValue, 0, 1, 1, 1)
        self.pMainLayout.addWidget(self.pStartLabel, 1, 0, 1, 1)
        self.pMainLayout.addWidget(self.pStartValue, 1, 1, 1, 1)
        self.pMainLayout.addWidget(self.pEndLabel, 2, 0, 1, 1)
        self.pMainLayout.addWidget(self.pEndValue, 2, 1, 1, 1)
        self.pMainLayout.addWidget(self.pWeight1Label, 3, 0, 1, 1)
        self.pMainLayout.addWidget(self.pWeight1Edit, 3, 1, 1, 1)
        self.pMainLayout.addWidget(self.pWeight2Label, 4, 0, 1, 1)
        self.pMainLayout.addWidget(self.pWeight2Edit, 4, 1, 1, 1)
        self.pMainLayout.addWidget(self.pWeight3Label, 5, 0, 1, 1)
        self.pMainLayout.addWidget(self.pWeight3Edit, 5, 1, 1, 1)
        self.pMainLayout.addWidget(self.pOutdLabel, 6, 0, 1, 1)
        self.pMainLayout.addWidget(self.pOutdEdit, 6, 1, 1, 1)
        self.pMainLayout.addWidget(self.pIndLabel, 7, 0, 1, 1)
        self.pMainLayout.addWidget(self.pIndEdit, 7, 1, 1, 1)
        self.pMainLayout.addWidget(self.pOutclLabel, 8, 0, 1, 1)
        self.pMainLayout.addWidget(self.pOutclEdit, 8, 1, 1, 1)
        self.pMainLayout.addWidget(self.pInclLabel, 9, 0, 1, 1)
        self.pMainLayout.addWidget(self.pInclEdit, 9, 1, 1, 1)

        self.pButtonLayout = QGridLayout()
        self.pButtonLayout.setColumnStretch(0, 1)
        self.pButtonLayout.setColumnStretch(1, 1)
        self.pButtonLayout.setColumnStretch(2, 1)
        self.pButtonLayout.setColumnStretch(3, 1)
        self.pButtonLayout.addWidget(self.pOKButton, 0, 1)
        self.pButtonLayout.addWidget(self.pCancelButton, 0, 2)

        self.pMainLayout.addLayout(self.pButtonLayout, 10, 0, 1, 2)
        self.pathParaWidget.setLayout(self.pMainLayout)



    def createCentralWidget(self):

        self.m_pTabWidget = QTabWidget()
        self.m_pTabWidget.addTab(self.m_pToolBox, '组件栏')
        self.m_pTabWidget.addTab(self.m_pPathTreeWidget, '路径列表')
        self.m_pTabWidget.addTab(self.pathParaWidget, '路径参数')

        self.m_pMainLayout = QHBoxLayout()
        self.m_pMainLayout.addWidget(self.m_pTabWidget, 1)
        self.m_pMainLayout.addWidget(self.m_pView,4 )

        self.m_pMainWidget = QWidget()
        self.m_pMainWidget.setLayout(self.m_pMainLayout)

        self.setCentralWidget(self.m_pMainWidget)

    def findActionbyString(self, string):

        for pAction1 in self.m_pFileMenu.actions():
            if pAction1.text() == string:
                return pAction1
        for pAction2 in self.m_pHelpMenu.actions():
            if pAction2.text() == string:
                return pAction2
        return None



    def createScene(self):

        self.m_pScene = Scene()
        self.m_pScene.setSceneRect(-1000, -1000, 2000, 2000)
        self.m_pView = SceneWidget(self.m_pScene)
        self.m_pView.setRenderHint(QPainter.Antialiasing)
        self.m_pView.setCacheMode(QGraphicsView.CacheBackground)
        self.m_pView.setViewportUpdateMode(QGraphicsView.BoundingRectViewportUpdate)
        self.m_pView.resize(400, 600)

    def createConnections(self):

        self.m_pButtonGroup.buttonClicked[int].connect(self.slotButtonGroupClicked)
        self.m_pScene.emitFinishInsert.connect(self.slotFinishInsert)
        self.m_pPathTreeWidget.itemPressed.connect(self.slotItemPressed)
        self.m_pAddPathAction.triggered.connect(self.slotAddPath)
        self.pOKButton.clicked.connect(self.slotOKPathPara)
        self.pCancelButton.clicked.connect(self.slotCancelPathPara)

        self.findActionbyString('退出').triggered.connect(self.close)
        self.findActionbyString('保存').triggered.connect(self.slotSave)
        self.findActionbyString('打开').triggered.connect(self.slotOpen)
        self.findActionbyString('清空窗口').triggered.connect(self.slotClear)


    def slotOpen(self):

        fileName = QFileDialog.getOpenFileName(self, '打开', '', 'xml(*.xml)')
        # fileName = ''.join(fileName2)
        fileName = fileName[0]
        if QFile.exists(fileName):
            isSuccess = self.readXMLFile(fileName)
            if isSuccess:
                QMessageBox.information(self, '提示', '读取文件成功')
            else:
                QMessageBox.warning(self, '警告', '读取文件失败')
        else:
            msg = QMessageBox()
            msg.setText('文件不存在')
            msg.exec()

    def slotSave(self):

        fileName = QFileDialog.getSaveFileName(self, '另存为', '', 'xml(*.xml)')
        fileName = fileName[0]
        if fileName == None:
            return False
        avaliableFile = ''.join(fileName)
        self.setPathWayPoints()
        isSuccess = self.writeXMLFile(avaliableFile)
        if not isSuccess:
            msg = QMessageBox()
            msg.setText('保存失败')
            msg.exec()
        else:
            msg = QMessageBox()
            msg.setText('保存成功')
            msg.exec()

    def readXMLFile(self, filePath):

        xmlFile = QFile(filePath)
        if not xmlFile.open(QIODevice.ReadOnly):
            print("the file can not be writen error:", xmlFile.errorString())
            return False
        domDocument = QDomDocument()
        res = domDocument.setContent(xmlFile, True)
        if not res[0]:
            xmlFile.close()
            print("parse error at Line:{0},Column:{1},error:{2}".format(res[2], res[3], res[1]))
            return False

        root = domDocument.documentElement()
        if root.tagName() != 'SceneDesignTemplate':
            return False
        self.m_pTemplate = Template()
        self.m_pTemplate.setTemplateName(root.attribute('name'))
        self.m_pTemplate.setRemark(root.attribute('remark'))
        self.m_pTemplate.setMode(root.attribute('mode'))
        self.m_pTemplate.setScale(root.attribute('scale'))

        child = root.firstChildElement()
        while not child.isNull():
            if child.tagName() == 'Boundary':
                self.readBoundary(child)
            elif child.tagName() == 'Barrier':
                self.readBarrier(child)
            elif child.tagName() == 'EclipseSite':
                self.readSite(child)
            elif child.tagName() == 'Occupied':
                self.readOccupied(child)
            elif child.tagName() == 'Path':
                self.readPath(child)
            child = child.nextSiblingElement()

        self.pStartValue.setText('站位' + str(self.m_pScene.m_StartEclipseSite.id_) + '(' + str(self.m_pScene.m_StartEclipseSite.pos().x()) + ' , ' + str(self.m_pScene.m_StartEclipseSite.pos().y()) + ')')
        self.pEndValue.setText('站位：' + str(self.m_pScene.m_EndEclipseSite.id_) + '(' + str(self.m_pScene.m_EndEclipseSite.pos().x()) + ' , ' + str(self.m_pScene.m_EndEclipseSite.pos().y()) + ')')

        return True

    def readPath(self, element):

        pPath = Path()
        pPath.setId(int(element.attribute('id')))
        pPath.setName(element.attribute('name'))
        self.m_pScene.m_pathName = element.attribute('name')
        self.pPathNameValue.setText(self.m_pScene.m_pathName)
        pPath.setColor(Util.long2Color(int(element.attribute('color'))))

        child = element.firstChildElement()
        while not child.isNull():
            if child.tagName() == 'StartPoint':
                id = int(child.attribute('eclipseSite_id'))
                pSite = self.m_siteMap.get(id)
                if not pSite:
                    QMessageBox.warning(self, '警告', pPath.getName()+':路径起点信息错误!')
                    continue
                pPath.setStartItem(pSite)
                self.m_pScene.m_StartEclipseSite = pSite
                # self.pStartValue.setText('站位' + str(self.m_pScene.m_StartEclipseSite.id_) + '(' + child.attribute('position_x') + ' , ' + child.attribute('position_y') + ')')
                angle = float(child.attribute('angle'))
                pPath.setStartPosAndAngle(pSite, angle)
            elif child.tagName() == 'EndPoint':
                id = int(child.attribute('eclipseSite_id'))
                pSite = self.m_siteMap.get(id)
                if not pSite:
                    QMessageBox.warning(self, '警告', pPath.getName() + ':路径终点信息错误!')
                    continue
                pPath.setEndItem(pSite)
                self.m_pScene.m_EndEclipseSite = pSite
                # self.pEndValue.setText('站位' + str(self.m_pScene.m_EndEclipseSite.id_) + '(' + child.attribute('position_x') + ' , ' + child.attribute('position_y') + ')')
                angle = float(child.attribute('angle'))
                pPath.setEndPosAndAngle(pSite, angle)
            elif child.tagName() == 'WayPoint':
                path = []
                node = child.firstChildElement()
                while not node.isNull():
                    point = WayPoint()
                    point.pos_ = Util.String2PointF(node.attribute('pos'))
                    point.radian_ = float(node.attribute('angle'))
                    path.append(point)
                    node = node.nextSiblingElement()
                pPath.setWayPoints(path)
            child = child.nextSiblingElement()

        self.pWeight1Edit.setText(str(0.4))
        self.pWeight2Edit.setText(str(0.3))
        self.pWeight3Edit.setText(str(0.3))
        self.pOutdEdit.setText(str(50.0))
        self.pIndEdit.setText(str(50.0))
        self.pOutclEdit.setText(str(100.0))
        self.pInclEdit.setText(str(100.0))

        self.m_pView.insertPath(pPath)
        pItem = TreeItem(pPath.getName(), pPath)
        self.m_pPathTreeRootItem.addChild(pItem)
        self.m_pPathTreeRootItem.setExpanded(True)

    def readSite(self, element):

        name = element.attribute('name')
        color = Util.long2Color(int(element.attribute('color')))
        px = float(element.attribute('position_x'))
        py = float(element.attribute('position_y'))
        rx = float(element.attribute('radius_x'))
        ry = float(element.attribute('radius_y'))
        rotation = float(element.attribute('rotation'))
        id = int(element.attribute('id'))

        pSite = EclipseSite(rx, ry)
        self.m_pScene.addItem(pSite)
        pSite.setRotation(rotation)
        pSite.setId(id)
        pSite.setColor(color)
        pSite.setName(name)
        pSite.setPos(px, py)
        pSite.setData(Qt.UserRole, ITEM_ECLIPSE_SITE)
        self.m_pScene.m_eclipseSiteList.append(pSite)
        # self.m_pScene.insertEclipseSiteItem(pSite)
        self.m_siteMap[id] = pSite

        # self.m_pScene.addItem(pSite)
        # self.m_pScene.insertEclipseSiteItem(pSite)

    def readBoundary(self, element):

        childs = element.childNodes()
        size = childs.size()
        vec = []
        for i in range(size):
            element = childs.at(i).toElement()
            vec.append(QPointF(float(element.attribute('x')), float(element.attribute('y'))))
        vecPolygon = QPolygonF(vec)
        self.m_pBoundary = PolygonEdgeObstacle(vecPolygon)
        # self.m_pScene.addItem(self.m_pBoundary)
        self.m_pScene.insertBoundary(self.m_pBoundary)

    def readBarrier(self, element):

        childs = element.childNodes()
        size = childs.size()
        for i in range(size):
            elementTemp = childs.at(i).toElement()
            pObstacle = None
            if elementTemp.tagName() == 'Rect':
                width = float(elementTemp.attribute('width'))
                height = float(elementTemp.attribute('height'))
                pObstacle = RectObstacle(width, height)
                pObstacle.setData(Qt.UserRole, ITEM_RECT)
            # elif element.tagName() == 'Rect_Occupied':
            #     width = element.attribute('width')
            #     height = element.attribute('height')
            #     pObstacle = RectOccupied(width, height)
            #     pObstacle.setData(Qt.UserRole, ITEM_RECT_OCCUPIED)
            elif elementTemp.tagName() == 'Polygon':
                childsTemp = elementTemp.childNodes()
                sizeTemp = childsTemp.size()
                vec = []
                for j in range(sizeTemp):
                    child = childsTemp.at(j).toElement()
                    vec.append(QPointF(float(child.attribute('x')), float(child.attribute('y'))))
                vecPolygonF = QPolygonF(vec)
                pObstacle = PolygonObstacle(vecPolygonF)
                pObstacle.setData(Qt.UserRole, ITEM_POLYGON)
            elif elementTemp.tagName() == 'Eclipse':
                radius_x = float(elementTemp.attribute('radius_x'))
                radius_y = float(elementTemp.attribute('radius_y'))
                pObstacle = EclipseObstacle(radius_x, radius_y)
                pObstacle.setData(Qt.UserRole, ITEM_ECLIPSE)
            # print('xxxxxxxxxxxxxxx', elementTemp.attribute('position_x'))
            # print('yyyyyyyyyyyyyyy', elementTemp.attribute('position_y'))
            self.m_pScene.addItem(pObstacle)
            pObstacle.setRotation(float(elementTemp.attribute('rotation')))
            pObstacle.setPos(QPointF(float(elementTemp.attribute('position_x')), float(elementTemp.attribute('position_y'))))
            pObstacle.setColor(Util.long2Color(int(elementTemp.attribute('color'))))
            pObstacle.setName(elementTemp.attribute('name'))
            self.m_pScene.m_barrierItemList.append(pObstacle)
            # self.m_pScene.addItem(pObstacle)
            # self.m_pScene.insertItem(pObstacle)

    def readOccupied(self, element):

        width = float(element.attribute('width'))
        height = float(element.attribute('height'))
        pOccupied= RectOccupied(width, height)
        self.m_pScene.addItem(pOccupied)
        pOccupied.setData(Qt.UserRole, ITEM_RECT_OCCUPIED)
        pOccupied.setPos(QPointF(float(element.attribute('position_x')), float(element.attribute('position_y'))))
        pOccupied.setRotation(float(element.attribute('rotation')))
        pOccupied.setColor(Util.long2Color(int(element.attribute('color'))))
        pOccupied.setName(element.attribute('name'))
        self.m_pScene.m_occupiedItemList.append(pOccupied)
        # self.m_pScene.addItem(pOccupied)
        # self.m_pScene.insertOccupiedItem(pOccupied)

    def slotClear(self):

        self.m_pScene.clear()
        self.m_pScene.m_pBoundaryItem = None
        self.m_pScene.m_barrierItemList = []
        self.m_pScene.m_occupiedItemList = []
        self.m_pScene.m_eclipseSiteList = []
        self.m_pScene.helperItemList = []
        self.m_pScene.points = []
        self.m_pScene.points_edge = []
        self.m_pScene.lineItems = []
        self.m_pScene.lineItems_edge = []
        self.m_pScene.m_editState = 0

        self.m_pScene.m_pathName = None
        self.m_pScene.m_StartEclipseSite = None
        self.m_pScene.m_EndEclipseSite = None



    def writeXMLFile(self, filePath):

        if len(filePath) == 0:
            return False
        xmlFile = QFile(filePath)
        if not xmlFile.open(QIODevice.WriteOnly | QIODevice.Truncate):
            print("the file can not be writen error:", xmlFile.errorString())
            return False
        doc = QDomDocument()
        instruction = doc.createProcessingInstruction("xml", 'version="1.0" encoding="UTF-8"')

        doc.appendChild(instruction)
        root = doc.createElement('SceneDesignTemplate')
        root.setAttribute('name', self.m_pTemplate.getTemplateName())
        root.setAttribute('remark', self.m_pTemplate.getRemark())
        root.setAttribute('mode', self.m_pTemplate.getMode())
        root.setAttribute('scale', self.m_pTemplate.getScale())
        doc.appendChild(root)

        self.m_pBoundary = self.m_pScene.getBoundary()
        if self.m_pBoundary:
            boundaryNode = doc.createElement('Boundary')
            boundaryPolygon = self.m_pBoundary.polygonF()
            for point in boundaryPolygon:
                pointNode = doc.createElement('point')
                pointNode.setAttribute('x', point.x())
                pointNode.setAttribute('y', point.y())
                boundaryNode.appendChild(pointNode)
            root.appendChild(boundaryNode)

        barrierNode = doc.createElement('Barrier')
        items = self.m_pScene.items()
        # print('items.size:', len(items))
        siteItems = []
        occupiedItems = []
        for item in items:
            pObstacle = item
            if (pObstacle) and (pObstacle.type() != ITEM_POLYGON_EDGE) and (pObstacle.type() != ITEM_ECLIPSE_SITE) and (pObstacle.type() != ITEM_ECLIPSE_SITE_ROTATION) and (pObstacle.type() != ITEM_RECT_OCCUPIED) and (not isinstance(pObstacle, HelperItem)) and (not isinstance(pObstacle, LineItem) and (not isinstance(pObstacle, QGraphicsPathItem))):
                if self.getBarrierNameByType(pObstacle.type()) == 'error':
                    return False
                node = doc.createElement(self.getBarrierNameByType(pObstacle.type()))
                node.setAttribute('name', pObstacle.getName())
                node.setAttribute('type', pObstacle.type())
                node.setAttribute('position_x', pObstacle.pos().x())
                node.setAttribute('position_y', pObstacle.pos().y())
                node.setAttribute('rotation', pObstacle.rotation())
                node.setAttribute('color', Util.color2Long(pObstacle.getColor()))

                if pObstacle.type() == ITEM_RECT:
                    rectObj = pObstacle
                    node.setAttribute('width', rectObj.width())
                    node.setAttribute('height', rectObj.height())
                elif pObstacle.type() == ITEM_ECLIPSE:
                    eclipseObj = pObstacle
                    node.setAttribute('radius_x', eclipseObj.radiusX())
                    node.setAttribute('radius_y', eclipseObj.radiusY())
                elif pObstacle.type() == ITEM_POLYGON:
                    polyObj = pObstacle
                    p = polyObj.polygonF()
                    for point in p:
                        pointNode = doc.createElement('point')
                        pointNode.setAttribute('x', point.x())
                        pointNode.setAttribute('y', point.y())
                        node.appendChild(pointNode)
                barrierNode.appendChild(node)

            elif (item.data(Qt.UserRole) == ITEM_ECLIPSE_SITE):
                pSite = item
                siteItems.append(pSite)
            elif (item.data(Qt.UserRole) == ITEM_RECT_OCCUPIED):
                pOccupied = item
                occupiedItems.append(pOccupied)
        root.appendChild(barrierNode)

        for pSite in siteItems:
            siteNode = doc.createElement('EclipseSite')
            siteNode.setAttribute('id', pSite.id())
            siteNode.setAttribute('name', pSite.getName())
            siteNode.setAttribute('type', pSite.type())
            siteNode.setAttribute('position_x', pSite.pos().x())
            siteNode.setAttribute('position_y', pSite.pos().y())
            siteNode.setAttribute('rotation', pSite.rotation())
            siteNode.setAttribute('color', Util.color2Long(pSite.getColor()))
            siteNode.setAttribute('radius_x', pSite.radiusX())
            siteNode.setAttribute('radius_y', pSite.radiusY())
            root.appendChild(siteNode)

        for pOccupied in occupiedItems:
            occupiedNode = doc.createElement('Occupied')
            occupiedNode.setAttribute('name', pOccupied.getName())
            occupiedNode.setAttribute('type', pOccupied.type())
            occupiedNode.setAttribute('position_x', pOccupied.pos().x())
            occupiedNode.setAttribute('position_y', pOccupied.pos().y())
            occupiedNode.setAttribute('rotation', pOccupied.rotation())
            occupiedNode.setAttribute('width', pOccupied.width())
            occupiedNode.setAttribute('height', pOccupied.height())
            occupiedNode.setAttribute('color', Util.color2Long(pOccupied.getColor()))
            root.appendChild(occupiedNode)


        paths = self.getPaths()
        for pPath in paths:
            pathNode = doc.createElement('Path')
            pathNode.setAttribute('id', pPath.id())
            pathNode.setAttribute('name', pPath.getName())
            pathNode.setAttribute('color', Util.color2Long(pPath.getColor()))

            startNode = doc.createElement('StartPoint')
            startNode.setAttribute('eclipseSite_id', pPath.getStartItem().id())
            startNode.setAttribute('angle', pPath.getStartItem().rotation())
            pathNode.appendChild(startNode)

            wayNode = doc.createElement('WayPoint')
            wayPoints = pPath.getWayPoints()
            for point in wayPoints:
                node = doc.createElement('Node')
                node.setAttribute('pos', Util.pointF2String(point.pos_))
                node.setAttribute('angle', point.radian_)
                wayNode.appendChild(node)
            pathNode.appendChild(wayNode)

            endNode = doc.createElement('EndPoint')
            endNode.setAttribute('eclipseSite_id', pPath.getEndItem().id())
            endNode.setAttribute('angle', pPath.getEndItem().rotation())
            pathNode.appendChild(endNode)

            root.appendChild(pathNode)
        text = QTextStream(xmlFile)
        doc.save(text, 4)
        xmlFile.close()
        return True

    def getBarrierNameByType(self, type):

        if type == ITEM_RECT:
            return 'Rect'
        elif type == ITEM_ECLIPSE:
            return 'Eclipse'
        elif type == ITEM_POLYGON:
            return 'Polygon'

        return 'Error'

    def setPathWayPoints(self):

        paths = self.getPaths()
        for pPath in paths:
            pStartItem = pPath.getStartItem()
            pPath.setStartPosAndAngle(pStartItem, pStartItem.rotation())
            pEndItem = pPath.getEndItem()
            pPath.setEndPosAndAngle(pEndItem, pEndItem.rotation())
            pPath.setWayPoints(self.makeWayFromScene(pStartItem, pPath.id()))

    def makeWayFromScene(self, pStartItem, id):

        # pass
        if not pStartItem:
            wayPoints = []
            QMessageBox.warning(self, '警告', pStartItem.getName()+':路径信息错误！')
            return wayPoints
        path = []
        pCurItem = pStartItem.getLineItemMap().get(id)
        while pCurItem:
            pObserver = pCurItem.endObserver()
            path.append(WayPoint(pObserver.pos(), pObserver.rotation()))
            pItem = pObserver
            if isinstance(pItem, AnchorItem):
                pCurItem = pItem.beforeLineItem()
            else:
                pCurItem = None
            path.pop()

            print('type(path):', type(path))
            return path


    def slotButtonGroupClicked(self, type):

        # pass
        self.m_pScene.setEditState(type)

        for button in self.m_pButtonGroup.buttons():
            id = self.m_pButtonGroup.id(button)
            if id != type:
                button.setChecked(False)

    def slotFinishInsert(self, type):

        # pass
        button = self.m_pButtonGroup.button(type)
        if button != None:
            button.setChecked(False)

    def slotItemPressed(self, pItem, index):

        self.tempTreeItem = pItem
        if QApplication.mouseButtons() == Qt.RightButton:
            menu = QMenu()
            menu.addAction(self.m_pAddPathAction)
            menu.exec(QCursor.pos())

    def slotAddPath(self):

        # pass
        dialog = pathEditDialog()
        dialog.setScene(self.m_pScene)

        if dialog.exec() == QDialog.Accepted:
            pPath = Path()
            pPath.setName(dialog.getPathName())
            self.m_pScene.m_pathName = dialog.getPathName()
            pPath.setStartItem(dialog.getStartSite())
            self.m_pScene.m_StartEclipseSite = dialog.getStartSite()
            pPath.setEndItem(dialog.getEndSite())
            self.m_pScene.m_EndEclipseSite = dialog.getEndSite()

            self.appendPathTreeItem(pPath)
            self.m_pView.insertPath(pPath)
            self.pPathNameValue.setText(self.m_pScene.m_pathName)
            self.pStartValue.setText('站位'+str(self.m_pScene.m_StartEclipseSite.id_) + '(' + str(self.m_pScene.m_StartEclipseSite.pos().x()) + ' , ' + str(self.m_pScene.m_StartEclipseSite.pos().y()) + ')')
            self.pEndValue.setText('站位'+str(self.m_pScene.m_EndEclipseSite.id_) + '(' + str(self.m_pScene.m_EndEclipseSite.pos().x()) + ' , ' + str(self.m_pScene.m_EndEclipseSite.pos().y()) + ')')
            self.pWeight1Edit.setText(str(0.4))
            self.pWeight2Edit.setText(str(0.3))
            self.pWeight3Edit.setText(str(0.3))
            self.pOutdEdit.setText(str(50.0))
            self.pIndEdit.setText(str(50.0))
            self.pOutclEdit.setText(str(100.0))
            self.pInclEdit.setText(str(100.0))


    def appendPathTreeItem(self, pPath):

        pItem = TreeItem(pPath.getName(), pPath)
        pItem.setData(0, Qt.UserRole, pPath.getId())
        self.tempTreeItem.addChild(pItem)
        self.tempTreeItem.setExpanded(True)

    def getPaths(self):

        paths = []
        for i in range(self.m_pPathTreeRootItem.childCount()):
            pItem = self.m_pPathTreeRootItem.child(i)
            if pItem.data(0, Qt.UserRole) != -1:
                paths.append(pItem.getPath())
        return paths


    def slotOKPathPara(self):

        self.m_pScene.m_StartEclipseSite.weight1 = float(self.pWeight1Edit.text())
        self.m_pScene.m_StartEclipseSite.weight2 = float(self.pWeight2Edit.text())
        self.m_pScene.m_StartEclipseSite.weight3 = float(self.pWeight3Edit.text())
        self.m_pScene.m_StartEclipseSite.outd = float(self.pOutdEdit.text())
        self.m_pScene.m_StartEclipseSite.ind = float(self.pIndEdit.text())
        self.m_pScene.m_StartEclipseSite.outcl = float(self.pOutclEdit.text())
        self.m_pScene.m_StartEclipseSite.incl = float(self.pInclEdit.text())
        QMessageBox.information(self, '提示', '参数设置完毕', QMessageBox.Yes|QMessageBox.No, QMessageBox.Yes)


    def slotCancelPathPara(self):

        self.m_pScene.m_StartEclipseSite.weight1 = 0.4
        self.m_pScene.m_StartEclipseSite.weight2 = 0.3
        self.m_pScene.m_StartEclipseSite.weight3 = 0.3
        self.m_pScene.m_StartEclipseSite.outd = 50.0
        self.m_pScene.m_StartEclipseSite.ind = 50.0
        self.m_pScene.m_StartEclipseSite.outcl = 100.0
        self.m_pScene.m_StartEclipseSite.incl = 100.0
        QMessageBox.information(self, '提示', '参数已重置', QMessageBox.Yes|QMessageBox.No, QMessageBox.Yes)

# from SimuEnv.obstacle import *








if __name__ == '__main__':
    app = QApplication(sys.argv)
    print('0000000000000000000')
    main = MainWindow()
    print('1111111111111111111')
    main.showMaximized()
    sys.exit(app.exec_())





