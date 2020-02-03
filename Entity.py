import numpy as np
import scipy.sparse

class Entity:

    def __init__(self, fileName, pos, sprite):
        
        self.fileName = fileName
        self.pos = pos
        self.vel = np.array((0,0))
        self.acc = np.array((0,0))
        
        if type(sprite) == list:
            self.sprite = scipy.sparse.lil_matrix(sprite)
        else:
            self.sprite = sprite

        
    def applyForce(self, direction, magnitude):

        self.acc = np.add(self.acc,np.multiply(direction, magnitude))
    
        
