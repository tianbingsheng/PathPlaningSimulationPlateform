import sys
import os
import math
from abc import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
# from SimuEnv.obstacle import *
from SimuEnv.helperitem import *
from SimuEnv.sysinclude import *
from SimuEnv.util import *
from SimuEnv.pathgenerate import *
from SimuEnv.pathinfo import *
from PyQt5.QtXml import QDomDocument
from SimuEnv.template import *


class Scene(QGraphicsScene):

    m_pBoundaryItem = None
    m_barrierItemList = []
    m_occupiedItemList = []
    m_eclipseSiteList = []
    # helperItemList = []
    points = []
    points_edge = []
    lineItems = []
    lineItems_edge = []
    m_editState = 0

    m_pathName = None
    m_StartEclipseSite = None
    m_EndEclipseSite = None


    emitFinishInsert = pyqtSignal(int)
    emitSelectedItem = pyqtSignal(type)

    def __init__(self):
        super(Scene, self).__init__()
        self.helperItemList = []
        self.initHelperItems()
        self.createConnection()
        #buildTest()

    def initHelperItems(self):

        for i in range(4):
            rect = QRectF(0, 0, 5, 5)
            item = HelperItem(rect, i)
            self.helperItemList.append(item)
            item.setVisible(False)
            self.addItem(item)

    def helperItems(self):

        return self.helperItemList

    def setEditState(self, state):

        self.m_editState = state

    def getBarrierItemList(self):

        return self.m_barrierItemList

    def getOccupiedItemList(self):

        return self.m_occupiedItemList

    def getEclipseSiteList(self):

        return self.m_eclipseSiteList



    def mousePressEvent(self, event):
    # def mousePressEvent(self, event):

        item = None
        if (self.m_editState == ITEM_RECT) and (QApplication.mouseButtons() == Qt.LeftButton):
            # item = Test()
            # item = Obstacle()
            item = RectObstacle()
            item.setData(Qt.UserRole, ITEM_RECT)
            # item.setPos(event.scenePos())
            self.m_barrierItemList.append(item)
            item.ObstacleID = len(self.m_barrierItemList)
            self.addItem(item)

        elif (self.m_editState == ITEM_RECT_OCCUPIED) and (QApplication.mouseButtons() == Qt.LeftButton):
            item = RectOccupied()
            item.setData(Qt.UserRole, ITEM_RECT_OCCUPIED)
            # item.setPos(event.scenePos())
            self.addItem(item)
            self.m_occupiedItemList.append(item)
            item.OccupiedID = len(self.m_occupiedItemList)
        elif (self.m_editState == ITEM_ECLIPSE) and (QApplication.mouseButtons() == Qt.LeftButton):
            item = EclipseObstacle()
            item.setData(Qt.UserRole, ITEM_ECLIPSE)
            self.addItem(item)
            # item.setPos(event.scenePos())
            self.m_barrierItemList.append(item)
            item.ObstacleID = len(self.m_barrierItemList)
        elif (self.m_editState == ITEM_POLYGON):
            if (QApplication.mouseButtons() == Qt.LeftButton):
                self.points.append(event.scenePos())
                if len(self.points) >= 2:
                    item2 = QGraphicsLineItem()
                    item2.setLine(QLineF(self.points[len(self.points)-1], self.points[len(self.points)-2]))
                    self.addItem(item2)
                    self.lineItems.append(item2)
            elif (QApplication.mouseButtons() == Qt.RightButton):
                if len(self.points) > 2:
                    for i in self.lineItems:
                        self.removeItem(i)
                    # del self.lineItems
                    self.lineItems.clear()
                    polygon1 = QPolygonF(self.points)
                    obstacle = PolygonObstacle(polygon1)
                    # obstacle = PolygonObstacle(self.points)
                    self.points.clear()
                    item = obstacle
                    item.setData(Qt.UserRole, ITEM_POLYGON)
                    self.addItem(item)
                    self.m_barrierItemList.append(item)
        elif (self.m_editState == ITEM_POLYGON_EDGE):
            if (QApplication.mouseButtons() == Qt.LeftButton):
                self.points_edge.append(event.scenePos())
                if len(self.points_edge) >= 2:
                    item2 = QGraphicsLineItem()
                    item2.setLine(QLineF(self.points_edge[len(self.points) - 1], self.points_edge[len(self.points) - 2]))
                    self.addItem(item2)
                    self.lineItems_edge.append(item2)
            elif (QApplication.mouseButtons() == Qt.RightButton):
                if len(self.points_edge) > 2:
                    for i in self.lineItems_edge:
                        self.removeItem(i)
                    # del self.lineItems_edge
                    self.lineItems_edge.clear()
                    polygon2 = QPolygonF(self.points_edge)
                    obstacle = PolygonEdgeObstacle(polygon2)
                    # obstacle = PolygonEdgeObstacle(self.points_edge)
                    self.points_edge.clear()
                    item = obstacle
                    item.setData(Qt.UserRole, ITEM_POLYGON_EDGE)
                    item.enableBoundary()
                    # item.setPos(event.scenePos())
                    self.addItem(item)


        elif (self.m_editState == ITEM_ECLIPSE_SITE) and (QApplication.mouseButtons() == Qt.LeftButton):
            pESItem = EclipseSite()
            pESItem.setColor(lightBlue)
            pESItem.setData(Qt.UserRole, ITEM_ECLIPSE_SITE)
            self.addItem(pESItem)
            pESItem.setPos(event.scenePos())
            self.emitFinishInsert.emit(self.m_editState)
            self.m_eclipseSiteList.append(pESItem)
            self.m_editState = 0

        if  item:
            if self.m_editState == ITEM_POLYGON_EDGE or self.m_editState == ITEM_POLYGON:
                item.setPos(0, 0)
            else:
                item.setPos(event.scenePos())

            self.emitFinishInsert.emit(self.m_editState)

            if self.m_editState == ITEM_POLYGON_EDGE:
                pObj = item
                if pObj:
                    self.m_pBoundaryItem = item
                    # pObj.enableBoundary()
                    pObj.setFlag(QGraphicsLineItem.ItemIsMovable, False)
                    pObj.setFlag(QGraphicsLineItem.ItemIsSelectable, False)

            self.m_editState = 0

        QGraphicsScene.mousePressEvent(self, event)
        # super().mousePressEvent(event)


    def createConnection(self):
        pass


    def mouseReleaseEvent(self, event):

        # super().mouseReleaseEvent(event)
        QGraphicsScene.mouseReleaseEvent(self, event)

    def setBoundary(self):
        pass

    def getBoundary(self):
        if self.m_pBoundaryItem:
            return self.m_pBoundaryItem

    def insertBoundary(self, pObj):
        if pObj:
            self.m_pBoundaryItem = pObj
            pObj.enableBoundary()
            pObj.setFlag(QGraphicsItem.ItemIsMovable, False)
            pObj.setFlag(QGraphicsItem.ItemIsSelectable, False)
            self.m_pBoundaryItem.setData(Qt.UserRole, ITEM_POLYGON_EDGE)
            self.addItem(pObj)

    def insertItem(self, pObj):
        assert (pObj)
        self.addItem(pObj)
        pObj.setFlag(QGraphicsItem.ItemIsMovable, False)
        pObj.setFlag(QGraphicsItem.ItemIsSelectable, False)
        self.m_barrierItemList.append(pObj)

    def insertOccupiedItem(self, pObj):
        assert (pObj)
        self.addItem(pObj)
        pObj.setFlag(QGraphicsItem.ItemIsMovable, False)
        pObj.setFlag(QGraphicsItem.ItemIsSelectable, False)
        self.m_occupiedItemList.append(pObj)

    def insertEclipseSiteItem(self, pObj):

        assert (pObj)
        self.addItem(pObj)
        pObj.setFlag(QGraphicsItem.ItemIsMovable, False)
        pObj.setFlag(QGraphicsItem.ItemIsSelectable, False)
        self.m_eclipseSiteList.append(pObj)

    def wheelEvent(self, event):

        if (event.delta() != 0) and (QApplication.keyboardModifiers() == Qt.ShiftModifier):
            for item in self.selectedItems():
                item.setRotation(int(item.rotation() + event.delta()/120.0 + 360) % 360)
                item.update()
        # super().wheelEvent(event)
        QGraphicsScene.wheelEvent(self, event)

    def buildTest(self):
        pass

    def mouseMoveEvent(self, event):
        if len(self.selectedItems()) != 1 :
            return
        pItem = self.selectedItems()[0]
        if pItem:
            if QApplication.keyboardModifiers()==Qt.ShiftModifier:
                lineF = QLineF(event.scenePos(), pItem.pos())
                pItem.setRotation(-(lineF.angle()-270))
        super().mouseMoveEvent(event)
        QGraphicsScene.mouseMoveEvent(self, event)






