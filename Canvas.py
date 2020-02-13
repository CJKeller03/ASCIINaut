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
        print(chr(27) + "[2J")
        print(chr(27) + "[1;1f")
        print(chr(27) + "[?25l")
  
    # for mac and linux(here, os.name is 'posix') 
    else: 
        _ = system('clear')

def stackCanvases(canvases):
    return Canvas(matrix = np.vstack([np.hstack([canvasObj.canvas for canvasObj in row]) for row in canvases]))

def formatCanvas(canvas):
    if type(canvas) == Canvas:
        strArray = canvas.asStrList()
    else:
        raise TypeError("formatCanvas requires an argument of type Canvas.")
    
    return "\n".join([" ".join(Row) for Row in strArray])
    
def createStackableCanvas(canvas, size, axis):
    matchingShape = canvas.canvas.shape

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

        return [[chr(int(v)) if v != 0 else " " for v in row] for row in self.canvas.T.tolist()]

    def initialize(self, offset = (0,0)):
        if self.initialMatrix is not None:
            self.canvas = self.initialMatrix
            self.size = self.initialMatrix.shape
        else:
            self.canvas = np.empty(self.size)

        self.offset = offset

    def drawSprite(self,sprite,position,avoidHoles = False):

        shape = sprite.shape

        if len(shape) != 2:
            raise ValueError("drawSprite requires a 2D numpy array as sprite")
        
        if not avoidHoles:
            self.canvas[position[0]+self.offset[0]:position[0]+shape[0]+self.offset[0],position[1]+self.offset[1]:position[1]+shape[1]+self.offset[1]] = sprite
        else:   
            raise Exception("avoidHoles not set up yet")
    
    def cutOutSection(self, size, position, alignment = "CENTER"):

        position = [position[0]+self.offset[0], position[1]+self.offset[1]]
        
        if alignment == "CENTER":
            self.canvas = self.canvas[position[0]-size[0]//2:position[0]+size[0]-size[0]//2,position[1]-size[1]//2:position[1]+size[1]-size[1]//2]
        elif alignment == "CORNER":
            self.canvas = self.canvas[position[0]:position[0]+size[0],position[1]:position[1]+size[1]]
        
    






