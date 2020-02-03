import numpy as np
import os
import pickle

import Entity

class MapLoader:

    def __init__(self, saveFolder, chunkSize = 200, loadRange = 100):
        
        self.saveFolder = saveFolder
        self.chunkSize = chunkSize
        self.loadRange = loadRange
        
        self.currentEntities = []
        self.savedChunks = None

    def getEntities(self, pos):
        chunkPos = [pos[0]//self.chunkSize,pos[1]//self.chunkSize]
        
        chunkPath = self.saveFolder+"\\World\\Chunk_{}~{}".format(*chunkPos)
        
        entities = []
        
        if not os.path.exists(chunkPath):
            self.generateChunk(pos)
        
        for file in os.listdir(chunkPath+"\\Entities"):
            if file.endswith("pkl"):
                with open(chunkPath+"\\Entities\\"+file,"rb") as entity:
                    entities.append(pickle.load(entity))
        
        return entities
    
    def saveEntities(self, entities, pos):
        chunkPath = self.saveFolder+"\\World\\Chunk_{}~{}".format(*[pos[0]//self.chunkSize,pos[1]//self.chunkSize])
        
        for entity in entities:
            with open(chunkPath+entity.fileName+".pkl","wb") as file:
                pickle.dump(entity, file, protocol = pickle.HIGHEST_PROTOCOL)

    
    def generateChunk(self, pos):
        chunkPos = [pos[0]//self.chunkSize,pos[1]//self.chunkSize]

        chunkPath = self.saveFolder+"\\World\\Chunk_{}~{}".format(*chunkPos)

        if os.path.exists(chunkPath):
            return
        else:
            os.makedirs(chunkPath+"\\Entities",exist_ok = True)

        entities = [Entity.Entity("TestEntity",(chunkPos[0]*self.chunkSize,chunkPos[1]*self.chunkSize),[[65,65],[65,65]])]
        
        for entity in entities:
            with open(chunkPath+"\\Entities\\"+entity.fileName+".pkl","wb") as file:
                pickle.dump(entity, file, protocol = pickle.HIGHEST_PROTOCOL)

    
    def getRegion(self,pos):
        chunkPos = [pos[0]//self.chunkSize,pos[1]//self.chunkSize]

        #DeltaX = CircleX - Max(RectX, Min(CircleX, RectX + RectWidth));
        #DeltaY = CircleY - Max(RectY, Min(CircleY, RectY + RectHeight));
        #return (DeltaX * DeltaX + DeltaY * DeltaY) < (CircleRadius * CircleRadius);
        
        topLeft = [float("inf"),float("inf")]

        nearEntities = []
        
        for y in range(-1,2):
            for x in range(-1,2):
                chunkX = (chunkPos[0]+x)*self.chunkSize
                chunkY = (chunkPos[1]+y)*self.chunkSize
                
                deltaX = pos[0] - max(chunkX, min(pos[0], chunkX + self.chunkSize))
                deltaY = pos[1] - max(chunkY, min(pos[1], chunkY + self.chunkSize))

                if (deltaX**2 + deltaY**2) < (self.loadRange**2):
                    
                    nearEntities.extend(self.getEntities((chunkX,chunkY)))
                    topLeft[0] = min(topLeft[0],chunkX)
                    topLeft[1] = min(topLeft[1],chunkY)
                    
        
        return nearEntities, topLeft








      
