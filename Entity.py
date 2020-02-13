import numpy as np
import scipy.sparse
import timeit

def roundNearest(x, a):
    return round(x / a) * a


class Entity:

    def __init__(self, name, pos, sprite, mass = 1, rigidity = 0):
        
        self.name = name

        self.mass = mass
        self.rigidity = rigidity
        
        self.pos = np.array(pos)
        self.physicsPos = np.array(pos)
        self.vel = np.array([0,0])
        self.acc = np.array([0,0])
        
        if type(sprite) != np.array:
            self.sprite = np.array(sprite).T
        else:
            self.sprite = sprite.T

        
    def applyForce(self, vector):

        self.acc = np.add(self.acc,np.divide(vector,self.mass))

    def applyAcc(self, vector):

        self.acc = np.add(self.acc,vector)

    def absorbEnergy(self, amount):
        #print(self.name,"absorbed",amount)
        pass
        
    def updatePhysics(self):
        self.physicsPos = np.add(self.physicsPos, np.round(self.vel,2))
        self.pos = np.rint(self.physicsPos).astype(int)
        self.vel = np.round(np.add(self.vel,self.acc),8)
        self.acc = np.zeros(2)

class Ship(Entity):

    def __init__(self, name, pos, sprite, mass = 1, rigidity = 0.1, crumpleThreshold = 10, maxHullStrength = 50):

        self.crumpleThreshold = crumpleThreshold
        self.maxHullStrength = maxHullStrength
        self.hullStrength = maxHullStrength

        self.damageScale = 1

        self.absorbEnergy = True

        super().__init__(name, pos, sprite, mass, rigidity)

    def disableInelasticCollision(self):
        self.absorbEnergy = False

    def enableInelasticCollision(self):
        self.absorbEnergy = True

    def absorbEnergy(self, amount):
        hullStrength -= amount*self.damageScale

        
            

class Asteroid(Entity):

    def __init__(self, pos, sprite, mass = 100):

        super().__init__("Asteroid", pos, sprite, mass, 0)






