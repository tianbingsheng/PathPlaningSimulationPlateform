from PyQt5.QtCore import QCryptographicHash

class CarType:

    uuid = ''
    # def __init__(self):
    #     self.name_ = '新建车辆'
    #     self.length_ = 4.0
    #     self.width_ = 2.0
    #     self.height_ = 2.0
    #     self.maxAccelerate = 10.0
    #     self.maxVelocity = 20.0

    def __init__(self, length, width, height, maxAccelerate, maxVelocity):
        self.name_ = '新建车辆'
        self.length_ = length
        self.width_ = width
        self.height_ = height
        self.maxAccelerate = maxAccelerate
        self.maxVelocity = maxVelocity

    def getName(self):

        return self.name_

    def getWidth(self):

        return self.width_

    def getHeight(self):

        return self.height_

    def getLength(self):

        return self.length_

    def getMaxAccelerate(self):

        return self.maxAccelerate

    def getMaxVelocity(self):

        return self.maxVelocity

    def setWidth(self, width):

        self.width_ = width

    def setHeight(self, height):

        self.height_ = height

    def setLength(self, length):

        self.length_ = length

    def setMaxAcc(self, maxAccelerate):

        self.maxAccelerate = maxAccelerate

    def setMaxVelocity(self, maxVelocity):

        self.maxVelocity = maxVelocity

    def setName(self, name):

        self. name_ = name

    def setUuid(self, uuid):

        self.uuid = uuid

    def getUuid(self):

        return self.uuid
