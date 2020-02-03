import numpy as np
import random
import math
import keyboard
import GraphicsController as GC
import MapHandler as MH
import timeit

class GraphicsIntegrator:

    def __init__(self,ViewArea, ChunkSize = 11):

        self.World = MH.World("Test",ChunkSize)
        self.Renderer = GC.Renderer(ViewArea)
        self.ViewArea = ViewArea


    def DrawSprite(self,Sprite,Pos):
        self.Renderer.DrawSprite(Sprite,Pos)
        

    def DrawWorld(self, Pos):
        ViewTL, View = self.World.GetRegion(Pos)

        #print("ViewTL:",ViewTL)

        #View[Pos[1]-ViewTL[1]][Pos[0]-ViewTL[0]] = "X"
        
        #print(View)

        self.Renderer.UpdateBackground(View,ViewTL)

        self.DrawSprite(Ship,ShipPos)
        

        #print("RenderOff:",[Pos[0]-ViewTL[0], Pos[1]-ViewTL[1]])

        self.Renderer.DrawFrame(Pos,"CENTER")
        





#Center = CenterPos(Background)        
#TopLeft = (Center[0]-(self.ViewArea[0]//2)+Offset[0], Center[1]-(self.ViewArea[1]//2)+Offset[1])
#BottomRight = (Center[0]+(self.ViewArea[0]//2)+Offset[0], Center[1]+(self.ViewArea[1]//2)+Offset[1])


Ship = [["A","A","A"],
        ["<","-",">"],
        ["V","V","V"]]

ShipPos = [0,0]
GI = GraphicsIntegrator((50,50),75)

while True:
    if keyboard.is_pressed("w"):
        ShipPos[1] -= 1
    if keyboard.is_pressed("s"):
        ShipPos[1] += 1
    if keyboard.is_pressed("a"):
        ShipPos[0] -= 1
    if keyboard.is_pressed("d"):
        ShipPos[0] += 1

    #GI.DrawSprite(Ship,ShipPos)
    
    GI.DrawWorld(ShipPos)

    print(ShipPos)




#print("FPS:",Frames/timeit.timeit(Code,setup = Setup, number = Frames))



Frames = 100

Setup = '''
import numpy as np
import random
import math
import keyboard
import GraphicsController as GC
import MapHandler as MH

class GraphicsIntegrator:

    def __init__(self,ViewArea, ChunkSize = 11):

        self.World = MH.World("Test",ChunkSize)
        self.Renderer = GC.Renderer(ViewArea)
        self.ViewArea = ViewArea


    def DrawSprite(self,Sprite,Pos):
        self.Renderer.DrawSprite(Sprite,Pos)
        

    def DrawWorld(self, Pos):
        ViewTL, View = self.World.GetRegion(Pos)

        #print("ViewTL:",ViewTL)

        #View[Pos[1]-ViewTL[1]][Pos[0]-ViewTL[0]] = "X"
        
        #print(View)

        self.Renderer.UpdateBackground(View,ViewTL)
        

        #print("RenderOff:",[Pos[0]-ViewTL[0], Pos[1]-ViewTL[1]])

        self.Renderer.DrawFrame(Pos,"CENTER")
        

ShipPos = [0,0]
GI = GraphicsIntegrator((50,50),75)

Ship = [["A","A","A"],
        ["<","[]",">"],
        ["V","V","V"]]
'''

Code = '''
if keyboard.is_pressed("w"):
    ShipPos[1] -= 1
if keyboard.is_pressed("s"):
    ShipPos[1] += 1
if keyboard.is_pressed("a"):
    ShipPos[0] -= 1
if keyboard.is_pressed("d"):
    ShipPos[0] += 1

GI.DrawSprite(Ship,ShipPos)
    
GI.DrawWorld(ShipPos)

print(ShipPos)
'''
