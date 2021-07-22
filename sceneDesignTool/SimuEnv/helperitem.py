import sys
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

# from SimuEnv import obstacle
from SimuEnv import sysinclude

class HelperItem(QGraphicsRectItem):

    DIR_TOP = 0
    DIR_BOTTOM = 1
    DIR_LEFT = 2
    DIR_RIGHT = 3

    def __init__(self, rect, _dir):

        super(HelperItem, self).__init__(rect)
        self.m_dir = _dir
        self.m_pObs = None
        self.m_pESObs = None
        self.oldPos = QPointF()
        self.m_flag = -1
        self.setBrush(QBrush(Qt.blue))
        self.setAcceptHoverEvents(True)
        self.setFlags(QGraphicsItem.ItemIsSelectable)
        self.setFlags(QGraphicsItem.ItemIsMovable)
        self.setZValue(1000)

    def hoverEnterEvent(self, event):

        cursor = QCursor()
        if self.m_dir == self.DIR_TOP or self.m_dir == self.DIR_BOTTOM:
            cursor.setShape(Qt.SizeVerCursor)
            self.setCursor(cursor)
        else:
            cursor.setShape(Qt.SizeHorCursor)
            self.setCursor(cursor)
        if self.m_flag == sysinclude.ITEM_ECLIPSE_SITE:
            self.m_pESObs.setFlag(QGraphicsItem.ItemIsMovable, False)
        else:
            self.m_pObs.setFlag(QGraphicsItem.ItemIsMovable, False)
        self.oldPos = self.pos()

    def hoverLeaveEvent(self, event):

        cursor = QCursor()
        cursor.setShape(Qt.ArrowCursor)
        self.setCursor(cursor)
        if self.m_flag == sysinclude.ITEM_ECLIPSE_SITE:
            self.m_pESObs.setFlag(QGraphicsItem.ItemIsMovable, True)
        else:
            self.m_pObs.setFlag(QGraphicsItem.ItemIsMovable, True)

    def mouseReleaseEvent(self, event):

        QGraphicsItem.mouseReleaseEvent(self, event)
        # print('self.pos().x(), self.pos().y():')
        # print(self.pos().x(), self.pos().y())
        # print('self.oldPos.x(), self.oldPos.y():')
        # print(self.oldPos.x(), self.oldPos.y())
        vec = QPointF(self.pos().x()-self.oldPos.x(), self.pos().y()-self.oldPos.y())
        # print('vec.x(),vec.y():')
        # print(vec.x(),vec.y())
        if self.m_flag == sysinclude.ITEM_ECLIPSE_SITE:
            self.m_pESObs.adjust(self.dir(), vec)
        else:
            self.m_pObs.adjust(self.dir(), vec)
        self.oldPos = self.pos()


    def dir(self):

        return self.m_dir

    def setObstacle(self, pObj):

        self.m_pObs = pObj


    def setEclipseSite(self, pObj):

        self.m_flag = sysinclude.ITEM_ECLIPSE_SITE
        self.m_pESObs = pObj
        # print('m_pESObsType:')
        # print(type(self.m_pESobs))


# if __name__ == '__main__':
#     app = QApplication(sys.argv)
#     main = HelperItem()
#     sys.exit(app.exec_())


