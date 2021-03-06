import pygame
import pymunk
import pymunk.pygame_util
import random as r
import noise

from math import degrees


height = 500
width = 700
screenSizes = (height, width)


space = pymunk.Space()
space.gravity = 0, -9.8
fps = 40
sSpeed = 10
steps = 50*sSpeed
carNomSpeed = 2

mfps = 100


# colors
fWhite = (250, 250, 250)
white = (255, 255, 255)
black = (10, 10, 10)
red = (250, 0, 0)
green = (0, 250, 0)
blue = (0, 0, 250)
grassCol = (126, 200, 80)
skyCol = (135, 206, 235)
lightGround = (202, 189, 102)
lightGroundD = (152, 139, 52)

# images
tire = pygame.image.load("res/crc.png")
chasis = pygame.image.load("res/chasis.png")


class App:

    def __init__(self, sL=700, sH=240, aL=10000, aH=240):
        pygame.init()
        self.screenSize = (sL, sH)
        self.screen = pygame.display.set_mode(self.screenSize)
        self.atulSize = (aL, aH)
        self.backGround = pygame.Surface(self.atulSize)
        self.drawOptions = pymunk.pygame_util.DrawOptions(self.backGround)
        self.drawOptions.flags = pymunk.SpaceDebugDrawOptions.DRAW_SHAPES
        self.running = True
        self.clock = pygame.time.Clock()
        self.custEvent = None

    def spritHand(self, img, bdy, size=None):
        imgRot = img
        if not size == None:
            spt = pygame.transform.scale(img, size)
            imgRot = spt
        spt = pygame.transform.rotate(imgRot, degrees(bdy.angle))
        rect = spt.get_rect()
        rect.center = (bdy.position[0], self.screenSize[1]-bdy.position[1])
        self.backGround.blit(spt, rect)

    def terrainDraw(self, terr):
        # ground

        for j in range(terr.stPnt, terr.edPnt):
            xoff = terr.rstPnt*10
            recPoint = [(terr.tLis[j][0]-xoff, 500-terr.tLis[j][1]), (terr.tLis[j+1][0] - xoff,
                                                                      500-terr.tLis[j+1][1]), (terr.tLis[j+1][0]-xoff, 700), (terr.tLis[j][0]-xoff, 700)]
            te1 = pygame.draw.polygon(self.backGround, lightGround, recPoint)
            self.grad(lightGroundD, lightGround, recPoint,
                      forcedHeight=30, stepDraw=3)

    def event_handler(self, event):
        global sSpeed
        if event.type == pygame.QUIT:
            self.running = False
            pygame.image.save(self.backGround, 'intro.png')
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_i:
                sSpeed = sSpeed+1
            elif event.key == pygame.K_d:
                sSpeed = sSpeed-1
            elif event.key == pygame.K_s:
                sSpeed = 1
            elif event.key == pygame.K_f:
                sSpeed = 10

    def grad(self, stCol, edCol, polInfo, stepDraw=2, forcedHeight=0):
        if forcedHeight == 0:
            height = (min(polInfo[2][1], polInfo[3][1]) -
                      max(polInfo[0][1], polInfo[1][1]))
        else:
            height = forcedHeight
        sr, sg, sb = stCol
        er, eg, eb = edCol
        stp = 1/height
        colStp = ((er-sr)*stp, (eg-sg)*stp, (eb-sb)*stp)
        col = stCol
        height = int(round(height))+1
        for i in range(0, height, stepDraw):
            pygame.draw.polygon(self.backGround, col, [(polInfo[0][0], polInfo[0][1]+i), (polInfo[1][0], polInfo[1]
                                                                                          [1]+i), (polInfo[1][0], polInfo[1][1]+i+stepDraw), (polInfo[0][0], polInfo[0][1]+i+stepDraw)])
            col = (col[0]+colStp[0]*stepDraw, col[1]+colStp[1]
                   * stepDraw, col[2]+colStp[2]*stepDraw)

    def run(self):
        global mfps
        camera = pygame.Vector2(0, 0)
        while self.running:
            temp = pygame.event.get()
            self.screen.fill((250, 250, 250))
            self.backGround.fill(skyCol)
            # space.debug_draw(self.drawOptions)

            
            if not self.custEvent == None:
                self.custEvent(temp, camera)
            for event in temp:
                self.event_handler(event)

            self.screen.blit(self.backGround, camera)
            pygame.display.set_caption(
                "fps: {:.1f}".format(self.clock.get_fps()))

            pygame.display.update()

            self.clock.tick(fps)
            for i in range(steps):
                space.step(sSpeed/fps/steps)
            # if mfps == 0.0:
            #     mfps = 100
            # mfps = min(mfps,self.clock.get_fps())
            # print("fps:",self.clock.get_fps(),mfps)