class SceneWidget(QGraphicsView):

    m_pTemplate = Template()
    m_pScene = None
    # m_pScene = Scene()

    # def __init__(self):
    #
    #     super(SceneWidget, self).__init__()
    #     self.m_pScene = scene.Scene()
    #     self.m_pScene.setSceneRect(-1000, -1000, 2000, 2000)
    #     self.setScene(self.m_pScene)

    def __init__(self, pScene):

        super(SceneWidget, self).__init__()
        self.m_pScene = pScene
        self.setScene(self.m_pScene)
        self.horizontalScrollBar().installEventFilter(self)
        self.verticalScrollBar().installEventFilter(self)

    def readXMLFile(self, filePath):

        xmlFile = QFile(filePath)
        if not xmlFile.open(QIODevice.ReadOnly):
            return False
        domDocument = QDomDocument()
        if not domDocument.setContent(xmlFile, True):
            xmlFile.close()
            return False
        root = domDocument.documentElement()
        if root.tagName() != 'Environment_Template':
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
            child = child.nextSiblingElement()
        return True

    def readBoundary(self, element):
        pass

    def readBarrier(self, element):
        pass

    def insertItem(self, pItem):
        assert (pItem != None)
        self.m_pScene.addItem(pItem)

    # def wheelEvent(self, event):
    #     pass
        # event.setWidget(self.viewport())
        # event.setScene(self.mapToScene(event.pos()))
        # event.setScenePos(event.globalPos())
        # event.setAccepted(False)
        # wheelEvent = QGraphicsSceneEvent(QEvent.GraphicsSceneWheel)
        # wheelEvent.widget(self.viewport())
        # wheelEvent.scenePos(self.mapToScene(event.pos()))
        # wheelEvent.screenPos(event.globalPos())
        # wheelEvent.buttons(event.buttons())
        # wheelEvent.modifiers(event.modifiers)
        # wheelEvent.delta(event.delta())
        # wheelEvent.orientation(event.orientation())
        # wheelEvent.setAccepted(False)
        # QApplication.sendEvent(self.scene(), wheelEvent)
        # event.setAccepted(wheelEvent.isAccepted())

    def insertPath(self, pPath, isMovable = True):

        # pass
        pStartItem = pPath.getStartItem()
        pStartItem.setFlag(QGraphicsItem.ItemIsMovable, isMovable)
        if isMovable:
            pPath.setStartItem(pStartItem)
        else:
            pPath.setSceneStartItem(pStartItem)
        pEndItem = pPath.getEndItem()
        pEndItem.setFlag(QGraphicsItem.ItemIsMovable, isMovable)
        pEndItem.setEnd(True)

        if isMovable:
            pPath.setEndItem(pEndItem)
        else:
            pPath.setSceneEndItem(pEndItem)
        pLineItem = LineItem(pStartItem, pEndItem)
        pStartItem.setLineItem(pLineItem, pPath.id())
        self.insertItem(pLineItem)

        pLineItem.setVisible(True)

        wayPoints = pPath.getWayPoints()
        for i in range(len(wayPoints)-1, 0, -1):
            pStartItem.insertAnchorItem(wayPoints[i].pos_, wayPoints[i].radian_, not isMovable)


