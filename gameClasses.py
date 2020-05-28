import pygame
import pymunk
import pymunk.pygame_util
import random as r


space = pymunk.Space()
space.gravity = 0, -9.8
fps = 30
sSpeed = 10
steps = 50*sSpeed


class App:

    def __init__(self, sL=700, sH=240, aL=10000, aH=240):
        pygame.init()
        self.screenSize = (sL, sH)
        self.screen = pygame.display.set_mode(self.screenSize)
        self.atulSize = (aL, aH)
        self.backGround = pygame.Surface(self.atulSize)
        self.drawOptions = pymunk.pygame_util.DrawOptions(self.backGround)
        self.running = True
        self.clock = pygame.time.Clock()
        self.custEvent = None

    def event_handler(self, event):
        global sSpeed
        if event.type == pygame.QUIT:
            self.running = False
            pygame.image.save(self.screen, 'intro.png')
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_i:
                sSpeed = sSpeed+1
            elif event.key == pygame.K_d:
                sSpeed = sSpeed-1
            elif event.key == pygame.K_s:
                sSpeed = 1
            elif event.key == pygame.K_f:
                sSpeed = 10

    def run(self):
        camera = pygame.Vector2(0, 0)
        while self.running:
            temp = pygame.event.get()

            for event in temp:
                self.event_handler(event)
            if not self.custEvent == None:
                self.custEvent(temp, camera)

            self.screen.fill((250, 250, 250))
            self.backGround.fill((250, 250, 250))
            space.debug_draw(self.drawOptions)
            self.screen.blit(self.backGround, camera)
            pygame.display.update()

            self.clock.tick(fps)
            for i in range(steps):
                space.step(sSpeed/fps/steps)


class Car:

    def __init__(self, pos, weight=10, inSpeed=0, wheelW=10, whElast=0.2, whFric=0.9, wheelS=10, wheelM=1, moment=100, color=(200, 200, 250), chSize=(100, 50), whstiff=14, whdamp=5):

        self.ls = []

        # car Chasis
        self.carBody = pymunk.Body(weight, moment)
        self.carBody.position = pos
        self.carVertex = [(-chSize[0]/2, -chSize[1]/2), (-chSize[0]/2, chSize[1]/2),
                          (chSize[0]/2, chSize[1]/2), (chSize[0]/2, -chSize[1]/2)]
        self.chs = pymunk.Poly(self.carBody, (self.carVertex))
        self.chs.color = color
        self.chs.elasticity = 0.1
        self.chs.friction = 0.9
        self.ls.append((self.carBody, self.chs))

        # car Front Wheel
        self.whBdyF = pymunk.Body(wheelW, moment=wheelM)
        self.whBdyF.position = pos[0] + \
            (chSize[0]/2)-10, pos[1]+(-chSize[1]/2)-2*wheelS
        self.wShapeF = pymunk.Circle(self.whBdyF, wheelS)
        self.wShapeF.elasticity = whElast
        self.wShapeF.friction = whFric
        self.fwJntG = pymunk.constraint.GrooveJoint(
            self.carBody, self.whBdyF, ((chSize[0]/2)-10, -chSize[1]/2), ((chSize[0]/2)-10, (-chSize[1]/2)-(2*wheelS)), (0, 0))
        self.fwJntS = pymunk.constraint.DampedSpring(self.carBody, self.whBdyF, ((
            chSize[0]/2)-10, -chSize[1]/2), (0, 0), 2*wheelS, whstiff, whdamp)

        self.ls.append((self.whBdyF, self.wShapeF, self.fwJntG, self.fwJntS))

        # car Back Wheel
        self.whBdyB = pymunk.Body(wheelW, moment=10)
        self.whBdyB.position = pos[0] + \
            (-chSize[0]/2)+10, pos[1]+(-chSize[1]/2)-2*wheelS
        self.wShapeB = pymunk.Circle(self.whBdyB, wheelS)
        # self.wShapeB.weight = wheelW
        self.wShapeB.elasticity = whElast
        self.wShapeB.friction = whFric
        self.bwJntG = pymunk.constraint.GrooveJoint(
            self.carBody, self.whBdyB, ((-chSize[0]/2)+10, -chSize[1]/2), ((-chSize[0]/2)+10, (-chSize[1]/2)-(2*wheelS)), (0, 0))
        self.bwJntS = pymunk.constraint.DampedSpring(self.carBody, self.whBdyB, ((
            -chSize[0]/2)+10, -chSize[1]/2), (0, 0), 2*wheelS, whstiff, whdamp)
        self.bwmot = pymunk.constraint.SimpleMotor(
            self.whBdyB, space.static_body, inSpeed)
        self.ls.append((self.whBdyB, self.wShapeB, self.bwJntG, self.bwJntS))
        # jump
        # self.fjnpb = pymunk.Body()
        # self.fjnpb.position = (0,-(chSize[1]/2))

        self.bwJntG.max_force = 1000
        self.fwJntG.max_force = 1000

        # space opject add
        space.add(self.ls)

    def carDes(self):
        space.remove(self.ls)


class Terrain:

    def __init__(self, lent):
        self.tLis = self.terra(lent)
        noSegs = len(self.tLis)
        for j in range(noSegs-1):
            seg = pymunk.Segment(space.static_body, self.tLis[j], self.tLis[j+1], 5)
            seg.friction = 0.9
            seg.elasticity = 0.5
            space.add(seg)

    def terra(self, leng):
        ls = [(0, 10), (100, 10)]
        for i in range(100, leng+100, 100):
            j = r.randint(10, 80)
            ls.append((i, j))
        return ls
