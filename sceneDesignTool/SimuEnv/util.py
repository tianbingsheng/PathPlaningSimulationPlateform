import sys
import os
import string
from PyQt5.QtGui import *
from PyQt5.QtCore import *
PI = 3.1415926

class Util:

    def __init__(self):
        pass

    @staticmethod
    def color2Long(color):
        return ((color.alpha() << 24) + (color.red() << 16) + (color.green() << 8) + color.blue())

    @staticmethod
    def long2Color(val):

        a = (val & 0xff000000) >> 24
        r = (val & 0x00ff0000) >> 16
        g = (val & 0x0000ff00) >> 8
        b = (val & 0x000000ff)
        return QColor(r, g, b, a)

    @staticmethod
    def Radian2Angle(radian):

        ret = radian / PI * 180
        while ret < 0 :
            ret += 360
        while ret > 360:
            ret -= 360
        return ret

    @staticmethod
    def pointF2String(point):

        str = ('(%1,%2)').format(point.x(), point.y())
        return str

    @staticmethod
    def String2PointF(str):

        x = ''
        y = ''
        tmp = ''
        for i in range(len(str)):
            if str[i] == ',':
                x = tmp
                tmp = ''
            elif str[i] != '(' and str[i] != ')':
                tmp += str[i]
        y = tmp
        return QPointF(float(x), float(y))


if __name__ == '__main__':
    app = Util()
    app.Radian2Angle(3.14)
    app.pointF2String(QPointF(2.5, 3.0))
    app.String2PointF('(2.5,3.0)')