class Car:

    def __init__(self, pos, weight=10, inSpeed=0, wheelW=10, whElast=0.2, whFric=0.9, wheelSF=10, wheelSB=10, wheelM=1, moment=100, color=skyCol, chSize=(100, 50), whstiff=14, whdamp=5):

        self.whSb = self.whSf = self.whoff = 13
        

        self.ls = []

        # car air status
        self.carAirLas = True
        self.carAirCurr = True

        # torque needed to apply
        self.torqNeed = 0

        # car Chasis
        self.carBody = pymunk.Body(weight, moment)
        self.carBody.position = pos
        self.carVertex = [(-chSize[0]/2, -chSize[1]/2), (-chSize[0]/2, 5),
                          (chSize[0]/2, 5), (chSize[0]/2, -chSize[1]/2)]
        self.chs = pymunk.Poly(self.carBody, (self.carVertex))
        self.chs.color = color
        self.chs.elasticity = 0.1
        self.chs.friction = 0.9
        self.ls.append((self.carBody, self.chs))

        # car Front Wheel
        self.whBdyF = pymunk.Body(wheelW, moment=wheelM)
        self.whBdyF.position = pos[0] + \
            (chSize[0]/2)-self.whoff, pos[1]+(-chSize[1]/2)-2*wheelSF
        self.wShapeF = pymunk.Circle(self.whBdyF, self.whSf)
        self.wShapeF.elasticity = whElast
        self.wShapeF.friction = whFric
        self.fwJntG = pymunk.constraint.GrooveJoint(
            self.carBody, self.whBdyF, ((chSize[0]/2)-self.whoff, -chSize[1]/2), ((chSize[0]/2)-self.whoff, (-chSize[1]/2)-(2*wheelSF)), (0, 0))
        self.fwJntS = pymunk.constraint.DampedSpring(self.carBody, self.whBdyF, ((
            chSize[0]/2)-self.whoff, -chSize[1]/2), (0, 0), 2*wheelSF, whstiff, whdamp)

        self.ls.append((self.whBdyF, self.wShapeF, self.fwJntG, self.fwJntS))

        # car Back Wheel
        self.whBdyB = pymunk.Body(wheelW, moment=10)
        self.whBdyB.position = pos[0] + \
            (-chSize[0]/2)+self.whoff, pos[1]+(-chSize[1]/2)-2*wheelSB
        self.wShapeB = pymunk.Circle(self.whBdyB, self.whSb)
        self.wShapeB.elasticity = whElast
        self.wShapeB.friction = whFric
        self.bwJntG = pymunk.constraint.GrooveJoint(
            self.carBody, self.whBdyB, ((-chSize[0]/2)+self.whoff, -chSize[1]/2), ((-chSize[0]/2)+self.whoff, (-chSize[1]/2)-(2*wheelSB)), (0, 0))
        self.bwJntS = pymunk.constraint.DampedSpring(self.carBody, self.whBdyB, ((
            -chSize[0]/2)+self.whoff, -chSize[1]/2), (0, 0), 2*wheelSB, whstiff, whdamp)
        self.bwmot = pymunk.constraint.SimpleMotor(
            self.whBdyB, space.static_body, inSpeed)
        self.ls.append((self.whBdyB, self.wShapeB, self.bwJntG, self.bwJntS))

        self.bwJntG.max_force = 1000
        self.fwJntG.max_force = 1000

        spFil = pymunk.ShapeFilter(1)
        self.chs.filter = spFil
        self.wShapeB.filter = self.wShapeF.filter = spFil

        # space object add
        space.add(self.ls)

    def carTransp(self, xPos):
        bwPos = self.carBody.position[0]-self.whBdyB.position[0]
        fwPos = self.carBody.position[0]-self.whBdyF.position[0]
        constr = [self.bwJntG, self.fwJntG, self.bwJntS, self.fwJntS]
        space.remove(constr)
        carVel = self.carBody.velocity
        whVel = self.whBdyB.velocity, self.whBdyF.velocity
        self.carBody.position = (xPos, self.carBody.position[1])
        self.whBdyB.position = (xPos - bwPos, self.whBdyB.position[1])
        self.whBdyF.position = (xPos - fwPos, self.whBdyF.position[1])
        self.carBody.velocity = carVel
        self.whBdyB.velocity = whVel[0]
        self.whBdyF.velocity = whVel[1]
        space.add(constr)

    def air_land_trans(self, a2l):
        if a2l:
            if self.torqNeed != 0:
                space.add(self.bwmot)
                if self.torqNeed < 0:
                    self.bwmot.rate = 2
                else:
                    self.bwmot.rate = -2
                self.torqNeed = 0
        else:
            if self.motChk():
                if self.bwmot.rate > 0:
                    self.torqNeed = -2000000
                else:
                    self.torqNeed = 2000000
                space.remove(self.bwmot)

    def motChk(self):
        for i in space.constraints:
            if i == self.bwmot:
                return True
        return False

    def carMov(self, dir):

        if dir == 0:
            self.torqNeed = 0
            if self.motChk():
                space.remove(self.bwmot)

        elif self.carAirCurr:
            if dir == 1:
                self.torqNeed = -2000000
            elif dir == -1:
                self.torqNeed = 2000000
        else:
            for i in space.constraints:
                if i == self.bwmot:
                    break
            else:
                space.add(self.bwmot)
            if dir == 1:
                self.bwmot.rate = carNomSpeed
            elif dir == -1:
                self.bwmot.rate = -carNomSpeed

    def carDes(self):
        space.remove(self.ls)


