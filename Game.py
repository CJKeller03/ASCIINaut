import random
import math
import keyboard
import os
import scipy.sparse
import timeit
import time
import numpy as np
import traceback

import ctypes

kernel32 = ctypes.windll.kernel32
kernel32.SetConsoleMode(kernel32.GetStdHandle(-11), 7)

import Entity
import WorldLoader
import Canvas
import Physics


View = Canvas.Canvas(size = (1000,800))
World = WorldLoader.MapLoader(os.getcwd())

playerShip = Entity.Entity("player", (3,0), np.array([[88]]))
asteroid = Entity.Asteroid((20,0), np.array([[60,62]]), 10)
asteroid.vel = np.array((-0.01,0))

while True:
    try:
        
        entities, offset = World.getChunks(playerShip.pos)
        View.initialize((-offset[0],-offset[1]))
        
        if keyboard.is_pressed("w"):
            playerShip.applyAcc((0,-0.005))
        if keyboard.is_pressed("s"):
            playerShip.applyAcc((0,0.005))
        if keyboard.is_pressed("a"):
            playerShip.applyAcc((-0.005,0))
        if keyboard.is_pressed("d"):
           playerShip.applyAcc((0.005,0))

        
        
        entities.append(playerShip)
        entities.append(asteroid)
        
        for entity in entities:
            if entity.name == "player":
                pass
                #print("before:",entity.pos)
            View.drawSprite(entity.sprite,entity.pos)

        

        
        
        #print(Canvas.formatCanvas(View))

        #print("CUT")

        View.cutOutSection((50,50),playerShip.pos)
        
        Canvas.clearScreen()
        
        print(Canvas.formatCanvas(View))
        
        

        
        for i in range(len(entities)-1):
            for j in range(i+1,len(entities)):
                if Physics.checkEntityCollision(entities[i],entities[j]):
                    #print("collision")
                    Physics.calcCollision(entities[i],entities[j])

        print(playerShip.pos,playerShip.physicsPos,playerShip.vel,playerShip.acc)

        for entity in entities:
            entity.updatePhysics()
    
    except Exception as e:
        traceback.print_exc()
        input()
    

    time.sleep(0.01)



exit()

print(500/timeit.timeit('''

if keyboard.is_pressed("w"):
    playerShip.applyForce((0,-1),0.01)
if keyboard.is_pressed("s"):
    playerShip.applyForce((0,1),0.01)
if keyboard.is_pressed("a"):
    playerShip.applyForce((-1,0),0.01)
if keyboard.is_pressed("d"):
    playerShip.applyForce((1,0),0.01)


playerShip.updatePhysics()

entities, offset = World.getChunks(playerShip.pos)

View.initialize((-offset[0],-offset[1]))

for entity in entities:
    View.drawSprite(entity.sprite,entity.pos)

View.drawSprite(playerShip.sprite,playerShip.pos)



#print(Canvas.formatCanvas(View))

#print("CUT")

View.cutOutSection((50,50),playerShip.pos)

Canvas.clearScreen()

print(Canvas.formatCanvas(View))
print(playerShip.pos,playerShip.physicsPos,playerShip.vel,playerShip.acc)
time.sleep(0.01)



#input()


''',
'''
import random
import math
import keyboard
import os
import scipy.sparse
import timeit
import time
import numpy as np

import ctypes

kernel32 = ctypes.windll.kernel32
kernel32.SetConsoleMode(kernel32.GetStdHandle(-11), 7)

import Entity
import WorldLoader
import Canvas


View = Canvas.Canvas(size = (1000,800))
World = WorldLoader.MapLoader(os.getcwd())

playerShip = Entity.Entity("player",(0,0),np.array([[88]]))


''', number = 500))

input()
