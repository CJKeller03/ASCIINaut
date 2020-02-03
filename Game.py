import random
import math
import keyboard
import os
import scipy.sparse
import timeit

import Entity
import WorldLoader
import Canvas

View = Canvas.Canvas((500,500))
World = WorldLoader.MapLoader(os.getcwd())


shipSprite = scipy.sparse.lil_matrix([88])

ShipPos = [0,0]

print(1000/timeit.timeit('''

if keyboard.is_pressed("w"):
    ShipPos[1] -= 1
if keyboard.is_pressed("s"):
    ShipPos[1] += 1
if keyboard.is_pressed("a"):
    ShipPos[0] -= 1
if keyboard.is_pressed("d"):
    ShipPos[0] += 1


entities, offset = World.getRegion(ShipPos)

#print(entities)

View.initialize((-offset[0],-offset[1]))

for entity in entities:
    View.drawSprite(entity.sprite,entity.pos)

View.drawSprite(shipSprite,ShipPos)



#print(Canvas.formatCanvas(View))

#print("CUT")

View.cutOutSection((50,50),ShipPos)

Canvas.clearScreen()
print(Canvas.formatCanvas(View))

print(ShipPos)

#input()
''',
'''
import random
import math
import keyboard
import os
import scipy.sparse
import timeit
import Entity
import WorldLoader
import Canvas

View = Canvas.Canvas((500,500))
World = WorldLoader.MapLoader(os.getcwd())


shipSprite = scipy.sparse.lil_matrix([88])

ShipPos = [0,0]
''', number = 1000))

input()

while True:
    if keyboard.is_pressed("w"):
        ShipPos[1] -= 1
    if keyboard.is_pressed("s"):
        ShipPos[1] += 1
    if keyboard.is_pressed("a"):
        ShipPos[0] -= 1
    if keyboard.is_pressed("d"):
        ShipPos[0] += 1

    
    entities, offset = World.getRegion(ShipPos)

    #print(entities)
    
    View.initialize((-offset[0],-offset[1]))

    for entity in entities:
        View.drawSprite(entity.sprite,entity.pos)

    View.drawSprite(shipSprite,ShipPos)
    
    

    #print(Canvas.formatCanvas(View))

    #print("CUT")

    View.cutOutSection((50,50),ShipPos)

    Canvas.clearScreen()
    print(Canvas.formatCanvas(View))
    
    print(ShipPos)

    #input()


