class MicroMock(object):
    def __init__(self, iDict = None, **kwargs):
        if iDict:
            self.__dict__.update(iDict)
        self.__dict__.update(kwargs)