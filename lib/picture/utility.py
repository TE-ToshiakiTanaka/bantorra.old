from bantorra.util import define
from bantorra.util.log import Log

BASE_NAME = "Picture.Bantorra"
LOG = Log(BASE_NAME, True, "picture.log")

APP_TMP = define.APP_TMP
APP_LOG = define.APP_LOG

class POINT(object):
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height

    def __repr__(self):
        return "POINT()"

    def __str__(self):
        return "(X, Y) = (%s, %s), Width = %s, Height = %s" \
            % (self.x, self.y, self.width, self.height)