class Obstacle(QGraphicsItem):

    m_lineSize = 5
    entityName = ''
    ObstacleID = 0
    OccupiedID = 0
    # m_color = Qt.transparent

    def __init__(self):

        super(Obstacle, self).__init__()
        self.setFlag(QGraphicsItem.ItemIsSelectable)
        self.setFlag(QGraphicsItem.ItemIsMovable)
        self.setFlag(QGraphicsItem.ItemSendsGeometryChanges)
        self.setFlag(QGraphicsItem.ItemSendsScenePositionChanges)
        self.m_color = QColor(Qt.transparent)
        # self.m_color = Qt.transparent
        self.m_isBoundary = False

    # def mousePressEvent(self, event):
    def mousePressEvent(self, event: 'QGraphicsSceneMouseEvent'):

        if not self.isBoundary():
            self.updateHelperItem()
            cursor = QCursor()
            cursor.setShape(Qt.SizeAllCursor)
            self.setCursor(cursor)
        QGraphicsItem.mousePressEvent(self, event)
        # QGraphicsItem.mousePressEvent(event)

    # def mouseReleaseEvent(self, event):
    def mouseReleaseEvent(self, event: 'QGraphicsSceneMouseEvent'):

        cursor = QCursor()
        cursor.setShape(Qt.ArrowCursor)
        self.setCursor(cursor)
        # super().mouseReleaseEvent(event)
        QGraphicsItem.mouseReleaseEvent(self, event)

    def exitEditState(self):

        pScene = self.scene()
        assert (pScene)
        # items = pScene.helperItems().copy()
        for i in range(len(self.scene().helperItems())):
            self.scene().helperItems()[i].setVisible(False)
            # items[i].setVisible(False)


    def paint(self, painter, option, widget):

        self.render(painter)


    def render(self, painter):
        pass

    def isBoundary(self):

        return self.m_isBoundary

    def updateHelperItem(self):

        items = self.scene().helperItems().copy()

        centers = self.calCenterForEachLine(self.boundingRect(), self.m_lineSize)
        for i in range(len(items)):
            rect = self.calSquareByWidth(self.m_lineSize)
            items[i].setRect(rect)
            sceneP = self.mapToScene(centers[i])
            items[i].setPos(sceneP)
            items[i].setObstacle(self)
            items[i].setVisible(True)

    def boundingRect(self):

        return QRectF()

    def calCenterForEachLine(self, rect, linesize):

        top = QLineF(rect.topLeft(), rect.topRight())
        bottom = QLineF(rect.bottomLeft(), rect.bottomRight())
        left = QLineF(rect.topLeft(), rect.bottomLeft())
        right = QLineF(rect.topRight(), rect.bottomRight())

        fourCenters = []
        fourCenters.append(top.pointAt(0.5))
        fourCenters.append(bottom.pointAt(0.5))
        fourCenters.append(left.pointAt(0.5))
        fourCenters.append(right.pointAt(0.5))
        return fourCenters

    def calSquareByWidth(self, width):

        assert (width >= 1)
        rect = QRectF(0, 0, width, width)
        rect.moveCenter(QPointF(0.0, 0.0))
        return rect

    def getAttributes(self):

        ret = []
        pair = Pair('', '')
        pair.first = QObject.tr('位置')
        pair.second = ('(%1,%2)').format(self.pos().x, self.pos().y())
        ret.append(pair)
        return ret

    def itemChange(self, change, value):

        if change == QGraphicsItem.ItemPositionHasChanged:
            self.updateHelperItem()
        return value

    def getColor(self):

        return self.m_color

    def getName(self):

        return self.entityName

    def setColor(self, color):

        self.m_color = color

    def setName(self, name):

        self.entityName = name

    def enableBoundary(self):

        self.m_isBoundary = True

    @abstractmethod
    def type(self):
        pass

    @abstractmethod
    def adjust(self, dirType, vec):
        pass




class RectObstacle(Obstacle):

    # def __init__(self):
    #     super(RectObstacle, self).__init__()
    #     self.m_width = 50.0
    #     self.m_height = 60.0

    def __init__(self, width=50.0, height=60.0):
        super().__init__()
        self.m_width = width
        self.m_height = height

    def type(self):

        return sysinclude.ITEM_RECT

    def boundingRect(self):

        rect = QRectF(0, 0, self.m_width, self.m_height)
        rect.moveCenter(QPointF(0.0, 0.0))
        return rect

    def render(self, painter):

        painter.save()
        brush = QBrush(Qt.black, Qt.Dense5Pattern)
        painter.setBrush(brush)
        painter.setPen(QPen(Qt.black, 2, Qt.DotLine))
        # brush = QBrush(self.m_color)
        # painter.setBrush(brush)
        painter.drawRect(self.boundingRect())
        painter.restore()

    def adjust(self, dirType, vec):

        if dirType == HelperItem.DIR_RIGHT:
            self.m_width += vec.x()
            curPos = self.pos()
            curPos.setX(curPos.x() + vec.x() / 2)
            self.setPos(curPos)
        elif dirType == HelperItem.DIR_LEFT:
            self.m_width -= vec.x()
            curPos = self.pos()
            curPos.setX(curPos.x() + vec.x() / 2)
            self.setPos(curPos)
        elif dirType == HelperItem.DIR_BOTTOM:
            self.m_height += vec.y()
            curPos = self.pos()
            curPos.setY(curPos.y() + vec.y() / 2)
            self.setPos(curPos)
        elif dirType == HelperItem.DIR_TOP:
            self.m_height -= vec.y()
            curPos = self.pos()
            curPos.setY(curPos.y() + vec.y() / 2)
            self.setPos(curPos)

        self.prepareGeometryChange()
        self.updateHelperItem()
        self.update()

    def width(self):

        return self.m_width

    def height(self):

        return self.m_height


