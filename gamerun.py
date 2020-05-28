import pymunk
from gameClasses import *
import pygame
import math

# functions
trqVal = 0
trqt = 0
changle = 0
tempmax = 0
def cusEve(temp):
    global trqVal,changle,tempmax,trqt
    car1.carBody.torque = trqVal
    # car1.whBdyB.torque = trqt
    # tempmax = max(tempmax,car1.bwmot.impulse/(10/30/500))
    # print(tempmax)
    # car1.carBody.angle += changle*math.pi/180
    for event in temp:
        
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_b:
                bdy.position = 198,250
                bdy.velocity = pymunk.Vec2d(0,0)
            if event.key == pygame.K_SPACE:
                car1.carDes()
                car1.__init__((250,250))
            if event.key == pygame.K_RIGHT:
                # trqVal += -100
                space.add(car1.bwmot)
                car1.bwmot.rate = -1
                print(car1.bwmot.impulse)
            if event.key == pygame.K_LEFT:
                trqt = 5000
                # space.add(car1.bwmot)
                # car1.bwmot.rate = 1
            if event.key == pygame.K_j:
                # bdy.velocity = bdy.rotation_vector*10
                car1.carBody.velocity = (0,100)
            
            if event.key == pygame.K_q:
                changle = 5
                trqVal = 1000000
            if event.key == pygame.K_e:
                changle = -5
                trqVal = -1000000

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_q or event.key == pygame.K_e:
                changle = 0
                trqVal = 0
            if event.key == pygame.K_RIGHT or event.key == pygame.K_LEFT:
                # trqt = 0
                # pass
                # print(car1.bwmot.impulse)
                space.remove(car1.bwmot)
            
            
        # print(car1.whBdyB.torque)
        
        # bdy.angle += changle*math.pi/180
        # print("{:.2f}".format(bdy.angle*(180/math.pi)),bdy.rotation_vector)

# driver code
spaList = []

segFloor = pymunk.Segment(space.static_body,(0,10),(500,10),5)
segFloor.elasticity = 0.9
segFloor.friction = 0.9
spaList.append(segFloor)

segF = pymunk.Segment(space.static_body,(500,10),(600,50),5)
segF.friction = 0.8
spaList.append(segF)

# bdy = pymunk.Body()
# bdy.position = 250,250
# spe = pymunk.Poly.create_box(bdy,(100,50))
# spe.density = 10
# # spe = pymunk.Circle(bdy,20)
# spe.elasticity = 0.9
# spaList.append((spe,bdy))

car1 = Car((250,250))
# car1.bwmot.max_force = 5


space.add(spaList)
app = App(sH=500)
app.custEvent = cusEve
app.run()


            
