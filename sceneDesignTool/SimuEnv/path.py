import sys
from SimuEnv import sysinclude
from SimuEnv.cartype import *
from PyQt5.QtCore import QPointF
from PyQt5.Qt import QColor
from SimuEnv.scene import EclipseSite

class Posture:


    def __init__(self, site = EclipseSite(10.0, 10.0), radian = 0.0):
        self.radian_ = radian
        self.site_ = site

class WayPoint:

    pos_ = QPointF()
    radian_ = ''
    # def __init__(self):
    #     self.radian_ = 0.0
    def __init__(self, pos = QPointF(0.0, 0.0), radian = 0.0):
        self.radian_ = radian
        self.pos_ = pos

class Path:

    def __init__(self):

        self.id_ = sysinclude.Path_id
        sysinclude.Path_id = sysinclude.Path_id + 1
        self.pCarType_ = None  # CarType()
        self.pStartItem_ = None  # EclipseSite()
        self.pEndItem_ = None
        self.pSceneStartItem_ = None
        self.pSceneEndItem_ = None

        self.start_ = Posture()
        self.end_ = Posture()
        self.name_ = ''
        self.color = QColor()
        self.WayPoints_ = []
        self.m_rotateAngle_ = ''

    def id(self):

        return self.id_

    def setId(self, id):

        self.id_ = id

    def setName(self, name):

        self.name_ = name

    def setStartPosAndAngle(self, site, radian):

        self.start_.site_ = site
        self.start_.radian_ = radian

    def setEndPosAndAngle(self, site, radian):

        self.end_.site_ = site
        self.end_.radian_ = radian

    def setColor(self, color):

        self.color = color

    def setRotateAngle(self, angle):

        self.m_rotateAngle_ = angle

    def rotateAngle(self):

        return self.m_rotateAngle_


    def getColor(self):

        return self.color

    def getStart(self):

        return self.start_

    def getEnd(self):

        return self.end_

    def getId(self):

        return self.id_

    def getName(self):

        return self.name_

    def getWayPoints(self):

        return self.WayPoints_

    def setWayPoints(self, list):

        self.WayPoints_ = list.copy()

    def boundingRect(self):

        return self.pStartItem_.boundingRect()

    def setStartItem(self, pItem):

        self.pStartItem_ = pItem

    def setEndItem(self, pItem):

        self.pEndItem_ = pItem

    def getStartItem(self):

        return self.pStartItem_

    def getEndItem(self):

        return self.pEndItem_

    def setSceneStartItem(self, pItem):

        self.pSceneStartItem_ = pItem

    def getSceneStartItem(self):

        return self.pSceneStartItem_

    def setSceneEndItem(self, pItem):

        self.pEndItem_ = pItem

    def getSceneEndItem(self):

        return self.pSceneEndItem_