class RectOccupied(Obstacle):

    # def __init__(self):
    #     super(RectOccupied, self).__init__()
    #     self.m_width = 50.0
    #     self.m_height = 60.0

    def __init__(self, width=50.0, height=60.0):
        super(RectOccupied, self).__init__()
        self.m_width = width
        self.m_height = height

    def type(self):

        return sysinclude.ITEM_RECT_OCCUPIED

    def boundingRect(self):

        rect = QRectF(0, 0, self.m_width, self.m_height)
        rect.moveCenter(QPointF(0.0, 0.0))
        return rect

    def render(self, painter):

        painter.save()
        # brush = QBrush(Qt.black, Qt.Dense5Pattern)
        # painter.setBrush(brush)
        painter.setPen(QPen(Qt.black,2))
        painter.drawRect(self.boundingRect())
        painter.restore()

    def adjust(self, dirType, vec):

        if dirType == HelperItem.DIR_RIGHT:
            self.m_width += vec.x()
            curPos = self.pos()
            curPos.setX(curPos.x() + vec.x() / 2)
            self.setPos(curPos)
        elif dirType == HelperItem.DIR_LEFT:
            self.m_width -= vec.x()
            curPos = self.pos()
            curPos.setX(curPos.x() + vec.x() / 2)
            self.setPos(curPos)
        elif dirType == HelperItem.DIR_BOTTOM:
            self.m_height += vec.y()
            curPos = self.pos()
            curPos.setY(curPos.y() + vec.y() / 2)
            self.setPos(curPos)
        elif dirType == HelperItem.DIR_TOP:
            self.m_height -= vec.y()
            curPos = self.pos()
            curPos.setY(curPos.y() + vec.y() / 2)
            self.setPos(curPos)

        self.prepareGeometryChange()
        self.updateHelperItem()
        self.update()

    def width(self):

        return self.m_width

    def height(self):

        return self.m_height


class EclipseObstacle(Obstacle):

    # def __init__(self):
    #     super(EclipseObstacle, self).__init__()
    #     self.m_rx = 50.0
    #     self.m_ry = 60.0

    def __init__(self, rx=30.0, ry=30.0):
        super(EclipseObstacle, self).__init__()
        self.m_rx = rx
        self.m_ry = ry

    def boundingRect(self):

        rect = QRectF(0, 0, 2.0 * self.m_rx, 2.0 * self.m_ry)
        rect.moveCenter(QPointF(0.0, 0.0))
        return rect

    def render(self, painter):

        painter.save()
        brush = QBrush(Qt.black, Qt.Dense5Pattern)
        painter.setBrush(brush)
        painter.setPen(QPen(Qt.black, 2, Qt.DotLine))
        # brush = QBrush(self.m_color)
        # painter.setBrush(brush)
        painter.drawEllipse(QPointF(0.0, 0.0), self.m_rx, self.m_ry)
        painter.restore()

    def type(self):

        return sysinclude.ITEM_ECLIPSE

    def adjust(self, dirType, vec):

        if dirType == HelperItem.DIR_TOP:
            self.m_ry += -(vec.y() / 2)
            curPos = self.pos()
            curPos.setY(curPos.y() + vec.y() / 2)
            self.setPos(curPos)
        elif dirType == HelperItem.DIR_BOTTOM:
            self.m_ry += vec.y() / 2
            curPos = self.pos()
            curPos.setY(curPos.y() + vec.y() / 2)
            self.setPos(curPos)
        elif dirType == HelperItem.DIR_LEFT:
            self.m_rx += -(vec.x() / 2)
            curPos = self.pos()
            curPos.setX(curPos.x() + vec.x() / 2)
            self.setPos(curPos)
        elif dirType == HelperItem.DIR_RIGHT:
            self.m_rx += vec.x() / 2
            curPos = self.pos()
            curPos.setX(curPos.x() + vec.x() / 2)
            self.setPos(curPos)
        self.prepareGeometryChange()
        self.updateHelperItem()
        self.update()

    def radiusX(self):

        return self.m_rx

    def radiusY(self):

        return self.m_ry


class PolygonObstacle(Obstacle):

    def __init__(self, polygon):
        super(PolygonObstacle, self).__init__()
        # self.m_polygonF = QPolygonF(self.mapFromScene(points))
        self.m_polygonF = self.mapFromScene(polygon)

    def boundingRect(self):
        rect = self.m_polygonF.boundingRect()
        return rect

    def render(self, painter):
        painter.save()
        # brush = QBrush(self.m_color)
        # painter.setBrush(brush)
        brush = QBrush(Qt.black, Qt.Dense5Pattern)
        painter.setBrush(brush)
        painter.setPen(QPen(Qt.black, 2, Qt.DotLine))
        painter.drawPolygon(self.m_polygonF)
        painter.restore()

    def type(self):
        return sysinclude.ITEM_POLYGON

    def polygonF(self):
        return self.m_polygonF


class PolygonEdgeObstacle(PolygonObstacle):

    def __init__(self, polygon):
        super().__init__(polygon)
        # self.m_polygonF = QPolygonF(self.mapFromScene(points))
        # self.m_polygonF = self.mapFromScene(polygon)

    def render(self, painter):
        painter.save()
        # brush = QBrush(self.m_color)
        # painter.setBrush(brush)
        painter.setPen(QPen(Qt.black, 1))
        painter.drawPolygon(self.m_polygonF)
        painter.restore()

    def type(self):
        return sysinclude.ITEM_POLYGON_EDGE


