# from PyQt5.QtCore import *
from PyQt5.QtGui import QColor
# from enum import Enum


ITEM_RECT = int(1) #int(1), # 矩形
ITEM_RECT_OCCUPIED = int(11)  #站位
ITEM_ECLIPSE = int(2) #int(2), # 椭圆
ITEM_POLYGON = int(3) #int(3), # 多边形
ITEM_POLYGON_EDGE = int(4) #int(4), # 多边形边界
ITEM_ECLIPSE_SITE = int(5) #int(5), # 圆形起点 / 终点
ITEM_ECLIPSE_SITE_ROTATION = int(6) #int(6), # 带有方向的圆形起点 / 终点

EclipseSite_Id = 0
# EclipseSite_Id = 1
Path_id = 1
lightBlue = QColor(180, 250, 255)
