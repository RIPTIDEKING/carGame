import pymunk
from gameClasses import *
from pymunk.vec2d import Vec2d
import pygame
import math

# functions
trqVal = 0
trqt = 0
changle = 0
tempmax = 0

segType =type(pymunk.Segment(None,(0,0),(0,0),0))

def air_land(las,curr):
    if not las == curr:
        if curr:
            print('changed to air')
        else:
            print('changed to land')



def cusEve(temp, camera):
    global trqVal, changle, tempmax, trqt

    # camera
    camera[0] = -car1.carBody.position[0] + 85
    car1.carBody.torque = trqVal
    car1.whBdyB.torque = trqt
    
    lisb = space.bb_query(car1.wShapeB.bb,car1.wShapeB.filter)
    flag = False
    for i in lisb:
        if type(i) == segType:   
            flag = True
            break
    
    if not flag:
        lisf = space.bb_query(car1.wShapeF.bb,car1.wShapeB.filter)
        for i in lisf:
                if type(i) == segType:   
                    flag = True
                    break   
    car1.carAirLas = car1.carAirCurr
    car1.carAirCurr = not flag
    air_land(car1.carAirLas,car1.carAirCurr)


    for event in temp:

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_b:
                bdy.position = 198, 250
                bdy.velocity = pymunk.Vec2d(0, 0)
            if event.key == pygame.K_SPACE:
                car1.carDes()
                car1.__init__((250, 250))
            if event.key == pygame.K_RIGHT:
                # trqVal += -100
                space.add(car1.bwmot)
                car1.bwmot.rate = -2
                trqVal = 2000000
                
            if event.key == pygame.K_LEFT:
                space.add(car1.bwmot)
                car1.bwmot.rate = 2
                trqVal = -2000000
            
            if event.key == pygame.K_x:
                car1.bwmot.rate *= 5 

            if event.key == pygame.K_j:
                # ttt = Vec2d(-bdy.rotation_vector[1],bdy.rotation_vector[0])
                # bdy.velocity = ttt*10
                prepMul = Vec2d(
                    (-car1.carBody.rotation_vector[1], car1.carBody.rotation_vector[0]))
                car1.carBody.velocity = prepMul*100

            if event.key == pygame.K_q:
                changle = 5
                trqVal = 2000000
            if event.key == pygame.K_e:
                changle = -5
                trqVal = -2000000

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_q or event.key == pygame.K_e:
                changle = 0
                trqVal = 0
            if event.key == pygame.K_RIGHT:
                trqVal = 0
                space.remove(car1.bwmot)
            if event.key == pygame.K_LEFT:
                space.remove(car1.bwmot)
                trqVal = 0

        # print(car1.whBdyB.torque)

        # bdy.angle += changle*math.pi/180
        # print("{:.2f}".format(bdy.angle*(180/math.pi)),bdy.rotation_vector)


# driver code
spaList = []

# segFloor = pymunk.Segment(space.static_body,(0,10),(500,10),5)
# segFloor.elasticity = 0.9
# segFloor.friction = 0.9
# spaList.append(segFloor)

# segF = pymunk.Segment(space.static_body,(500,10),(600,50),5)
# segF.friction = 0.8
# spaList.append(segF)

# Next TODO: smooth terrain using peril noise, controls change(most work with only L or R)

# bdy = pymunk.Body()
# bdy.position = 250,280
# spe = pymunk.Poly.create_box(bdy,(100,50))
# spe.density = 10
# # spe = pymunk.Circle(bdy,20)
# spe.elasticity = 0.9
# spaList.append((spe,bdy))

car1 = Car((250, 250),whFric=1.5,moment=10)
# car1.bwmot.max_force = 5

tlength = 10000

space.add(spaList)
Terrain(tlength,persistence= 1.8,lacunarity=5.0,octaves=2)
app = App(sH=500, aH=500,aL=tlength)
app.custEvent = cusEve
app.run()