class Subject(QGraphicsItem):

    def __init__(self):
        super(Subject, self).__init__()

    def updateFromObserver(self, pObserve):
        pass

    def boundingRect(self):

        return QRectF()


class Observer(QGraphicsItem):

    def __init__(self):
        super(Observer, self).__init__()
        self.objs = []
    def attach(self, obj):
        self.objs.append(obj)
    def detach(self, obj):
        self.objs.remove(obj)
    def notify(self):
        for pObj in self.objs:
            pObj.updateFromObserver(self)

    def boundingRect(self):

        return QRectF()

    # def paint(self, painter, option, widget):
    #
    #     pass

class AnchorItem(Observer):

    def __init__(self):

        super(AnchorItem, self).__init__()
        self.setFlag(QGraphicsItem.ItemIsMovable)
        self.setFlag(QGraphicsItem.ItemIsSelectable)
        self.setFlag(QGraphicsItem.ItemSendsGeometryChanges)
        self.setFlag(QGraphicsItem.ItemSendsScenePositionChanges)
        self.radius = 10
        self.pInsertAnchorAction = QAction('插入锚点', self.scene())
        self.pDeleteAnchorAction = QAction('删除锚点', self.scene())
        self.pInsertAnchorAction.triggered.connect(self.slotInsertAnchorItem)
        self.pDeleteAnchorAction.triggered.connect(self.slotDeleteAnchorItem)

    def boundingRect(self):

        return QRectF(-self.radius, -self.radius, 2 * self.radius, 2 * self.radius)

    def paint(self, painter, option, widget=None):

        painter.save()
        painter.drawEllipse(QPointF(0.0, 0.0), self.radius, self.radius)
        points = [QPointF(0.0, -self.radius), QPointF(-self.radius / 1.5, 0.0), QPointF(self.radius / 1.5, 0.0)]
        polygonF = QPolygonF()
        for i in range(len(points)):
            polygonF.insert(i, points[i])
        leftCorner = QPointF(-self.radius / 4.0, 0.0)
        width = self.radius / 2.0
        height = math.sqrt(15) * self.radius / 4.0
        rectF = QRectF(leftCorner.x(), leftCorner.y(), width, height)

        brush = QBrush(Qt.red)
        painter.setBrush(brush)
        painter.drawPolygon(polygonF)
        painter.drawRect(rectF)
        painter.restore()


    # def mousePressEvent(self, event):
    #
    #     if self.pBeforeLineItem and QApplication.mouseButtons() == Qt.RightButton:
    #         self.menu = QMenu()
    #         self.pInsertAnchorAction = self.menu.addAction('插入锚点')
    #         self.pDeleteAnchorAction = self.menu.addAction('删除锚点')
    #         self.menu.exec_(QCursor.pos())
    #         self.pInsertAnchorAction.triggered.connect(self.slotInsertAnchorItem)
    #         self.pDeleteAnchorAction.triggered.connect(self.slotDeleteAnchorItem)

        # super().mousePressEvent(event)
    def contextMenuEvent(self, event: 'QGraphicsSceneContextMenuEvent'):

        if self.pBeforeLineItem:
            menu = QMenu()
            menu.addAction(self.pInsertAnchorAction)
            menu.addAction(self.pDeleteAnchorAction)
            menu.exec(QCursor.pos())

    def itemChange(self, change, value):

        if change == QGraphicsItem.ItemPositionChange:
            self.notify()
        return QGraphicsItem.itemChange(self, change, value)

    def setBeforeLineItem(self, pItem):

        self.pBeforeLineItem = pItem

    def setAfterLineItem(self, pItem):

        self.pAfterLineItem = pItem

    def beforeLineItem(self):

        return self.pBeforeLineItem

    def slotInsertAnchorItem(self):

        assert (self.pBeforeLineItem)
        pos = self.pBeforeLineItem.middlePos()
        self.insertAnchorItem(pos, 0.0)

    def insertAnchorItem(self, pos, angel, ishidden =False):

        pItem = AnchorItem()
        pItem.setPos(pos)
        pItem.setRotation(angel)
        self.scene().addItem(pItem)
        pItem.setVisible(not ishidden)

        newLine = LineItem(pItem, self.pBeforeLineItem.endObserver())
        self.scene().addItem(newLine)

        pObserver = self.pBeforeLineItem.endObserver()
        pEndAnchorItem = pObserver
        if not pEndAnchorItem:
            pEndAnchorItem.setAfterLineItem(newLine)
        self.pBeforeLineItem.changeEndItem(pItem)
        pItem.setBeforeLineItem(newLine)
        pItem.setAfterLineItem(self.pBeforeLineItem)

    def slotDeleteAnchorItem(self):

        self.pAfterLineItem.changeEndItem(self.pBeforeLineItem.endObserver())
        if isinstance(self.pBeforeLineItem.endObserver(), AnchorItem):
            pAnchorItem = self.pBeforeLineItem.endObserver()
            pAnchorItem.setAfterLineItem(self.pAfterLineItem)
        self.pBeforeLineItem.release()
        self.scene().removeItem(self.pBeforeLineItem)
        self.scene().removeItem(self)
        # QObject.deleteLater(self)
        # QGraphicsItem.update()