class Terrain:

    def __init__(self, octaves=1, lacunarity=2, persistence=0.5, friction=0.9, elasticity=0.5, color=grassCol):
        self.stPnt = 0
        self.rstPnt = 0
        self.offSet = 0
        self.edPnt = 300
        self.octave = octaves
        self.lacan = lacunarity
        self.persis = persistence
        self.tLis = self.terra()
        self.fric = friction
        self.elas = elasticity
        self.currSps = []
        self.color = color
        self.terraDraw()

    def terra(self):
        ls = []

        for i in range(0+self.offSet, 21100+self.offSet, 10):
            jt = (noise.pnoise1(i/1000, octaves=self.octave,
                                lacunarity=self.lacan, persistence=self.persis))
            j = jt*100+100
            ls.append((i, j))
        return ls[:2100]

    def terraDraw(self):
        self.currSps.clear()
        for j in range(self.stPnt, self.edPnt):
            xoff = self.rstPnt*10
            seg = pymunk.Segment(
                space.static_body, (self.tLis[j][0]-xoff, self.tLis[j][1]), (self.tLis[j+1][0]-xoff, self.tLis[j+1][1]), 5)
            seg.friction = self.fric
            seg.elasticity = self.elas
            seg.color = self.color
            self.currSps.append(seg)
        space.add(self.currSps)

    def terrUpdate(self):
        self.stPnt += 200
        self.rstPnt += 200
        self.edPnt += 200
        if(self.stPnt == 1800):
            self.terrUpdateHelp()
        print(self.stPnt, self.edPnt)
        space.remove(self.currSps)
        self.terraDraw()

    def terrUpdateHelp(self):
        self.stPnt = 0
        self.edPnt = 300
        self.offSet = self.tLis[-1][0]
        self.tLis = self.tLis[1800:]
        self.tLis = self.tLis + self.terra()[:1800]
        