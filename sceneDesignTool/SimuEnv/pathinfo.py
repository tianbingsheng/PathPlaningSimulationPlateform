from PyQt5.QtCore import *
from SimuEnv.pathgenerate import *
from SimuEnv.scene import *
from SimuEnv.collisiondetect import *
# from SimuEnv.mainwindow import *
import math
import numpy as np

class pathList:
    def __init__(self):
        self.path = []
        self.pathScore = 0.0
        self.pathLength = 0.0
        self.length1 = 0.0
        self.length2 = 0.0
        self.length3 = 0.0
        self.barrierNum = 0
        self.occupiedNum = 0.0
        self.useTime = 0.0
        self.isBarried = False
        self.isOutBoundary = False
        self.isSatisfyKinematic = True
        self.maxCurve = 0.0
        self.maxCurveDerivative = 0.0
        self.averageCurveDerivative = 0.0
        self.rotationNumber = 0
        self.outPos = State()
        self.inPos = State()


class pathInfo:

    def __init__(self, start, end, cheLength, zhanLength, scale, speed, wheelBase, steering, outd, ind, outcl, incl):

        self.startPos = start
        self.endPos = end
        self.cheLength = cheLength
        self.minRadius = self.findMinRadius(wheelBase, steering)
        # self.distance = self.find_d(cheLength, zhanLength)*scale
        self.distance = outd
        self.distance2 = ind
        self.outcl = outcl
        self.incl = incl
        self.speed = speed
        self.rotationNum = 0
        self.allPathList = []
        self.valuablePathList = []
        self.outPoints = []
        self.inPoints = []
        self.startOutPos = State()
        self.endInPos = State()
        self.startOutPathPoint = []
        self.endInPathPoint = []
        self.middlePathPoint = []
        self.rotationPosList = {}
        self.smoothPosList = {}
        self.maxLength = 0.0
        self.maxTime = 0.0
        self.maxAverageCurveDerivative = 0.0
        self.maxOccupied = 0.0
        self.minOccupied = 0.0
        self.minLength = 0.0
        self.minTime = 0.0
        self.minaverageCurveDerivative = 0.0
        self.curveDerivativeList = []



    def findMinRadius(self, wheelBase, steering):

        minRadius = wheelBase/(math.sin(steering*PI/180))
        print('minRadius:', minRadius)
        return minRadius

    def find_d(self, cheLength, zhanLength):

        return ((zhanLength + cheLength)/2.0)

    def doPathDesign(self):

        self.allPathList.clear()
        self.outPoints = self.selectOutOrInPoints(self.startPos, self.minRadius, self.distance, 20)
        self.inPoints = self.selectOutOrInPoints(self.endPos, self.minRadius, self.distance2, 20)
        for o in self.outPoints:
            self.startOutPos = o
            for i in self.inPoints:
                self.endInPos = i
                self.startOutPathPoint = self.drawEllipse(self.startPos, self.startOutPos, self.distance, 20)
                self.endInPathPoint = self.drawEllipse(self.endPos, self.endInPos, self.distance2, 20)
                self.middlePathPoint = self.drawMiddleTransfer(self.startOutPos, self.endInPos, 100, self.outcl, self.incl)

                t = self.getCurveList(self.startOutPos, self.endInPos, 100, self.outcl, self.incl)
                maxCurve2 = self.calMaxCurvature(t)
                t2 = self.getCurveDerivativeList(self.startOutPos, self.endInPos, 100, self.outcl, self.incl)
                maxCurveDerivative2 = self.calMaxCurvature(t2)
                averageDerivate2 = self.getAverageCurveDerivative(t2)
                self.setMaxCurvePosList(t)

                pathInform = pathList()
                pathPoints = []
                pathPoints.extend(self.startOutPathPoint)
                pathPoints.extend(self.middlePathPoint)
                pathPoints.extend(self.reverserOrder(self.endInPathPoint))
                self.rotationNum += len(self.rotationPosList)

                length1 = self.calculatePathLength(self.startOutPathPoint, 1)
                length2 = self.calculatePathLength(self.middlePathPoint, len(self.rotationPosList))
                length3 = self.calculatePathLength(self.endInPathPoint, 1)
                length = length1 + length2 + length3
                time = length / self.speed
                # time = 0.0
                # partOutPos = self.changeToPart(self.startPos, self.startOutPos)
                # partInPos = self.changeToPart(self.endPos, self.endInPos)
                # if (partOutPos.y < 0) and (partInPos.y > 0) :
                #     time = length / self.speed
                # elif (partOutPos.y < 0) and (partInPos.y < 0):
                #     time = (length1 + length2 + length3 * 2) / self.speed
                # elif (partOutPos.y > 0) and (partInPos.y > 0):
                #     time = (length1 * 2 + length2 + length3) / self.speed
                # elif (partOutPos.y > 0) and (partInPos.y < 0):
                #     time = (length1 * 2 + length2 + length3 * 2) / self.speed
                pathInform.path.extend(pathPoints)
                pathInform.maxCurve = maxCurve2
                pathInform.maxCurveDerivative = maxCurveDerivative2
                pathInform.averageCurveDerivative = averageDerivate2
                ActualMinRadius = 1/pathInform.maxCurve
                print('ActualMinRadius:', ActualMinRadius)
                if (1/pathInform.maxCurve)>self.minRadius:
                    pathInform.isSatisfyKinematic = True
                else:
                    pathInform.isSatisfyKinematic = False
                pathInform.rotationNumber = self.rotationNum
                pathInform.length1 = length1
                pathInform.length2 = length2
                pathInform.length3 = length3
                pathInform.pathLength = length
                pathInform.useTime = time
                pathInform.outPos = o
                pathInform.inPos = i
                self.allPathList.append(pathInform)

                self.rotationNum = 0
                self.rotationPosList.clear()


    def calculateOthers(self, scene, weight1, weight2, weight3):

        if len(self.allPathList) > 0:
            # print('OccupiedNum:', len(scene.getOccupiedItemList()))
            # print('BarrierNum:', len(scene.getBarrierItemList()))
            for i in range(len(self.allPathList)):
                self.allPathList[i].occupiedNum = self.traversalPathPointsForOccupy(self.allPathList[i].path, scene.getOccupiedItemList(), scene.getEclipseSiteList()[0])
            for i in range(len(self.allPathList)):
                self.allPathList[i].isOutBoundary = self.isOutBoundary(self.allPathList[i].path, scene.getBoundary(), scene.getEclipseSiteList()[0])
            for i in range(len(self.allPathList)):
                if (self.traversalPathPointsForBarrier(self.allPathList[i].path, scene.getBarrierItemList(), scene.getEclipseSiteList()[0])) > 0:
                    self.allPathList[i].isBarried = True
                else:
                    self.allPathList[i].isBarried = False

            self.getValuablePath()
            for i in range(len(self.valuablePathList)):
                self.valuablePathList[i].pathScore = self.getPathScore(self.valuablePathList[i], scene.getBarrierItemList(), weight1, weight2, weight3)

    def traversalPathPointsForOccupy(self, pList, occupyItemList, ellipse):

        lh = Node()
        rh = Node()
        rh.rect = ellipse.boundingRect()
        num = 0
        collisionID = []
        for pstate in pList:
            rh.angle = pstate.r
            rh.pos = QPointF(pstate.x, pstate.y)
            for occupy in occupyItemList:
                lh.angle = occupy.rotation()
                lh.pos = occupy.pos()
                lh.rect = occupy.boundingRect()
                f = occupy.OccupiedID in collisionID
                if (CollisionDetect.isCollision(lh, rh)) and (not f):
                    num = num +1
                    collisionID.append(occupy.OccupiedID)
                    break
        return num

    def traversalPathPointsForBarrier(self, pList, barrierItemList, ellipse):

        lh = Node()
        rh = Node()
        rh.rect = ellipse.boundingRect()
        num = 0
        collisionID = []
        for pstate in pList:
            rh.angle = pstate.r
            rh.pos = QPointF(pstate.x, pstate.y)
            for obstacle in barrierItemList:
                lh.angle = obstacle.rotation()
                lh.pos = obstacle.pos()
                lh.rect = obstacle.boundingRect()
                f = obstacle.ObstacleID in collisionID
                if (CollisionDetect.isCollision(lh, rh)) and (not f):
                    num = num +1
                    collisionID.append(obstacle.ObstacleID)
                    break
        return num

    def isOutBoundary(self, pList, edge, ellipse):

        if  edge:
            b = True
            lh = Node()
            rh = Node()
            lh.angle = edge.rotation()
            lh.pos = edge.boundingRect().center()
            lh.rect = edge.boundingRect()
            lh.rect.translate(-lh.pos)
            rh.rect = ellipse.boundingRect()
            for pstate in pList:
                rh.angle = pstate.r
                rh.pos = QPointF(pstate.x, pstate.y)
                b = CollisionDetect.isCollision(lh, rh)
                if b == False:
                    return True
            return False
        return False

    def getPathScore(self, path, occupiedItemList, a, b, c):

        self.getMaxLength()
        self.getMaxTime()
        self.getMaxOccupied()
        self.getMaxAverageCurveDerivative()

        score = 0.0

        occupiedNum = path.occupiedNum
        # barrierNum = path.barrierNum
        pathLength = path.pathLength
        useTime = path.useTime
        averageCurveDerivative = path.averageCurveDerivative
        if occupiedItemList and (self.maxLength != self.minLength) and (self.maxOccupied != self.minOccupied) and (self.minaverageCurveDerivative != self.maxAverageCurveDerivative):
            score = 1 + (-(pathLength-self.minLength)/(self.maxLength-self.minLength))*a + (-(occupiedNum-self.minOccupied)/(self.maxOccupied-self.minOccupied))*b + (-(averageCurveDerivative-self.minaverageCurveDerivative)/(self.maxAverageCurveDerivative-self.minaverageCurveDerivative))*c
            return score
        elif occupiedItemList and (self.maxLength != self.minLength) and (self.maxOccupied == self.minOccupied) and (self.minaverageCurveDerivative != self.maxAverageCurveDerivative):
            score = 1 + (-(pathLength-self.minLength)/(self.maxLength-self.minLength))*a + (-(averageCurveDerivative-self.minaverageCurveDerivative)/(self.maxAverageCurveDerivative-self.minaverageCurveDerivative))*c
            return score
        elif (len(occupiedItemList) == 0) and (self.maxLength != self.minLength) and (self.minaverageCurveDerivative != self.maxAverageCurveDerivative):
            score = 1 + (-(pathLength-self.minLength)/(self.maxLength-self.minLength))*a + (-(averageCurveDerivative-self.minaverageCurveDerivative)/(self.maxAverageCurveDerivative-self.minaverageCurveDerivative))*c
            return score


    def getMaxLength(self):
        self.sortPathLength()
        self.maxLength = self.valuablePathList[0].pathLength
        self.minLength = self.valuablePathList[-1].pathLength

    def sortPathLength(self):

        for i in range(len(self.valuablePathList)):
            for j in range((len(self.valuablePathList)-i-1)):
                if self.valuablePathList[j].pathLength < self.valuablePathList[j+1].pathLength:
                    p = self.valuablePathList[j]
                    self.valuablePathList[j] = self.valuablePathList[j+1]
                    self.valuablePathList[j+1] = p

    def getMaxTime(self):

        self.sortPathTime()
        self.maxTime = self.valuablePathList[0].useTime
        self.minTime = self.valuablePathList[-1].useTime

    def sortPathTime(self):

        for i in range(len(self.valuablePathList)):
            for j in range((len(self.valuablePathList)-i-1)):
                if self.valuablePathList[j].useTime < self.valuablePathList[j+1].useTime:
                    p = self.valuablePathList[j]
                    self.valuablePathList[j] = self.valuablePathList[j+1]
                    self.valuablePathList[j+1] = p

    def getMaxAverageCurveDerivative(self):

        self.sortAverageCurveDerivative()
        self.maxAverageCurveDerivative = self.valuablePathList[0].averageCurveDerivative
        self.minaverageCurveDerivative = self.valuablePathList[-1].averageCurveDerivative

    def sortAverageCurveDerivative(self):

        for i in range(len(self.valuablePathList)):
            for j in range((len(self.valuablePathList)-i-1)):
                if self.valuablePathList[j].averageCurveDerivative < self.valuablePathList[j+1].averageCurveDerivative:
                    p = self.valuablePathList[j]
                    self.valuablePathList[j] = self.valuablePathList[j+1]
                    self.valuablePathList[j+1] = p
    def getMaxOccupied(self):

        self.sortPathOccupied()
        self.maxOccupied = self.valuablePathList[0].occupiedNum
        self.minOccupied = self.valuablePathList[-1].occupiedNum

    def sortPathOccupied(self):

        for i in range(len(self.valuablePathList)):
            for j in range((len(self.valuablePathList)-i-1)):
                if self.valuablePathList[j].occupiedNum < self.valuablePathList[j+1].occupiedNum:
                    p = self.valuablePathList[j]
                    self.valuablePathList[j] = self.valuablePathList[j+1]
                    self.valuablePathList[j+1] = p

    def makePath(self):

        self.sortScore()
        return self.valuablePathList[0]

    def sortScore(self):

        for i in range(len(self.valuablePathList)):
            for j in range((len(self.valuablePathList)-i-1)):
                if self.valuablePathList[j].pathScore < self.valuablePathList[j+1].pathScore:
                    p = self.valuablePathList[j]
                    self.valuablePathList[j] = self.valuablePathList[j+1]
                    self.valuablePathList[j+1] = p

    def getValuablePath(self):

        print('allPathList.size:', len(self.allPathList))

        for i in range(len(self.allPathList)):
            if (self.allPathList[i].isOutBoundary == False) and (self.allPathList[i].isBarried==False) and (self.allPathList[i].isSatisfyKinematic==True):
                self.valuablePathList.append(self.allPathList[i])
            # if (self.allPathList[i].isOutBoundary==False) and (self.allPathList[i].isSatisfyKinematic==True) and (self.allPathList[i].isBarried==False):
            #     self.valuablePathList.append(self.allPathList[i])

        print('valuablePathList.size:', len(self.valuablePathList))



    def selectOutOrInPoints(self, p, r, d, unitAngle):

        if d >= 2*r :
            angle1 = 0.0
            angle2 = 180.0
            angle3 = 180.0
            angle4 = 360.0
            l = []
            for i in np.arange(angle1, angle2, unitAngle):
                q = State()
                w = State()
                q.x = d * math.cos(i * PI / 180)
                q.y = d * math.sin(i * PI / 180)
                q.r = 2 * i - 90
                w = self.changeToGlobal(p, q)
                l.append(w)
            for i in np.arange(angle3, angle4, unitAngle):
                q = State()
                w = State()
                q.x = d * math.cos(i * PI / 180)
                q.y = d * math.sin(i * PI / 180)
                q.r = 2 * i - 450
                w = self.changeToGlobal(p, q)
                l.append(w)
            y = State(d * math.cos(angle4 * PI / 180), d * math.sin(angle4 * PI / 180), 2 * angle4 - 450)
            u = self.changeToGlobal(p, y)
            l.append(u)
            return l

        else:
            angle1 = (math.acos(d / (2 * r))) * 180 / PI
            angle2 = 180 - angle1
            angle3 = 180 + angle1
            angle4 = 360 - angle1
            l = []
            for i in np.arange(angle1, angle2, unitAngle):
                q = State()
                w = State()
                q.x = d * math.cos(i * PI / 180)
                q.y = d * math.sin(i * PI / 180)
                q.r = 2 * i - 90
                w = self.changeToGlobal(p, q)
                l.append(w)
            e = State(d * math.cos(angle2 * PI / 180), d * math.sin(angle2 * PI / 180), 2 * angle2 - 90)
            t = self.changeToGlobal(p, e)
            l.append(t)
            for i in np.arange(angle3, angle4, unitAngle):
                q = State()
                w = State()
                q.x = d * math.cos(i * PI / 180)
                q.y = d * math.sin(i * PI / 180)
                q.r = 2 * i - 450
                w = self.changeToGlobal(p, q)
                l.append(w)
            y = State(d * math.cos(angle4 * PI / 180), d * math.sin(angle4 * PI / 180), 2 * angle4 - 450)
            u = self.changeToGlobal(p, y)
            l.append(u)
            return l


    def changeToGlobal(self, o, p):

        q = State()
        t = o.r * PI /180
        q.x = o.x + p.x * math.cos(t) - p.y * math.sin(t)
        q.y = o.y + p.x * math.sin(t) + p.y * math.cos(t)
        q.r = p.r - 90 + o.r
        if q.r > 360:
            q.r -= 360
        if q.r < 0:
            q.r += 360

        return q

    def changeToPart(self, o, p):

        q = State()
        t = o.r * PI / 180
        q.x = (p.x - o.x) * math.cos(t) + (p.y - o.y) * math.sin(t)
        q.y = -(p.x - o.x) * math.sin(t) + (p.y - o.y) * math.cos(t)
        q.r = p.r - o.r + 90
        if q.r > 360:
            q.r -= 360
        if q.r < 0:
            q.r += 360
        return q


    def drawEllipse(self, s, o, d, number):

        o2 = self.changeToPart(s, o)
        span = qAbs(o2.r * PI / 180 - PI /2)
        t = span / 2
        radius = (d/2)/math.sin(t)

        list = []
        if o2.x > 0 and o2.y > 0:

            a = span/number
            for i in range(number):
                p = State()
                q = State()
                p.x = radius - radius * math.cos(a * i)
                p.y = radius * math.sin(a * i)
                p.r = (PI / 2 - a * i) * 180 /PI
                q = self.changeToGlobal(s, p)
                list.append(q)

        if o2.x < 0 and o2.y > 0:

            a = span/number
            for i in range(number):
                p = State()
                q = State()
                p.x = -(radius - radius * math.cos(a * i))
                p.y = radius * math.sin(a * i)
                p.r = (PI / 2 + a * i) * 180 /PI
                q = self.changeToGlobal(s, p)
                list.append(q)

        if o2.x < 0 and o2.y < 0:

            a = span/number
            for i in range(number):
                p = State()
                q = State()
                p.x = -(radius - radius * math.cos(a * i))
                p.y = -(radius * math.sin(a * i))
                p.r = (PI / 2 - a * i) * 180 /PI
                q = self.changeToGlobal(s, p)
                list.append(q)

        if o2.x > 0 and o2.y < 0:

            a = span/number
            for i in range(number):
                p = State()
                q = State()
                p.x = radius - radius * math.cos(a * i)
                p.y = -(radius * math.sin(a * i))
                p.r = (PI / 2 + a * i) * 180 /PI
                q = self.changeToGlobal(s, p)
                list.append(q)

        return list


    def reverserOrder(self, list):

        reOrder = []
        for i in reversed(list):
            reOrder.append(i)

        return reOrder


    def drawMiddleTransfer(self, o, i, n, outcl, incl):

        pointlist = self.pointSet(o, i, outcl, incl)
        cx = 3.0 * (pointlist[1].x - pointlist[0].x)  # 计算参数
        bx = 3.0 * (pointlist[2].x - pointlist[1].x) - cx
        ax = pointlist[3].x - pointlist[0].x - bx - cx
        cy = 3.0 * (pointlist[1].y - pointlist[0].y)
        by = 3.0 * (pointlist[2].y - pointlist[1].y) - cy
        ay = pointlist[3].y - pointlist[0].y - by - cy

        transfer = []
        dt = 1.0 / n
        for t in np.arange(0.0, 1.0+dt, dt):
            slop = (3*ay*t*t + 2*by*t + cy)/(3*ax*t*t + 2*bx*t + cx)
            ret = State()
            t_squared = t * t
            t_cubic = t_squared * t
            ret.x = ax * t_cubic + bx * t_squared + cx * t + pointlist[0].x
            ret.y = ay * t_cubic + by * t_squared + cy * t + pointlist[0].y
            ret.r = (math.atan(slop) + PI/2)*180/PI
            if ret.r > 360:
                ret -= 360
            if ret.r < 0:
                ret.r += 360
            transfer.append(ret)
        return transfer

    def getCurveList(self, o, i, n, outcl, incl):

        pointlist = self.pointSet(o, i, outcl, incl)
        cx = 3.0 * (pointlist[1].x - pointlist[0].x)  # 计算参数
        bx = 3.0 * (pointlist[2].x - pointlist[1].x) - cx
        ax = pointlist[3].x - pointlist[0].x - bx - cx
        cy = 3.0 * (pointlist[1].y - pointlist[0].y)
        by = 3.0 * (pointlist[2].y - pointlist[1].y) - cy
        ay = pointlist[3].y - pointlist[0].y - by - cy

        f2 = 6*bx*ay - 6*ax*by
        f1 = 6*ay*cx - 6*ax*cy
        f0 = 2*by*cx - 2*bx*cy

        g4 = 9*(ax*ax + ay*ay)
        g3 = 12*(ax*bx + ay*by)
        g2 = 6*(ax*cx + ay*cy) + 4*(bx*bx + by*by)
        g1 = 4*(bx*cx + by*cy)
        g0 = cx*cx + cy*cy

        curveList = []
        dt = 1.0 / n
        for t in np.arange(0.0, 1.0+dt, dt):
            fx = qAbs(f2*t*t + f1*t + f0)
            gx2 = g4*t*t*t*t + g3*t*t*t + g2*t*t + g1*t +g0
            gx = math.pow(gx2, 3.0*0.5)
            t2 = fx/gx
            curveList.append(t2)

        return curveList

    def getCurveDerivativeList(self, o, i, n, outcl, incl):

        pointlist = self.pointSet(o, i, outcl, incl)
        cx = 3.0 * (pointlist[1].x - pointlist[0].x)  # 计算参数
        bx = 3.0 * (pointlist[2].x - pointlist[1].x) - cx
        ax = pointlist[3].x - pointlist[0].x - bx - cx
        cy = 3.0 * (pointlist[1].y - pointlist[0].y)
        by = 3.0 * (pointlist[2].y - pointlist[1].y) - cy
        ay = pointlist[3].y - pointlist[0].y - by - cy

        f2 = 6*bx*ay - 6*ax*by
        f1 = 6*ay*cx - 6*ax*cy
        f0 = 2*by*cx - 2*bx*cy

        g4 = 9*(ax*ax + ay*ay)
        g3 = 12*(ax*bx + ay*by)
        g2 = 6*(ax*cx + ay*cy) + 4*(bx*bx + by*by)
        g1 = 4*(bx*cx + by*cy)
        g0 = cx*cx + cy*cy

        curveDerivativeList = []
        dt = 1.0 / n
        for t in np.arange(0.0, 1.0+dt, dt):
            fx = qAbs(f2*t*t + f1*t + f0)
            gx2 = g4*t*t*t*t + g3*t*t*t + g2*t*t + g1*t +g0
            gx = math.pow(gx2, 3.0*0.5)
            t2 = fx/gx
            fx_2 = (2*f2*t+f1)*gx - (f2*t*t+f1*t+f0)*1.5*pow(gx2,0.5)*(4*g4*t*t*t+3*g3*t*t+2*g2*t+g1)
            gx_2 = pow(gx,2)
            t3 = abs(fx_2/gx_2)
            curveDerivativeList.append(t3)

        return curveDerivativeList

    def calMaxCurvature(self, t):

        l = 0
        for i in range(len(t)):
            if t[l] <= t[i]:
                l = i
        return t[l]

    def getAverageCurveDerivative(self, t):
        sum = 0.0
        for i in range(len(t)):
            sum = sum + t[i]
        average = sum/len(t)
        return average

    def setMaxCurvePosList(self, t):

        start = False
        for i in range(len(t)-1):
            if (t[i+1] >= t[i]) and (not start):
                start = True
            elif (t[i+1] < t[i]) and start:
                start = False
                self.rotationPosList.update(i=self.middlePathPoint[i])

    def setMinCurvePosList(self, t):

        start = False
        for i in range(len(t - 1)):
            if (t[i + 1] <= t[i]) and (not start):
                start = True
            elif (t[i + 1] > t[i]) and start:
                start = False
                self.smoothPosList.update(i=self.middlePathPoint[i])





    def pointSet(self, o, i, outcl, incl):

        # distance = math.fabs(o.x - i.x) + math.fabs(o.y - i.y)
        andorPoints = []
        andorPoints.append(State(o.x, o.y))
        # p1 = self.selectControlPoints(andorPoints[0], o.r - 90, distance / 2.0)
        p1 = self.selectControlPoints(andorPoints[0], o.r - 90, outcl)
        andorPoints.append(p1)
        p3 = State(i.x, i.y)
        # p2 = self.selectControlPoints(p3, i.r - 90, -distance / 2.0)
        p2 = self.selectControlPoints(p3, i.r - 90, -incl)
        andorPoints.append(p2)
        andorPoints.append(p3)
        return andorPoints


    def selectControlPoints(self, p, degree, length):

        angle = degree * PI / 180.0
        lengthY = math.sin(angle) * length
        lengthX = math.cos(angle) * length
        return State(p.x + lengthX, p.y + lengthY)

    def calculateLength(self, s1, s2):

        length = math.sqrt((s1.x - s2.x)*(s1.x -s2.x) + (s1.y - s2.y)*(s1.y - s2.y))
        return length

    def calculatePathLength(self, pathPoints, n):

        length1 = 0.0
        for i in range(len(pathPoints)-1):
            temp = self.calculateLength(pathPoints[i], pathPoints[i+1])
            length1 += temp
        length = length1*math.pow(1.0, n)
        return length