class LineItem(Subject):

    def __init__(self, _pStartItem, _pEndItem):

        super().__init__()
        self.pStartItem = _pStartItem
        self.pEndItem = _pEndItem
        self.pStartItem.attach(self)
        self.pEndItem.attach(self)

    def release(self):

        self.pStartItem.detach(self)
        self.pEndItem.detach(self)

    def boundingRect(self):

        x1 = self.pStartItem.pos().x()
        y1 = self.pStartItem.pos().y()
        x2 = self.pEndItem.pos().x()
        y2 = self.pEndItem.pos().y()

        lx = min(x1, x2)
        rx = max(x1, x2)
        ty = min(y1, y2)
        by = max(y1, y2)

        width = rx - lx
        if width < 5:
            width = 5
        height = by - ty
        if height < 5:
            height = 5
        return QRectF(lx, ty, width, height + 100)

    def paint(self, painter, option, widget=None):

        painter.save()
        painter.setPen(QPen(Qt.DashLine))
        painter.drawLine(self.pStartItem.pos(), self.pEndItem.pos())
        painter.restore()
        painter.save()

        vec = QVector2D(self.pEndItem.pos() - self.pStartItem.pos())
        vec.normalize()
        norm = QVector2D(-vec.y(), vec.x())

        mid = QPointF(self.pStartItem.pos() / 2.0 + self.pEndItem.pos() / 2.0)
        mid_x = mid.x()
        mid_y = mid.y()
        vec_x = vec.x()
        vec_y = vec.y()
        norm_x = norm.x()
        norm_y = norm.y()
        pA = QPointF((mid_x + vec_x*5), (mid_y + vec_y*5))
        pD = QPointF((mid_x - vec_x*5), (mid_y - vec_y*5))
        pB = QPointF((mid_x - vec_x*5 + norm_x*5), (mid_y - vec_y*5 + norm_y*5))
        pC = QPointF((mid_x - vec_x*5 - norm_x*5), (mid_y - vec_y*5 - norm_y*5))
        pointList = [pA, pB, pC]

        polygonF = QPolygonF(pointList)
        brush = QBrush(Qt.green)
        painter.setBrush(brush)
        painter.drawPolygon(polygonF)
        painter.restore()

    def updateFromObserver(self, pObserve):

        # assert (pObserve == self.pStartItem or pObserve == self.pEndItem)
        self.update()

    def changeEndItem(self, pItem):

        self.pEndItem.detach(self)
        self.pEndItem = pItem
        self.pEndItem.attach(self)
        self.update()

    def changeStartItem(self, pItem):

        self.pStartItem.detach(self)
        self.pStartItem = pItem
        self.pStartItem.attach(self)
        self.update()

    def middlePos(self):

        return QPointF(self.pStartItem.pos() / 2.0 + self.pEndItem.pos() / 2.0)

    def endObserver(self):

        return self.pEndItem

    def startObserver(self):

        return self.pStartItem


