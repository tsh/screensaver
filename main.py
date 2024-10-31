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


class World(ShowBase):
    def genLabelText(self, text, i):
        return OnscreenText(text=text, pos=(0.06, -.06 * (i + 0.5)), fg=(1, 1, 1, 1),
                            parent=self.a2dTopLeft,align=TextNode.ALeft, scale=.05)

    def __init__(self):
        ShowBase.__init__(self)

        self.nodes = None
        self.camera_move = False

        self.lights = []
        self.light_tpl = '[L]: Toggle lights {state}'
        self.is_light = False
        self.setup_lights()

        # The standard camera position and background initialization
        self.setBackgroundColor(0, 0, 0)
        # self.disableMouse()
        self.x = 0
        self.y = -12
        self.z = 0
        self.cam.setPos(self.x, self.y, self.z)
        box = self.loader.loadModel('models/skybox_1024.egg')
        tex = self.loader.loadCubeMap('models/polluted_earth_#.jpg')
        box.setTexture(tex, 1)
        box.reparentTo(render)

        # self.scene_system()


        filters = CommonFilters(base.win, base.cam)
        filters.set_bloom()

        self.light_text = self.genLabelText(self.light_tpl.format(state=self.is_light), 1)
        self.scene_sun_text = self.genLabelText('[1] : Sun', 2)
        self.scene_system_text = self.genLabelText('[2] : System', 3)

        self.yearCounter = 0
        self.simRunning = True

        self.accept("escape", sys.exit)

        self.accept('l', self.toggle_light, [self.light_text])
        # self.toggle_light(self.light_text)
        # self.accept('arrow_left', self.handle_left)
        # self.accept('arrow_right', self.handle_right)
        # self.accept('arrow_up', self.handle_up)
        # self.accept('arrow_down', self.handle_down)
        self.accept('1', self.scene_sun)
        self.accept('2', self.scene_system)
        #
        self.taskMgr.add(self.set_camera_task, "set_camera_task")
        # self.taskMgr.add(self.debug_log, 'debug_log')

    def scene_system(self):
        self.reset()

        stars = NodePath('stars')
        sun = self.loader.loadModel("models/planet_sphere")
        # sun_tex = loader.loadTexture("models/sun_1k_tex.jpg")
        sun_tex = self.loader.loadTexture("models/8k_sun.jpg")
        sun.setTexture(sun_tex, 1)
        sun.setScale(3)
        sun.setPos(0, 0, 0)
        sun.reparentTo(stars)
        sun_rot = sun.hprInterval(20, (360, 0, 0))
        sun_rot.loop()
        stars.reparentTo(self.render)
        self.nodes = stars

        self.setBackgroundColor(0, 0, 0)
        self.x = 0
        self.y = -12
        self.z = 0
        self.cam.setPos(self.x, self.y, self.z)
        self.camera_move = True

    def reset(self):
        if self.nodes:
            self.nodes.removeNode()
        self.camera_move = False


    def is_visible_fast(self, pos):
        p1 = self.cam.getRelativePoint(self.render, pos)
        if not self.camLens.project(p1, Point2()):
            return False
        return True

    def is_visible(self, object):
        lensBounds = self.cam.node().getLens().makeBounds()
        bounds = object.getBounds()
        bounds.xform(object.getParent().getMat(self.cam))
        return bool(lensBounds.contains(bounds))


    def scene_sun(self):
        self.reset()

        stars = NodePath('stars')
        sun = self.loader.loadModel("models/planet_sphere")
        # sun_tex = loader.loadTexture("models/sun_1k_tex.jpg")
        sun_tex = self.loader.loadTexture("models/8k_sun.jpg")
        sun.setTexture(sun_tex, 1)
        sun.setScale(3)
        sun.setPos(0, 0, 0)
        sun.reparentTo(stars)

        s = Material()
        sun.setMaterial(s, 1)

        sun_rot = sun.hprInterval(20, (360, 0, 0))
        sun_rot.loop()
        stars.reparentTo(self.render)
        self.nodes = stars

        self.setBackgroundColor(0, 0, 0)
        self.x = 0
        self.y = -12
        self.z = 0
        self.cam.setPos(self.x, self.y, self.z)

    def debug_log(self, task):
        print(self.is_visible(self.nodes))
        return Task.cont

    def set_camera_task(self, task):
        if self.camera_move:
            self.y += 0.1
            self.camera.setPos(self.x, self.y, self.z)

            stars = NodePath('stars')
            pos = self.camera.getPos()
            interval = 100
            if pos.y % interval == 0:
                sun = self.loader.loadModel("models/planet_sphere")
                sun_tex = self.loader.loadTexture("models/sun_1k_tex.jpg")
                sun.setTexture(sun_tex, 1)
                sun.setScale(3)
                sun.setPos(pos.x, pos.y+interval, pos.z)
                sun_rot = sun.hprInterval(20, (360, 0, 0))
                sun_rot.loop()
                stars.reparentTo(self.render)
                sun.reparentTo(stars)
        return Task.cont

    def handle_left(self):
        self.x -= 1

    def handle_right(self):
        self.x += 1

    def handle_up(self):
        self.y += 1

    def handle_down(self):
        self.y -= 1

    def setup_lights(self):
        self.lightX = 0
        self.lightSpeed = 1

        alight = AmbientLight('alight')
        alight.setColor((0.2, 0.2, 0.2, 1))
        alnp = render.attachNewNode(alight)
        self.lights.append(alnp)


        plight = PointLight("plight")
        plight.setColor((1,1,1,1))
        plnp = self.render.attachNewNode(plight)
        plnp.setPos(10, 20, 0)
        self.lights.append(plnp)
        
        plight.setShadowCaster(True, 1024, 1024)
        self.render.setShaderAuto()


    def toggle_light(self, text):
        if self.is_light:
            for l in self.lights:
                render.clearLight(l)
        else:
            for l in self.lights:
                render.setLight(l)
        self.is_light = not(self.is_light)
        text.setText(self.light_tpl.format(state=self.is_light))



w = World()
w.run()