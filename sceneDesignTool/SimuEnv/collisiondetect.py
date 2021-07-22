from PyQt5.QtCore import *
from PyQt5.QtGui import *

class Node:
    rect = QRectF()
    pos = QPointF()
    angle = 0.0

class CollisionDetect:

    @staticmethod
    def isCollision(lh, rh):

        lpolygon = CollisionDetect.calPolygon(lh)
        rpolygon = CollisionDetect.calPolygon(rh)
        return lpolygon.intersected(rpolygon).size() > 0

    @staticmethod
    def calPolygon(node):

        transformLeft = QTransform()
        transformLeft.translate(node.pos.x(), node.pos.y())
        transformLeft.rotateRadians(node.angle)
        return transformLeft.map(QPolygonF(node.rect))