class EclipseSite(Observer):
    path_ = []
    m_lineSize = 5
    m_color = QColor()

    def __init__(self, rx=10.0, ry=10.0):

        super(EclipseSite, self).__init__()
        self.m_rx = rx
        self.m_ry = ry

        self.setFlag(QGraphicsItem.ItemIsSelectable)
        self.setFlag(QGraphicsItem.ItemIsMovable)
        self.setFlag(QGraphicsItem.ItemSendsGeometryChanges)
        self.setFlag(QGraphicsItem.ItemSendsScenePositionChanges)
        self.pInsertAnchorAction = QAction('插入锚点', self.scene())
        self.pGenerateBezier = QAction('生成贝塞尔', self.scene())
        self.pGeneratePath = QAction('生成三段式', self.scene())
        self.pInsertAnchorAction.triggered.connect(self.slotInsertAnchorItem)
        self.pGenerateBezier.triggered.connect(self.slotGenerateBezier)
        self.pGeneratePath.triggered.connect(self.slotGeneratePath)

        self.pLineItem = None
        self.m_lineItem = {}
        self.isEnd = False
        self.prePathItem = None
        self.m_isBoundary = False
        self.entityName = ''
        self.id_ = sysinclude.EclipseSite_Id
        sysinclude.EclipseSite_Id += 1
        self.path_ = []

        self.outd = 50.0
        self.ind = 50.0
        self.outcl = 100.0
        self.incl = 100.0
        self.weight1 = 0.4
        self.weight2 = 0.3
        self.weight3 = 0.3



    def type(self):

        return sysinclude.ITEM_ECLIPSE_SITE

    def id(self):

        return self.id_

    def setId(self, id):

        self.id_ = id

    def boundingRect(self):

        rect = QRectF(0, 0, 2*self.m_rx+self.m_rx, 2*self.m_ry+self.m_ry)
        rect.moveCenter(QPointF(0.0, 0.0))
        return rect

    def paint(self, painter, option, widget):

        self.render(painter)

    def render(self, painter):

        painter.save()
        brush = QBrush(self.m_color)
        pen = QPen()
        painter.setPen(pen)
        painter.setBrush(brush)
        painter.drawEllipse(QPointF(0.0, 0.0), self.m_rx, self.m_ry)
        points = [QPointF(self.m_rx / 2, -self.m_ry - 2), QPointF(0, -self.m_ry - 3 * self.m_rx / 4 - 2), QPointF(-self.m_rx / 2, -self.m_ry - 2)]
        triangle = QPolygonF(points)
        painter.drawPolygon(triangle)
        painter.restore()

    def adjust(self, dirType, vec):

        if dirType == HelperItem.DIR_TOP:
            self.m_ry += -vec.y() / 2
            curPos = self.pos()
            curPos.setY(curPos.y() + vec.y() / 2)
            self.setPos(curPos)
        elif dirType == HelperItem.DIR_BOTTOM:
            self.m_ry += vec.y() / 2
            curPos = self.pos()
            curPos.setY(curPos.y() + vec.y() / 2)
            self.setPos(curPos)
        elif dirType == HelperItem.DIR_LEFT:
            self.m_rx += -vec.x() / 2
            curPos = self.pos()
            curPos.setX(curPos.x() + vec.x() / 2)
            self.setPos(curPos)
        elif dirType == HelperItem.DIR_RIGHT:
            self.m_rx += vec.x() / 2
            curPos = self.pos()
            curPos.setX(curPos.x() + vec.x() / 2)
            self.setPos(curPos)
        self.prepareGeometryChange()
        self.updateHelperItem()
        self.update()

    def exitEditState(self):

        pScene = self.scene()
        assert (pScene)
        items = []
        items = pScene.helperItems().copy()
        for i in range(len(items)):
            items[i].setVisible(False)

    def updateHelperItem(self):

        pScene = self.scene()
        if pScene == None:
            return
        items = pScene.helperItems()
        centers = self.calCenterForEachLine(self.boundingRect(), self.m_lineSize)
        for i in range(len(items)):
            rect = self.calSquareByWidth(self.m_lineSize)
            items[i].setRect(rect)
            sceneP = self.mapToScene(centers[i])
            items[i].setPos(sceneP)
            items[i].setEclipseSite(self)
            items[i].setVisible(True)

    def calCenterForEachLine(self, rect, linesize):

        top = QLineF(rect.topLeft(), rect.topRight())
        bottom = QLineF(rect.bottomLeft(), rect.bottomRight())
        left = QLineF(rect.topLeft(), rect.bottomLeft())
        right = QLineF(rect.topRight(), rect.bottomRight())

        fourCenters = []
        fourCenters.append(top.pointAt(0.5))
        fourCenters.append(bottom.pointAt(0.5))
        fourCenters.append(left.pointAt(0.5))
        fourCenters.append(right.pointAt(0.5))
        return fourCenters

    def calSquareByWidth(self, width):

        assert (width >= 1)
        rect = QRectF(0, 0, width, width)
        rect.moveCenter(QPointF(0.0, 0.0))
        return rect

    def mousePressEvent(self, event):

        if not self.isBoundary() and QApplication.mouseButtons() == Qt.LeftButton:
            self.updateHelperItem()
            cursor = QCursor()
            cursor.setShape(Qt.SizeAllCursor)
            self.setCursor(cursor)

        super().mousePressEvent(event)
        # QGraphicsItem.mousePressEvent(event)

    def mouseReleaseEvent(self, event):

        cursor = QCursor()
        cursor.setShape(Qt.ArrowCursor)
        self.setCursor(cursor)
        QGraphicsItem.mouseReleaseEvent(self, event)
        # QGraphicsItem.mouseReleaseEvent(event)

    # def wheelEvent(self, event):
    #
    #     event.setWidget(self.)
    #     event.setScenePos(self.mapToScene(event.pos()))
    #     wheelEvent = QGraphicsSceneEvent(QEvent.GraphicsSceneWheel)
    #     wheelEvent.widget(self.viewport())
    #     wheelEvent.scenePos(self.mapToScene(event.pos()))
    #     wheelEvent.screenPos(event.globalPos())
    #     wheelEvent.buttons(event.buttons())
    #     wheelEvent.modifiers(event.modifiers)
    #     wheelEvent.delta(event.delta())
    #     wheelEvent.orientation(event.orientation())
    #     wheelEvent.setAccepted(False)
    #     QApplication.sendEvent(self.scene(), wheelEvent)
    #     event.setAccepted(wheelEvent.isAccepted())

    def setLineItem(self, pItem, id):

        self.pLineItem = pItem
        self.m_lineItem[id] = pItem

    def getLineItem(self):

        return self.pLineItem

    def getLineItemMap(self):

        return self.m_lineItem

    def setEnd(self, isEnd):

        self.isEnd = isEnd

    def itemChange(self, change, value):

        if change == QGraphicsItem.ItemPositionHasChanged:
            self.updateHelperItem()
            return value
        if change == QGraphicsItem.ItemPositionChange:
            self.notify()
        return QGraphicsItem.itemChange(self, change, value)

    def contextMenuEvent(self, QGraphicsSceneContextMenuEvent):

        if self.pLineItem:
            menu = QMenu()
            menu.addAction(self.pInsertAnchorAction)
            menu.addAction(self.pGenerateBezier)
            menu.addAction(self.pGeneratePath)
            menu.exec_(QCursor.pos())


    def slotInsertAnchorItem(self):

        assert (self.pLineItem != None)
        pos = self.pLineItem.middlePos()
        self.insertAnchorItem(pos, 0.0)

    def insertAnchorItem(self, pos, angle, ishidden = False):

        pItem = AnchorItem()
        pItem.setPos(pos)
        pItem.setRotation(angle)
        self.scene().addItem(pItem)

        pItem.setVisible(not ishidden)
        newLine = LineItem(pItem, self.pLineItem.endObserver())
        self.scene().addItem(newLine)
        pObserver = self.pLineItem.endObserver()
        if isinstance(pObserver, AnchorItem):
            pEndAnchorItem = pObserver
            pEndAnchorItem.setAfterLineItem(newLine)
        newLine.setVisible(not ishidden)
        self.pLineItem.changeEndItem(pItem)
        pItem.setBeforeLineItem(newLine)
        pItem.setAfterLineItem(self.pLineItem)

    def generatePoints(self):

        andorPoints = []
        andorPoints.append(State(self.pos().x(), self.pos().y(), self.rotation()))
        pCurItem = self.pLineItem
        while pCurItem:
            pObserver = pCurItem.endObserver()
            # pItem = AnchorItem()
            # pItem = pObserver
            if isinstance(pObserver, AnchorItem):
                pItem = pObserver
                andorPoints.append(State(pItem.pos().x(), pItem.pos().y(), pItem.rotation()))
                pCurItem = pItem.beforeLineItem()
            else:
                item = pObserver
                andorPoints.append(State(item.pos().x(), item.pos().y(), item.rotation()))
                pCurItem = None
        return andorPoints

    def GeneratePath(self, weight1, weight2, weight3, outd, ind, outcl, incl):

        pathItem = None
        self.path_.clear()
        self.makepath(weight1, weight2, weight3, outd, ind, outcl, incl)
        if len(self.path_) <= 0:
            # QMessageBox.warning(self, '提示', '无合适运动路径', QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes)
            return
        path1 = QPainterPath()
        path1.moveTo(self.path_[0].x, self.path_[0].y)
        size = len(self.path_)
        for i in range(1, size):
            path1.lineTo(self.path_[i].x, self.path_[i].y)
        pen1 = QPen(QColor(34, 139, 34))
        # pen1 = QPen(Qt.green)
        pathItem = self.scene().addPath(path1, pen1)
        if self.prePathItem is not None:
            self.scene().removeItem(self.prePathItem)
            self.update()
        self.prePathItem = pathItem

    def slotGenerateBezier(self):

        s = self.scene()
        self.path_.clear()
        anchorPoints = self.generatePoints()
        pathPoints = []
        for i in range(1, len(anchorPoints)):
            pg = PathGeneration()
            retPL = pg.calPath(anchorPoints[i - 1], anchorPoints[i])
            pathPoints.extend(retPL)

        self.path_ = pathPoints.copy()
        pathItem = None
        if len(self.path_) <= 0:
            return
        path1 = QPainterPath()
        path1.moveTo(self.path_[0].x, self.path_[0].y)
        size = len(self.path_)
        for i in range(1, size):
            path1.lineTo(self.path_[i].x, self.path_[i].y)
        pen1 = QPen(Qt.black)
        pathItem = self.scene().addPath(path1, pen1)
        if self.prePathItem is not None:
            self.scene().removeItem(self.prePathItem)
            self.update()
        self.prePathItem = pathItem

    def slotGeneratePath(self):

        self.GeneratePath(self.weight1, self.weight2, self.weight3, self.outd, self.ind, self.outcl, self.incl)

    def makepath(self, weight1, weight2, weight3, outd, ind, outcl, incl):

        s = self.scene()
        anchorPoints = self.generatePoints()
        pathPoints = []
        for i in range(1, len(anchorPoints)):
            pi = pathInfo(anchorPoints[i - 1], anchorPoints[i], 40, 60, 1, 1, 15, 30, outd, ind, outcl, incl)
            pi.doPathDesign()
            pi.calculateOthers(s, weight1, weight2, weight3)
            if len(pi.valuablePathList) >= 1:
                p1 = pi.makePath()
                print("BestPathScore:", p1.pathScore, "PathLength:", p1.pathLength, "PassOccupiedNum:", p1.occupiedNum, "ActualMinRadius:", 1/p1.maxCurve)
                pathPoints.extend(p1.path)
                self.path_.extend(pathPoints)

    def getFirstState(self):
        assert (len(self.path_) > 0)
        return self.path_[0]

    def getColor(self):

        return self.m_color

    def getName(self):

        return self.entityName

    def setColor(self, color):

        self.m_color = color

    def setName(self, name):

        self.entityName = name

    def getAttributes(self):
        ret = []
        pair = Pair()
        pair.first = '位置'
        pair.second = '(%1, %2)'.format(self.pos().x(), self.pos().y())
        ret.append(pair)
        return ret

    def enableBoundary(self):

        self.m_isBoundary = True

    def isBoundary(self):

        return self.m_isBoundary

    def radiusX(self):

        return self.m_rx

    def radiusY(self):

        return self.m_ry

    def setWeight1(self, weight1):

        self.weight1 = weight1

    def setWeight2(self, weight2):

        self.weight2 = weight2

    def setWeight3(self, weight3):

        self.weight3 = weight3

    def setOutd(self, outd):

        self.outd = outd

    def setInd(self, ind):

        self.ind = ind

    def setOutcl(self, outcl):

        self.outcl = outcl

    def setIncl(self, incl):

        self.incl = incl

    def getWeight1(self):

        return self.weight1

    def getWeight2(self):

        return self.weight2

    def getWeight3(self):

        return self.weight3

    def getOutd(self):

        return self.outd

    def getInd(self):

        return self.ind

    def getOutcl(self):

        return self.outcl

    def getIncl(self):

        return self.incl



