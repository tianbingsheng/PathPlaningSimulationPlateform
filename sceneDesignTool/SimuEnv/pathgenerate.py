from PyQt5.QtCore import QPointF
import math
import numpy as np

class State:

    x = 0.0
    y = 0.0
    r = 0.0
    # def __init__(self):
    #
    #     self.x = 0.0
    #     self.y = 0.0
    #     self.r = 0.0

    # def __init__(self, pos, angle):
    #
    #     self.x = pos.x()
    #     self.y = pos.y()
    #     self.r = angle
    #
    def __init__(self, _x = 0.0, _y = 0.0, _r = 0.0):

        self.x = _x
        self.y = _y
        self.r = _r

class PathGeneration:

    def __init__(self):
        pass

    def calPath(self, start, end):

        distance = math.fabs(start.x - end.x) + math.fabs(start.y - end.y)
        andorPoints = []
        andorPoints.append(State(start.x, start.y))
        p1 = self.getPointByPointAndAngle(andorPoints[0], start.r - 90, distance/2.0)
        andorPoints.append(p1)
        p3 = State(end.x, end.y)
        p2 = self.getPointByPointAndAngle(p3, end.r - 90, -distance/2.0)
        andorPoints.append(p2)
        andorPoints.append(p3)

        return self.calBezierCurve(andorPoints)



    def getPointByPointAndAngle(self, point, degree, length):

        angle = degree * 3.1415926 / 180.0
        lengthY = math.sin(angle) * length
        lengthX = math.cos(angle) * length
        return State(point.x + lengthX, point.y + lengthY)


    def calBezierCurve(self, pointList):

        retList = []
        dt = 0.01
        for t in np.arange(0, 1+dt, dt):
            temp = self.pointOnCubicBezier(pointList, t)
            retList.append(temp)
        return retList

    def pointOnCubicBezier(self, pointlist, t):

        ret = State()
        cx = 3.0 * (pointlist[1].x - pointlist[0].x)  # 计算参数
        bx = 3.0 * (pointlist[2].x - pointlist[1].x) - cx
        ax = pointlist[3].x - pointlist[0].x - bx - cx
        cy = 3.0 * (pointlist[1].y - pointlist[0].y)
        by = 3.0 * (pointlist[2].y - pointlist[1].y) - cy
        ay = pointlist[3].y - pointlist[0].y - by - cy
        t_squared = t * t
        t_cubic = t_squared * t
        ret.x = ax * t_cubic + bx * t_squared + cx * t + pointlist[0].x
        ret.y = ay * t_cubic + by * t_squared + cy * t + pointlist[0].y
        derivative_y = 3 * ay * t_squared + 2 * by * t + cy
        derivative_x = 3 * ax * t_squared + 2 * bx * t + cx
        angle_x = math.atan2(derivative_y, derivative_x) * 180 / math.pi  # 弧度转化为角度，数学坐标系中与x轴正向的夹角
        # 以下转化为与场景坐标系中，Y轴负向的夹角[0,360)。因为设置的Y轴负向为图形项的旋转轴,夹角为0度，顺时针为正
        if angle_x >= -90.0 and angle_x <= 0:
            ret.r = 90.0 - math.fabs(angle_x)
        elif angle_x > 0 and angle_x <= 180:
            ret.r = 90.0 + angle_x
        else:  # angle_x > -180 and angle_x < -90
            ret.r = 360.0 - (math.fabs(angle_x) - 90.0)
        if math.fabs(ret.r) <= 1e-5:
            ret.r = 0
        return ret


