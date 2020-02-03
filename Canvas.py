# import only system from os 
from os import system, name 
  
# import sleep to show output for some time period 
from time import sleep

import numpy as np
import scipy.sparse
import itertools
  
# define our clear function

def clearScreen(): 
  
    # for windows 
    if name == 'nt': 
        _ = system('cls') 
  
    # for mac and linux(here, os.name is 'posix') 
    else: 
        _ = system('clear')

def stackCanvases(canvases):
    return Canvas(matrix = scipy.sparse.vstack([scipy.sparse.hstack([canvasObj.canvas for canvasObj in row]) for row in canvases]))

def formatCanvas(canvas):
    if type(canvas) == Canvas:
        strArray = canvas.asStrList()
    else:
        raise TypeError("formatCanvas requires an argument of type Canvas.")
    
    return "\n".join([" ".join(Row) for Row in strArray])
    
def createStackableCanvas(canvas, size, axis):
    matchingShape = canvas.canvas.get_shape()

    if axis == "X":
        return Canvas((matchingShape[0],size))
    elif axis == "Y":
        return Canvas((size,matchingShape[0]))

    
class Canvas:

    def __init__(self, size = None, matrix = None, offset = (0,0)):

        self.initialMatrix = matrix
        self.size = size
        self.offset = offset
        self.initialize()

    def asIntArray(self):

        return self.canvas.toarray().T

    def asStrList(self):

        return [[chr(int(v)) if v != 0 else " " for v in row] for row in self.canvas.toarray().T]

    def initialize(self, offset = (0,0)):
        if self.initialMatrix is not None:
            self.canvas = self.initialMatrix
            self.size = self.initialMatrix.get_shape()
        else:
            self.canvas = scipy.sparse.lil_matrix(self.size)

        self.offset = offset

    def drawSprite(self,sprite,position,avoidHoles = False):

        shape = sprite.get_shape()
        
        if not avoidHoles:
            self.canvas[position[0]+self.offset[0]:position[0]+shape[0]+self.offset[0],position[1]+self.offset[1]:position[1]+shape[1]+self.offset[1]] = sprite
        else:
            spriteFast = sprite.tocoo()    
            for x,y,v in itertools.izip(spriteFast.row, spriteFast.col, spriteFast.data):
                if v != 0:
                    self.canvas[x+position[0]+self.offset[0],y+position[1]+self.offset[1]] = v
    
    def cutOutSection(self, size, position, alignment = "CENTER"):

        position = [position[0]+self.offset[0], position[1]+self.offset[1]]
        
        if alignment == "CENTER":
            self.canvas = self.canvas[position[0]-size[0]//2:position[0]+size[0]-size[0]//2,position[1]-size[1]//2:position[1]+size[1]-size[1]//2]
        elif alignment == "CORNER":
            self.canvas = self.canvas[position[0]:position[0]+size[0],position[1]:position[1]+size[1]]
        
    



#A = Canvas((5,5))
#A.drawSprite(scipy.sparse.lil_matrix([[65,65]]),(0,0))

#B = createStackableCanvas(A, 5, "X")
#B.drawSprite(scipy.sparse.lil_matrix([[66,66],[66,66]]),(0,0))

#C = stackCanvases([[A],[B],[B]])

#print(formatCanvas(C))



A = Canvas((10,10))
A.drawSprite(scipy.sparse.lil_matrix([[65,65],[65,65]]),(3,3))
print(formatCanvas(A))
A.cutOutSection((5,5),(3,3))
print(formatCanvas(A))