class EclipseObstacle_Rotation(Obstacle):

    # id_ = 1
    def __init__(self, rx, ry):
        super(EclipseObstacle_Rotation, self).__init__()
        self.m_rx = rx
        self.m_ry = ry
        self.id_ = 0

    def boundingRect(self):
        rect = QRectF(0, 0, 2.0 * self.m_rx + self.m_rx, 2.0 * self.m_ry + self.m_ry)
        rect.moveCenter(QPointF(0.0, 0.0))
        return rect

    def render(self, painter):
        painter.save()
        brush = QBrush(self.m_color)
        painter.setBrush(brush)
        painter.drawEllipse(QPointF(0.0, 0.0), self.m_rx, self.m_ry)
        points = [QPointF(self.m_rx / 2, -self.m_ry - 2), QPointF(0, -self.m_ry - 3 * self.m_rx / 4 - 2),
                  QPointF(-self.m_rx / 2, -self.m_ry - 2)]
        triangle = QPolygonF(points)
        painter.drawPolygon(triangle)

        painter.restore()

    def type(self):
        return ITEM_ECLIPSE_SITE_ROTATION

    def adjust(self, dirType, vec):
        pass

    def radiusX(self):
        return self.m_rx

    def radiusY(self):
        return self.m_ry

    def id(self):
        return self.id_

    def setId(self, id):
        self.id_ = id



class Pair():

    def __init__(self, first, second):
        self.first = first
        self.second = second



