import pymunk
from gameClasses import *
from pymunk.vec2d import Vec2d
import pygame
import math


# functions
trqt = 0
changle = 0
tempmax = 0

segType =type(pymunk.Segment(None,(0,0),(0,0),0))

def air_land(las,curr):
    if not las == curr:    
        car1.air_land_trans(not curr)



def cusEve(temp, camera):
    global changle, tempmax, trqt

    #sprit handle
    app.terrainDraw(terrain)
    app.spritHand(tire,car1.whBdyB)
    app.spritHand(tire,car1.whBdyF)
    app.spritHand(chasis,car1.carBody)

    # camera
    camera[0] = -car1.carBody.position[0] + 90
    car1.carBody.torque = car1.torqNeed
    car1.whBdyB.torque = trqt

    if car1.carBody.position[0] >= 8000:
        print(car1.carBody.position)
        terrain.stPnt = 791
        terrain.edPnt = 1700
        terrain.terrUpdate()
        car1.carTransp(90)
        
    
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
            elif event.key == pygame.K_SPACE:
                car1.carDes()
                car1.__init__((250, 250))
            elif event.key == pygame.K_RIGHT:
                car1.carMov(-1)    
            elif event.key == pygame.K_LEFT:
                car1.carMov(1)
            elif event.key == pygame.K_UP:
                car1.bwmot.rate *= 5 
            elif event.key == pygame.K_j:
                prepMul = Vec2d(
                    (-car1.carBody.rotation_vector[1], car1.carBody.rotation_vector[0]))
                car1.carBody.velocity = prepMul*100

        if event.type == pygame.KEYUP:
           
            if event.key == pygame.K_RIGHT or event.key == pygame.K_LEFT:
                car1.carMov(0)
            if event.key == pygame.K_UP:
                car1.bwmot.rate /= 5
       


# driver code
spaList = []

car1 = Car((250, 250),whFric=1.5,moment=10)
# car1.bwmot.max_force = 5
    
tlength = 10000

space.add(spaList)
terrain = Terrain(tlength,persistence= 1.8,lacunarity=5.0,octaves=2)
app = App(sH=height, aH=height,aL=tlength)
app.custEvent = cusEve
app.run()
