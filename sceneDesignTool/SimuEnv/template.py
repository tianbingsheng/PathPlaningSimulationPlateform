class Template:

    MODE_PHYSIC = 1
    MODE_PIXEL = 2

    def __init__(self):

        self.templateName = None
        self.remark = None
        self.mode = None
        self.scale = None


    def getTemplateName(self):

        return self.templateName

    def getRemark(self):

        return self.remark

    def getMode(self):

        return self.mode

    def getScale(self):

        return self.scale

    def setTemplateName(self, _templateName):

        self.templateName = _templateName

    def setRemark(self, _remark):

        self.remark = _remark

    def setMode(self, mode):

        self.mode = mode

    def setScale(self, scale):

        self.scale = scale



