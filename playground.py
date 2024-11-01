from direct.showbase.ShowBase import ShowBase

from panda3d.core import TextNode
from direct.interval.IntervalGlobal import *
from direct.gui.DirectGui import *
from direct.showbase.DirectObject import DirectObject
import sys
from direct.task import Task
from panda3d.core import PointLight, AmbientLight, NodePath
from direct.filter.CommonFilters import CommonFilters
from panda3d.core import Material, Point2
from math import cos, pi, sin

from direct.showbase.ShowBase import ShowBase
from direct.task import Task
from panda3d.core import (
    Geom,
    GeomNode,
    PandaNode,
    GeomTriangles,
    GeomVertexData,
    GeomVertexFormat,
    GeomVertexWriter,
    PlaneNode
)

format = GeomVertexFormat.getV3c4()
format = GeomVertexFormat.registerFormat(format)


class World(ShowBase):
    def genLabelText(self, text, i):
        return OnscreenText(text=text, pos=(0.06, -.06 * (i + 0.5)), fg=(1, 1, 1, 1),
                            parent=self.a2dTopLeft,align=TextNode.ALeft, scale=.05)

    def __init__(self):
        ShowBase.__init__(self)
        # self.disableMouse()
        # self.useDrive()
        # self.oobe()





        p = self.loader.loadModel('models/custom_box')
        p.reparentTo(self.render)
        tex = self.loader.loadTexture('models/polluted_earth_0.jpg')
        p.setTexture(tex,1)
        p.setPos(0,5,0)
        p.setHpr(0,90,0)

        p.setScale(1)
        # self.loader.loadModel('models/zup-axis').reparentTo(self.render)
        # box.setTexture(tex, 1)
        # box.reparentTo(render)
        # box.setPos(0,10,0)

w = World()
w.run()
